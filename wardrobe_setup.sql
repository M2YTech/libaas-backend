-- ====================================
-- Wardrobe Items Table Setup
-- Run this SQL in Supabase SQL Editor
-- ====================================

-- Create wardrobe_items table
CREATE TABLE IF NOT EXISTS wardrobe_items (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL,
  name VARCHAR(200) NOT NULL,
  description TEXT,
  image_url TEXT NOT NULL,
  category VARCHAR(100) NOT NULL,
  sub_category VARCHAR(100),
  color VARCHAR(50),
  style VARCHAR(50),
  pattern VARCHAR(50),
  tags TEXT[],
  auto_categorized BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_wardrobe_user_id ON wardrobe_items(user_id);
CREATE INDEX IF NOT EXISTS idx_wardrobe_category ON wardrobe_items(category);
CREATE INDEX IF NOT EXISTS idx_wardrobe_created_at ON wardrobe_items(created_at DESC);

-- Disable RLS (since we handle auth in backend)
ALTER TABLE wardrobe_items DISABLE ROW LEVEL SECURITY;

-- ====================================
-- Storage Bucket for Wardrobe Images
-- ====================================
-- Create this bucket manually in Supabase Dashboard:
-- 1. Go to Storage section
-- 2. Create new bucket called "wardrobe_images"
-- 3. Set it to PUBLIC

-- ====================================
-- Sample Query to verify setup
-- ====================================
-- SELECT * FROM wardrobe_items WHERE user_id = 'your-user-id' ORDER BY created_at DESC;














