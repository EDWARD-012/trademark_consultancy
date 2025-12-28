
<!-- ================= HERO ================= -->
<h1 align="center">⚖️ Trademark Consultancy Platform</h1>

<p align="center">
  <b>A production-grade, startup-level SaaS platform for Trademark & IP Consultancy</b><br/>
  Built & maintained as a <b>real startup contribution</b> — not a demo project.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Django-4.x-0C4B33?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Live%20%26%20Production-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-purple?style=for-the-badge"/>
</p>

<p align="center">
  🌐 <a href="https://trademark-consultancy.vercel.app"><b>Live Website</b></a> •
  🚀 <a href="#deployment-guide"><b>Deployment</b></a> •
  📧 <a href="#email--notification-system"><b>Email System</b></a> •
  🤝 <a href="#contributing"><b>Contributing</b></a>
</p>

---

## 🧠 Project Vision (Startup Mindset)

This project was developed with a **startup-first engineering mindset**:

✔ Real services  
✔ Real users  
✔ Real email notifications  
✔ Real deployment & monitoring  

**Trademark Consultancy** digitizes traditional trademark & IP workflows into a modern web platform used by consultants and agencies.

> Think of it as a **legal-tech SaaS MVP** built with production standards.

---

## 🔥 What Makes This Project Different

- 🚫 Not a college demo  
- 🏢 Built for real consultancy operations  
- 📩 Emails actually reach admins & clients  
- 🔐 Secrets & configs handled securely  
- 🌍 Deployed on real cloud platforms  

This is the type of project recruiters expect when they ask:
> “Have you worked on real-world systems?”

---

## ✨ Features Overview

### 📄 Real Consultancy Services (Live)
All services listed are **real & operational**:

- ™ Trademark Registration
- 🔁 Trademark Renewal
- ⚠️ Trademark Objection Handling
- ❌ Trademark Opposition
- © Copyright Registration
- 📜 Legal Documentation Support

Each service includes:
- Dedicated form
- Backend validation
- Email trigger
- Admin-side tracking

---

### 📧 Email & Notification System

A **fully functional SMTP-based email system** is integrated.

✔ Admin notification on every lead  
✔ Automatic confirmation emails  
✔ SMTP via environment variables  
✔ Works with Gmail / Zoho / Custom SMTP  

#### Environment Variables
```env
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
ADMIN_EMAIL=admin@example.com
```

---

### 🔐 Security & Configuration

- Environment-based configs (Vercel-ready)
- Secrets never committed to repo
- CSRF & form validation enabled
- Debug toggle via env variable

```env
DEBUG=False
SECRET_KEY=your_secret_key
DATABASE_URL=your_db_url
```

---

### 🎨 UI / UX (Gen-Z + Professional)
- Clean startup-grade UI
- Tailwind CSS styling
- Fully responsive
- Legal-tech brand friendly

---

## 🧱 Tech Stack

| Layer | Tech |
|-----|-----|
| Backend | Django, Python |
| Frontend | HTML, Tailwind CSS |
| Database | SQLite (Dev), PostgreSQL (Prod) |
| Email | SMTP |
| Auth | Django Auth / Allauth |
| Deployment | Vercel / Render |
| Infra | Environment Variables |

---

## 📁 Project Structure

```text
trademark_consultancy/
├── accounts/        # Auth & users
├── leads/           # Leads & enquiries
├── services/        # Real consultancy services
├── core/            # Shared logic
├── templates/       # UI templates
├── static/          # Static files
├── config/          # Settings
└── manage.py
```

---

## ⚙️ Local Setup

```bash
git clone https://github.com/EDWARD-012/trademark_consultancy.git
cd trademark_consultancy
```

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate       # Windows
```

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

👉 http://127.0.0.1:8000

---

## 🚀 Deployment Guide

### 🌍 Deploy on Vercel (Production)

1. Push code to GitHub
2. Import repository in **Vercel**
3. Add Environment Variables:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `DATABASE_URL`
   - `EMAIL_HOST_USER`
   - `EMAIL_HOST_PASSWORD`
   - `ADMIN_EMAIL`
4. Set build command:
```bash
pip install -r requirements.txt
```
5. Set output:
```bash
python manage.py collectstatic --noinput
```
6. Deploy 🚀

---

### ☁️ Deploy on Render (Alternative)

```bash
Build Command:
pip install -r requirements.txt

Start Command:
gunicorn config.wsgi:application
```

---

## 🧪 Admin Panel

```bash
python manage.py createsuperuser
```

Visit:
👉 `/admin/`

---

## 🧑‍💻 Author & Startup Contributor

<p align="center">
  <b>Ravi Kumar Gupta (EDWARD-012)</b><br/>
  Senior Django Developer • Backend Engineer • Startup Contributor
</p>

<p align="center">
  <a href="https://github.com/EDWARD-012">GitHub</a> •
  <a href="https://www.linkedin.com/in/edward7780/">LinkedIn</a>
</p>

---

## 🤝 Contributing

PRs are welcome.
If you're improving UX, performance, or security — you're contributing to a real product.

---

## 📜 License

MIT License.

---

<p align="center">
  ⭐ If this project helped you understand real-world Django systems, drop a star!
</p>
