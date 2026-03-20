# Cithai Django – Exercise 3: Domain Layer Implementation

A Django-based domain layer for Cithai.

---

## Project Setup

### Requirements
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd cithai-django

# Install dependencies
pip install django djangorestframework

# Apply migrations
python manage.py migrate

# Create a superuser (for Admin CRUD)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/admin/` to access the Django Admin interface.

---

## Domain Model

The project implements four core domain entities:

### `User` (app: `user`)
Extends Django's built-in `AbstractUser` with:
- `max_song` — quota of songs a user can generate (default: 20)
- `auth_provider` — login method: `local` or `google`

### `Song` (app: `song`)
The central domain entity representing a generated song:
- `title`, `description`
- `occasion` — birthday, wedding, anniversary, holiday, other
- `genre` — pop, rock, jazz, classical, hiphop, rb, folk
- `voice_type` — male, female, instrumental
- `mood` — happy, sad, romantic, calm, funny
- `status` — generating → completed / failed
- `audiofile_url` — URL to the generated audio file (blank while generating)
- `is_private` — visibility control
- `created_at` — timestamp

**Relationships:**
- Many `Song`s belong to one `User` (ForeignKey)

### `SongGenerationRequest` (app: `songgenerationrequest`)
Tracks the AI generation job for each song:
- `song` — OneToOne link to `Song`
- `title`, `occasion`, `genre`, `voice_type`, `mood` — snapshot of what was requested
- `request_status` — generating / completed / failed
- `estimated_duration` — estimated generation time in seconds
- `requested_at` — timestamp

### `Sharelink` (app: `sharelink`)
A shareable link for a completed song:
- `song` — OneToOne link to `Song`
- `url` — the share URL
- `is_active` — whether the link is currently active

---

## CRUD Operations

All CRUD operations are available through **Django Admin** at `/admin/`.

### How to demonstrate CRUD:

1. Run the server and log in at `http://127.0.0.1:8000/admin/`
2. Navigate to any entity (Users, Songs, Song Generation Requests, Sharelinks)

| Operation | How to perform |
|-----------|---------------|
| **Create** | Click "Add" button on any model list page |
| **Read**   | Click any record to view its details |
| **Update** | Open a record and modify fields, then Save |
| **Delete** | Select records and use the "Delete selected" action, or open a record and click Delete |

### Suggested demo flow:
1. **Create** a User (Admin → Users → Add User)
2. **Create** a Song assigned to that user (Admin → Songs → Add Song)
3. **Create** a SongGenerationRequest linked to the song
4. **Create** a Sharelink for the song
5. **Update** the Song's `status` from `generating` to `completed` and add an `audiofile_url`
6. **Delete** the Sharelink to demonstrate deletion cascading

---

## Database

SQLite (default Django setup). The schema is fully defined by migrations in each app's `migrations/` folder.

---

## Project Structure

```
cithai-django/
├── mysite/              # Project config (settings, urls)
├── user/                # User domain entity
├── song/                # Song domain entity
├── songgenerationrequest/  # Generation job tracking
├── sharelink/           # Share link entity
├── db.sqlite3           # SQLite database
└── manage.py
```

## Demo Clip
[Watch Demo](https://www.youtube.com/watch?v=wLRInJ4SQEU)