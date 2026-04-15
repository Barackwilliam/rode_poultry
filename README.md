# 🐓 Rode Poultry Tanzania Limited — Website

Django e-commerce website for **Rode Poultry Tanzania Limited**, built by [JamiiTek Ltd](https://jamiitek.co.tz).

## Tech Stack
- **Backend**: Django 5.0
- **Database**: PostgreSQL via Supabase
- **Hosting**: Render.com
- **Static files**: WhiteNoise
- **Languages**: English & Swahili (i18n)

---

## 🚀 Local Setup

### 1. Clone and create virtual environment
```bash
git clone <repo-url>
cd rode_poultry
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env with your Supabase DATABASE_URL and other values
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create admin superuser
```bash
python manage.py createsuperuser
```

### 6. Add logo image
Place the Rode Poultry logo at:
```
static/images/logo.png
static/images/favicon.png
```

### 7. Collect static and run
```bash
python manage.py collectstatic
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## 📦 Admin Panel

Go to `/admin/` to:
- Add **Products** and **Categories**
- Upload **Gallery** photos and YouTube videos
- Manage **Orders** and update delivery status
- View customer messages

---

## 🌍 Deploy to Render

1. Push code to GitHub
2. Go to [render.com](https://render.com) → **New** → **Blueprint**
3. Connect your GitHub repo — Render will read `render.yaml` automatically
4. Add these environment variables in Render dashboard:
   - `EMAIL_HOST_USER` = jjbacketa@gmail.com
   - `EMAIL_HOST_PASSWORD` = your Gmail App Password
   - `ALLOWED_HOSTS` = your-app.onrender.com,www.rodepoultry.co.tz

### Supabase Database Setup
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Go to **Settings → Database**
4. Copy the **Connection string (URI)** — use the **Transaction pooler** URL for Render
5. Paste as `DATABASE_URL` in Render environment variables

---

## 🌐 Custom Domain (rodepoultry.co.tz)
1. In Render: Go to your service → **Custom Domains** → add `www.rodepoultry.co.tz`
2. In your domain registrar: point DNS to Render's CNAME
3. Update `ALLOWED_HOSTS` to include `www.rodepoultry.co.tz,rodepoultry.co.tz`

---

## 📱 Features
- ✅ Bilingual: English & Swahili (toggle button)
- ✅ Product catalog with categories, search, stock tracking
- ✅ Shopping cart (session-based)
- ✅ Checkout with Cash on Delivery
- ✅ Email notifications to admin on new orders
- ✅ Order tracking by Order ID + phone
- ✅ Gallery: photos (lightbox) + YouTube videos (modal)
- ✅ Contact form with email notification
- ✅ Customer accounts with order history
- ✅ WhatsApp integration
- ✅ Fully responsive (mobile-first)
- ✅ Admin dashboard with order status management

---

## 👤 Built By
**JamiiTek Ltd** — Dar es Salaam, Tanzania  
Web Development | Mobile Apps | AI Chatbots  
www.jamiitek.co.tz
