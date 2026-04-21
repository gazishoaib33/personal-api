# 🧑 Personal API

A personal REST API built from scratch with **FastAPI** and **SQLite** to track books, expenses, and notes — with full CRUD operations, API key authentication, and auto-generated interactive documentation.

> Built as a learning project to understand backend development: routing, databases, authentication, and clean API design.

---

## 🚀 Live Demo

Run locally → visit `http://127.0.0.1:8000/docs` for the full interactive Swagger UI.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11+ | Core language |
| FastAPI | Web framework — routing, validation, docs |
| SQLAlchemy | ORM — Python classes mapped to DB tables |
| SQLite | Database — zero-config, file-based |
| Pydantic | Schema validation for inputs and outputs |
| Uvicorn | ASGI server that runs the app |
| python-dotenv | Loads secret key from .env file |

---

## 📁 Project Structure

```
personal_api/
├── main.py          # App entry point — registers routers, creates DB tables
├── database.py      # SQLAlchemy engine, session, and get_db dependency
├── models.py        # Database table definitions (Book, Expense, Note)
├── schemas.py       # Pydantic schemas — input validation and output shaping
├── auth.py          # API key authentication dependency
├── requirements.txt # All dependencies
├── .env             # Secret API key (not committed)
└── routers/
    ├── books.py     # All /books routes
    ├── expenses.py  # All /expenses routes
    └── notes.py     # All /notes routes
```

---

## ⚙️ Setup & Run

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/personal-api.git
cd personal-api
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create your .env file**
```
API_KEY=your-secret-key-here
```

**5. Run the server**
```bash
uvicorn main:app --reload
```

**6. Open the docs**
```
http://127.0.0.1:8000/docs
```

---

## 📚 API Resources

### Books — `/books`

Track your reading list with status and ratings.

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | /books | ❌ | List all books (filter by `?status=`) |
| GET | /books/{id} | ❌ | Get one book |
| POST | /books | ✅ | Add a book |
| PUT | /books/{id} | ✅ | Update a book |
| DELETE | /books/{id} | ✅ | Delete a book |

**Status values:** `want_to_read` · `reading` · `finished`

**Example:**
```bash
curl -X POST http://localhost:8000/books \
  -H "X-API-Key: your-secret-key-here" \
  -H "Content-Type: application/json" \
  -d '{"title": "Clean Code", "author": "Robert Martin", "status": "reading", "rating": 5}'
```

---

### Expenses — `/expenses`

Log and summarize your spending by category.

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | /expenses | ❌ | List all (filter by `?category=` or `?month=`) |
| GET | /expenses/summary | ❌ | Total spend + breakdown by category |
| GET | /expenses/{id} | ❌ | Get one expense |
| POST | /expenses | ✅ | Log an expense |
| DELETE | /expenses/{id} | ✅ | Delete an expense |

**Example summary response:**
```json
{
  "total": 55.50,
  "by_category": {
    "food": 20.50,
    "transport": 35.00
  }
}
```

---

### Notes — `/notes`

Create tagged notes with full-text search.

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | /notes | ❌ | List all (filter by `?tag=` or `?search=`) |
| GET | /notes/{id} | ❌ | Get one note |
| POST | /notes | ✅ | Create a note |
| PUT | /notes/{id} | ✅ | Update a note |
| DELETE | /notes/{id} | ✅ | Delete a note |

**Example search:**
```bash
curl "http://localhost:8000/notes?search=API"
```

---

## 🔐 Authentication

Read operations (GET) are **public** — no key needed.

Write operations (POST, PUT, DELETE) require an API key passed as a header:

```
X-API-Key: your-secret-key-here
```

Without the key you get a `403 Forbidden` response:
```json
{ "detail": "Invalid or missing API key." }
```

To test in Swagger UI, click the **Authorize** button at `/docs` and enter your key.

---

## 🧠 What I Learned

**Routing** — how HTTP methods (GET, POST, PUT, DELETE) map to operations using FastAPI's `@router` decorators.

**CRUD** — Create, Read, Update, Delete. Every resource implements all four using SQLAlchemy to interact with the database.

**ORM** — writing Python classes instead of raw SQL. SQLAlchemy maps `class Book` to a `books` table automatically.

**Pydantic Schemas** — separating what the API accepts (`BookCreate`) from what it returns (`BookOut`). Auto-validates incoming data and returns `422` if wrong.

**Dependency Injection** — FastAPI's `Depends()` system injects DB sessions and auth checks into routes without repeating code.

**API Key Authentication** — protecting write routes using a `Security` dependency that reads the `X-API-Key` header against the secret in `.env`.

**Query Parameters** — filtering with `?status=finished`, `?month=2025-04`, `?search=keyword` without extra routes.

**Project Structure** — splitting into `models.py`, `schemas.py`, `auth.py`, and `routers/` so each file has one clear responsibility.

---

## 📈 What's Next

- [ ] Add JWT authentication (login + expiring tokens)
- [ ] Add pagination (`?skip=0&limit=20`)
- [ ] Add a Workouts resource (same pattern)
- [ ] Migrate from SQLite to PostgreSQL
- [ ] Deploy to Railway or Render

---

## 📄 License

MIT — free to use and modify.
