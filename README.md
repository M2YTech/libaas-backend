# LibaasAI Backend

FastAPI backend for the LibaasAI wardrobe assistant application.

## Features

- 🔐 User authentication (signup/login)
- 🖼️ Image upload to Supabase Storage
- 🤖 AI-powered image analysis using CLIP model
- 📊 Fashion insights and recommendations

## Tech Stack

- **Framework**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage
- **AI Model**: OpenAI CLIP (clip-vit-base-patch32)
- **Authentication**: bcrypt password hashing

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend` folder:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

### 3. Set Up Supabase

#### Create the `users` table:

```sql
CREATE TABLE users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  gender VARCHAR(20) NOT NULL,
  height VARCHAR(20),
  country VARCHAR(100),
  body_shape VARCHAR(50),
  skin_tone VARCHAR(50),
  image_url TEXT,
  clip_insights JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for email lookups
CREATE INDEX idx_users_email ON users(email);
```

#### Create Storage Bucket:

1. Go to Supabase Dashboard → Storage
2. Create a new bucket called `profile_images`
3. Set it to **Public** bucket
4. Add policy to allow uploads

### 4. Run the Server

```bash
# From the backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### Authentication

#### POST `/auth/signup`

Register a new user with profile details and optional image.

**Request** (multipart/form-data):
- `name`: string (required)
- `email`: string (required)
- `password`: string (required, min 6 chars)
- `gender`: string (required: "male", "female", "other")
- `height`: string (optional)
- `country`: string (optional)
- `body_shape`: string (optional)
- `skin_tone`: string (optional)
- `image`: file (optional)

**Response**:
```json
{
  "message": "Signup successful",
  "user_id": "uuid",
  "clip_insights": {
    "top_label": "casual",
    "top_confidence": 0.85,
    "all_predictions": [...]
  }
}
```

#### POST `/auth/login`

Authenticate user with email and password.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response**:
```json
{
  "message": "Login successful",
  "user_id": "uuid",
  "name": "User Name",
  "email": "user@example.com"
}
```

#### GET `/auth/profile/{user_id}`

Get user profile by ID.

## CLIP Model

The backend uses the `openai/clip-vit-base-patch32` model for zero-shot image classification. It analyzes uploaded images to detect:

- Gender presentation (man/woman)
- Style (casual/formal/traditional)
- Clothing type (shirt, t-shirt, dress, etc.)
- Season suitability (summer/winter)

These insights are stored with the user profile and used for outfit recommendations.

## Development

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── database.py      # Supabase client
│   ├── schemas.py       # Pydantic models
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py    # Auth endpoints
│   │   ├── models.py    # User models
│   │   └── utils.py     # Password hashing, etc.
│   └── ai/
│       ├── __init__.py
│       └── clip_insights.py  # CLIP model
├── requirements.txt
├── .env.example
└── README.md
```

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`














