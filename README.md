# 📚 Gutenberg API

A Django-based REST API to query and filter Project Gutenberg book data.

---

## 🚀 Features

- Search and filter books by:
  - Gutenberg ID
  - Author (partial match)
  - Title (partial match)
  - Language(s)
  - Topic (subject or bookshelf, partial match)
  - Mime-type
- Paginated results sorted by popularity (`download_count`)
- Swagger UI for interactive API exploration
- Supports environment-based DB configuration

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sumitpareek1992/gutenberg_api.git
cd gutenberg_api
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Create `.env` File

Create a `.env` file in the root directory with the following content:

```
DB_USER=postgres
DB_NAME=books_db
DB_PASSWORD=tops?123
```

> Ensure PostgreSQL is installed and running on your system.

### 4. Create PostgreSQL Database

Login to your PostgreSQL client (e.g. `psql`) and run:

```sql
CREATE DATABASE books_db;
```

### 5. Load Gutendex Data

Take a dump of the Gutendex dataset and import it into the `books_db` database.
Ensure it maps to the models defined in your Django app.

---

## ▶️ Run the Application

### 6. Run Migrations

```bash
python3 manage.py migrate
```

### 7. Start the Server

```bash
python3 manage.py runserver
```

The Swagger documentation will be available at:

🌐 [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

---

## 📘 API Usage

### Base Endpoint

```
GET /api/books/
```

### Query Parameters

| Parameter     | Description                                                                |
|---------------|----------------------------------------------------------------------------|
| `book_id`     | Gutenberg ID(s), e.g. `book_id=1342,84`                                    |
| `language`    | Language code(s), e.g. `language=en,fr`                                    |
| `mime_type`   | Mime-types, e.g. `mime_type=application/epub+zip,text/plain`               |
| `topic`       | Subject or bookshelf name (partial), e.g. `topic=child,literature`         |
| `author`      | Author name (partial), e.g. `author=dickens,shakespeare`                   |
| `title`       | Book title (partial), e.g. `title=pride,prejudice`                         |

> All parameters support comma-separated multiple values.

### Example Request

```http
GET /api/books/?language=en&topic=children&author=dickens
```

---

## 🔁 Sample Response

```json
{
  "message": "Books fetch successfully",
  "status": true,
  "books": [
    {
      "title": "A Christmas Carol",
      "authors": ["Charles Dickens"],
      "language": ["en"],
      "subjects": ["Christmas stories"],
      "bookshelves": ["Children’s Literature"],
      "formats": [
        {"mime_type": "application/epub+zip", "url": "http://..."},
        {"mime_type": "text/plain", "url": "http://..."}
      ],
      "genre": "Children"
    }
  ],
  "total_recors": 1,
  "page_count": 1,
  "current_page": 1
}
```

---


## 🙋 Author

**Sumit Pareek**  
🔗 [GitHub](https://github.com/sumitpareek1992)
