# Instant Placement 🚀
**Your Next Job, Found Instantly.**

Instant Placement is a premium job aggregator SaaS that allows users to search across multiple platforms (LinkedIn, Indeed, Glassdoor, ZipRecruiter) in one place.

## Features
- **Global Search:** Search jobs by title, location, and keywords.
- **Real-Time Data:** Powered by JSearch API via RapidAPI.
- **Premium Tiers:** Free and Pro plans.
- **Pro Features:**
  - Real-time filters (Last 1 hour, Last 8 hours).
  - Unlimited search results.
  - Keyword exclusion & Remote-only filters.
  - Daily email job digests matching saved searches.
- **Beautiful UI:** Modern dark-themed design with glassmorphism and smooth animations.

## Tech Stack
- **Backend:** Django (MVT pattern)
- **Frontend:** Django Templates + Tailwind CSS + Vanilla JS
- **Database:** SQLite
- **Auth:** Django Auth + Allauth (Google OAuth)
- **Payments:** Stripe
- **Tasks:** Celery + Redis
- **Caching:** Redis

## Setup Instructions

### 1. Clone & Install
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=...
DEBUG=True
RAPIDAPI_KEY=...
STRIPE_SECRET_KEY=...
STRIPE_WEBHOOK_SECRET=...
STRIPE_PRICE_ID=...
REDIS_URL=redis://127.0.0.1:6379/1
EMAIL_HOST=smtp-relay.brevo.com
EMAIL_PORT=587
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
DEFAULT_FROM_EMAIL=Instant Placement <noreply@instantplacement.com>
```

### 3. Database & Admin
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Running Backend
```bash
python manage.py runserver
```

### 5. Running Celery
```bash
# In separate terminals
celery -A config worker --loglevel=info
celery -A config beat --loglevel=info
```

### 6. Stripe Webhook
```bash
stripe listen --forward-to localhost:8000/stripe/webhook/
```

## URL Structure
- `/` - Home
- `/jobs/results/` - Search results
- `/pricing/` - Pricing plans
- `/accounts/profile/` - User dashboard
- `/alerts/` - Saved searches (Pro)
- `/subscribe/checkout/` - Stripe payment

---
Developed by Antigravity AI
