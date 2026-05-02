from django.contrib import admin
from .models import Item, ItemImage, SaleHistory


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1
    fields = ['image', 'uploaded_at']
    readonly_fields = ['uploaded_at']


class SaleHistoryInline(admin.TabularInline):
    model = SaleHistory
    extra = 0
    fields = ['sold_price', 'sold_date', 'buyer_info', 'notes', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemImageInline, SaleHistoryInline]

    list_display = ['name', 'owner', 'urgency', 'status', 'estimated_price', 'functional_status', 'image_count']
    list_filter = ['urgency', 'owner', 'status', 'asset_type', 'tva_applied', 'functional_status', 'sales_platform']
    search_fields = ['name', 'description']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'owner', 'asset_type')
        }),
        ('Status & Urgency', {
            'fields': ('status', 'urgency', 'functional_status')
        }),
        ('Pricing', {
            'fields': ('sum_price', 'estimated_price', 'tva_applied')
        }),
        ('Sales', {
            'fields': ('sales_platform',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

    def image_count(self, obj):
        count = obj.images.count()
        return f"{count} image{'s' if count != 1 else ''}"
    image_count.short_description = 'Images'

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    list_display = ['item', 'image', 'uploaded_at']
    list_filter = ['uploaded_at', 'item__owner']
    search_fields = ['item__name']
    readonly_fields = ['uploaded_at']


@admin.register(SaleHistory)
class SaleHistoryAdmin(admin.ModelAdmin):
    list_display = ['item', 'sold_price', 'sold_date', 'buyer_info']
    list_filter = ['sold_date', 'item__owner']
    search_fields = ['item__name', 'buyer_info']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Sale Information', {
            'fields': ('item', 'sold_price', 'sold_date')
        }),
        ('Buyer Details', {
            'fields': ('buyer_info', 'notes')
        }),
        ('System', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
