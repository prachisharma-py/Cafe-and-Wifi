# ☕ Cafe & WiFi / London

**A Flask-based web app to find the best work-friendly cafes in London.**  
Easily browse, filter, and manage cafes based on Wi-Fi availability, socket access, seating, and other remote-worker-friendly features.

---

## 🚀 Live Demo

[![Live Demo](https://img.shields.io/badge/Live-Demo-green?style=for-the-badge)](https://your-demo-url.com)

---

## 📸 Preview

| Home Page                           | Filter Panel                         | Add Cafe Form                       |
|------------------------------------|--------------------------------------|-------------------------------------|
| ![Home](screenshots/home.png)      | ![Filters](screenshots/filters.png)  | ![Add Cafe](screenshots/add.png)    |

> Screenshots located in the `/screenshots` folder.

---

## 🚀 Features

- ✅ **Filter Cafes**
  - Wi-Fi availability
  - 🔌 Power sockets
  - 🚻 Toilets
  - 📞 Call-friendliness
  - 🪑 Number of seats (e.g., 0–10, 10–20, 50+)
- ➕ **Add New Cafes**
- ❌ **Delete Cafes**
- 🗺️ **Map Integration** – View cafes directly on Google Maps
- 📊 **Live Count & Smart Filtering**
- 🎨 **Modern, Responsive UI** – Built with Bootstrap 5 and FontAwesome
- 🛢️ **Database Flexibility** – SQLite locally, PostgreSQL on deployment

---

## 🛠 Tech Stack

| Layer         | Technology                                                 |
|---------------|------------------------------------------------------------|
| **Backend**   | Python, Flask                                              |
| **Frontend**  | HTML, CSS (Bootstrap 5), Jinja2, Font Awesome              |
| **Database**  | PostgreSQL (via [Neon](https://neon.tech)), SQLite         |
| **ORM**       | SQLAlchemy                                                 |
| **Forms**     | Flask-WTF, WTForms                                         |
| **Migrations**| Alembic                                                    |
| **Server**    | Gunicorn (for production)                                  |
| **Env Mgmt**  | `python-dotenv` for `.env` file-based config               |

---

## 🔋 Database & Deployment

This app supports flexible local and cloud deployment:

- ✅ **SQLite** for quick local development
- ✅ **PostgreSQL via [Neon](https://neon.tech)** for scalable, production-ready environments

You can configure the database using a `.env` file:

```env
# .env
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://<username>:<password>@<your-neon-host>.neon.tech/<database>?sslmode=require

---

### Using Neon means:

🚀 Serverless PostgreSQL

🔄 Auto-scaling & branching

🔐 Secure SSL connections

---

🙌 Contribution

Pull requests are welcome!
For major changes, please open an issue first to discuss what you'd like to change.
