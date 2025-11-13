-- Migration: Add is_master column to users table
-- This allows designating master users with unlimited message quotas

-- Add is_master column to the users table in the public schema
ALTER TABLE public.users 
ADD COLUMN IF NOT EXISTS is_master INTEGER NOT NULL DEFAULT 0;

-- Create an index on is_master for faster queries
CREATE INDEX IF NOT EXISTS idx_users_is_master ON public.users(is_master);

-- Add a comment to document the column
COMMENT ON COLUMN public.users.is_master IS 'Flag indicating if user has unlimited message quota (1 = master, 0 = regular user)';

-- Optional: Update a specific user to be master (replace with your actual user ID)
-- UPDATE public.users SET is_master = 1 WHERE email = 'your-email@example.com';
