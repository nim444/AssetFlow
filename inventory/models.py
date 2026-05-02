from django.db import models
from django.core.exceptions import ValidationError
from multiselectfield import MultiSelectField


class Item(models.Model):
    OWNER_CHOICES = [
        ('personal', 'Personal'),
        ('company', 'Company'),
    ]

    ASSET_TYPE_CHOICES = [
        ('none', 'None'),
        ('assets', 'Assets'),
        ('depreciation', 'Depreciation'),
    ]

    URGENCY_CHOICES = [
        ('low', 'Low - Can wait'),
        ('medium', 'Medium - Flexible'),
        ('high', 'High - Sell soon'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('archived', 'Archived'),
    ]

    SALES_PLATFORM_CHOICES = [
        ('olx', 'OLX'),
        ('facebook', 'Facebook Marketplace'),
        ('vinted', 'Vinted'),
        ('local', 'Local/In-person'),
        ('other', 'Other'),
    ]

    # Basic info
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    # Ownership & Classification
    owner = models.CharField(max_length=20, choices=OWNER_CHOICES)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES, default='none')

    # Status & Urgency
    functional_status = models.BooleanField(null=True, blank=True, help_text="True=Functional, False=Not functional, Null=Unknown")
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # Pricing
    sum_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Original cost / Total investment")
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Current market value")

    # Sales
    sales_platform = MultiSelectField(
        choices=SALES_PLATFORM_CHOICES,
        blank=True,
        null=True,
        help_text="Where you plan to sell this item"
    )

    # Tax
    tva_applied = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-urgency', '-created_at']
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.name

    def clean(self):
        """Validation: Can only set status to 'sold' if sale history exists"""
        if self.status == 'sold' and not self.sale_history.exists():
            raise ValidationError(
                "Cannot mark item as 'Sold' without a sale history record."
            )


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='items/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Item Image'
        verbose_name_plural = 'Item Images'

    def __str__(self):
        return f"Image for {self.item.name}"


class SaleHistory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='sale_history')
    sold_price = models.DecimalField(max_digits=10, decimal_places=2)
    sold_date = models.DateTimeField()
    buyer_info = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sold_date']
        verbose_name = 'Sale History'
        verbose_name_plural = 'Sale Histories'

    def __str__(self):
        return f"{self.item.name} - Sold on {self.sold_date.date()}"
