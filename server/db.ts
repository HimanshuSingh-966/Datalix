// Database configuration for Supabase
export const DATABASE_URL = process.env.DATABASE_URL;

if (!DATABASE_URL) {
  console.warn('⚠️  DATABASE_URL not set. Session management will use in-memory storage.');
}
