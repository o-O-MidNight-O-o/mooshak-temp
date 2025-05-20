# Mooshak 🛰️

**Mooshak** is a Django-based platform connecting **influencers**, **brands**, and **users** through structured profiles, ad collaborations, and a safe payment system. It supports media uploads, background tasks, role-based flows, and future integrations like the Instagram API.

---

## 🔑 User Roles

- 👤 User  
- 🏢 Brand  
- 🎥 Influencer  

Each role has its own dashboard, fields, and ad participation flow. Role verification is required for full access.

---

## 🚀 Core Features

### ✅ Authentication
- Email/password signup
- Role selection at registration
- Email verification (coming soon)

### ✅ Profiles
- First/last name, profile picture, optional banner
- Phone, city, country, role
- Social media links: Instagram, Twitter, Telegram, etc.
- Optional links like LinkedIn, Aparat, Twitch
- Referral code system
- Role-based profile tabs and restrictions

### ✅ Ads
- Brands and influencers can create ads
- Roles can request, accept, reject, or complete ads
- Ad metadata: title, banner, price range, platform, deadline, description
- Support for product-based collaborations

### ✅ Payments
- Safe payment escrow: hold until ad is verified
- Track income/outcome, wallet/card, ref ID, timestamps
- Loyalty percentage system for influencers (10%–50%)

### ✅ Background Tasks
- Image resizing via Celery
- Redis as task broker
- Media file upload and storage

### ✅ Search & Filter
- Search by:
  - Category, city, country
  - Role
  - Social media
  - Price
  - Can receive/send product or gifts
  - Platform type

---

## 📁 Project Structure

```txt
mooshak/
├── chat/               # Messaging logic (coming soon)
├── config/             # Django settings, Celery setup
├── core/               # Shared utilities, Celery tasks
├── profiles/           # User/brand/influencer models & APIs
├── templates/          # HTML templates (optional)
├── media/              # Uploaded images
└── manage.py
```
---

## ⚙️ Tech Stack

- Python 3.11+
- Django 5.2
- Django REST Framework
- Celery + Redis
- Pillow (image processing)
- SQLite (dev) → PostgreSQL (prod recommended)

---

## 🔧 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/o-O-MidNight-O-o/mooshak.git
cd mooshak
```
### 2. Set up virtualenv
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure .env
```bash
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```
### 5. Migrate and run
```bash
python manage.py migrate
python manage.py runserver
```
### 6. Start Celery (in another terminal)
```bash
celery -A config worker -l info
```
---

## 📡 API Highlights

| Method | Endpoint              | Purpose                       |
|--------|-----------------------|-------------------------------|
| POST   | `/api/register/`      | Register user                 |
| POST   | `/api/token/`         | Auth token (if JWT used)      |
| PATCH  | `/api/profiles/<id>/` | Update profile (image, links) |
| POST   | `/api/ads/`           | Create ad (brand/influencer)  |
| GET    | `/api/ads/`           | List/search ads               |


---

## 🛣️ Roadmap

- [x] Profile roles + media upload
- [x] Celery for background tasks
- [x] Social media links
- [ ] Messaging system
- [ ] Email verification
- [ ] Campaign management
- [ ] Insight tracking
- [ ] Instagram API
- [ ] Admin dashboard
- [ ] Docker + production setup

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

© 2025 [MidNight](https://github.com/o-O-MidNight-O-o)
