-- ====================================
-- LibaasAI Database Setup
-- Run this SQL in Supabase SQL Editor
-- ====================================

-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  gender VARCHAR(20) NOT NULL CHECK (gender IN ('male', 'female', 'other')),
  height VARCHAR(20),
  country VARCHAR(100),
  body_shape VARCHAR(50),
  skin_tone VARCHAR(50),
  image_url TEXT,
  clip_insights JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for email lookups (faster login)
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Create index for created_at (for sorting)
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at DESC);

-- ====================================
-- Row Level Security (RLS) Policies
-- ====================================
-- Disable RLS for users table (since we handle auth in backend)
ALTER TABLE users DISABLE ROW LEVEL SECURITY;

-- OR if you want to keep RLS enabled, use these policies instead:
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "Allow all operations" ON users FOR ALL USING (true) WITH CHECK (true);

-- ====================================
-- Storage Bucket Setup
-- ====================================
-- Note: Create this bucket manually in Supabase Dashboard
-- 1. Go to Storage section
-- 2. Create new bucket called "profile_images"
-- 3. Set it to PUBLIC
-- 4. Add the following policy:

-- Storage Policy (run in SQL editor or set via Dashboard):
-- Allow public read access
-- CREATE POLICY "Public Access" ON storage.objects FOR SELECT USING (bucket_id = 'profile_images');

-- Allow authenticated insert
-- CREATE POLICY "Allow Uploads" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'profile_images');

-- ====================================
-- Sample Query to verify setup
-- ====================================
-- SELECT * FROM users LIMIT 10;

-- ====================================
-- Drop table if needed (BE CAREFUL!)
-- ====================================
-- DROP TABLE IF EXISTS users;

