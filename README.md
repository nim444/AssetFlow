# AssetFlow

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0.4-092E20?style=for-the-badge&logo=django&logoColor=white)
![UV](https://img.shields.io/badge/UV-package_manager-DE5FE9?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

A personal asset management tool to track, value, and manage items you own — whether personal or company-owned. Built with Django and managed via UV.

Track what you have, what it's worth, where to sell it, and how the sale went.

---

## Features

<details>
<summary>📦 Item Management</summary>

- Track items with name, description, owner type (personal / company), and asset classification
- Set functional status: working, not working, or unknown
- Urgency levels: Low / Medium / High to prioritize what to sell first
- Item lifecycle: Draft → Active → Sold → Archived
- Multi-platform selling: list where you plan to sell (OLX, Facebook Marketplace, Vinted, Local, Other)

</details>

<details>
<summary>💰 Pricing & Tax</summary>

- Record the original cost (`sum_price`) and current estimated value (`estimated_price`)
- TVA (VAT) tracking flag per item
- Full sale history with sold price, date, and buyer info

</details>

<details>
<summary>🖼️ Image Support</summary>

- Attach multiple images per item
- Inline 75×75px thumbnail previews in the admin list view
- Images stored under `media/items/`

</details>

<details>
<summary>🛡️ Validation</summary>

- An item cannot be marked as **Sold** without a sale history record
- `full_clean()` called on every admin save to enforce model-level validation

</details>

---

## Tech Stack

```
assetflow/
├── assetflow/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
├── inventory/          # Core app
│   ├── models.py       # Item, ItemImage, SaleHistory
│   ├── admin.py        # Admin with inline previews
│   ├── migrations/
│   └── static/
│       └── inventory/
│           └── admin_preview.css
├── media/              # Uploaded item images
├── staticfiles/        # collectstatic output
├── manage.py
└── pyproject.toml      # UV-managed dependencies
```

| Layer | Tool |
|---|---|
| Language | Python 3.12 |
| Framework | Django 6.0.4 |
| Package manager | UV |
| Database | SQLite (dev) |
| Image handling | Pillow 12.2.0 |
| Multi-select field | django-multiselectfield |
| Tunnel (dev) | Cloudflare Tunnel |

---

## Setup

<details>
<summary>Requirements</summary>

- Python 3.12+
- [UV](https://docs.astral.sh/uv/) installed

</details>

<details>
<summary>Installation</summary>

```bash
# Clone the repo
git clone https://github.com/nim444/AssetFlow.git
cd AssetFlow

# Install dependencies
uv sync

# Apply migrations
uv run python manage.py migrate

# Create admin user
uv run python manage.py createsuperuser

# Start dev server
uv run python manage.py runserver
```

Then open [http://localhost:8000/admin](http://localhost:8000/admin)

</details>

<details>
<summary>Expose locally via Cloudflare Tunnel</summary>

```bash
# Install cloudflared (macOS)
brew install cloudflared

# Run tunnel (no account needed)
cloudflared tunnel --url http://localhost:8000
```

</details>

---

## License

MIT © [Nima Karimi](https://github.com/nim444)
