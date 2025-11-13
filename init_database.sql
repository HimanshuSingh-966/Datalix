-- DataLix AI - Complete Database Schema
-- PostgreSQL Database Initialization Script
-- 
-- This script creates all necessary tables, indexes, triggers, and functions
-- for the AI-Powered Data Analysis Platform with master user support

-- =============================================================================
-- TABLE: users
-- Description: Stores user authentication information and profiles
-- =============================================================================

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,  -- Bcrypt hashed password (never plain text)
    is_master INTEGER NOT NULL DEFAULT 0,  -- Flag for master users (1 = master, 0 = regular)
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes for users table
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_is_master ON users(is_master);

-- Comments for users table
COMMENT ON TABLE users IS 'User authentication and profile information';
COMMENT ON COLUMN users.id IS 'Unique user identifier (UUID)';
COMMENT ON COLUMN users.username IS 'Unique username for login';
COMMENT ON COLUMN users.email IS 'Unique email address';
COMMENT ON COLUMN users.password IS 'Bcrypt hashed password';
COMMENT ON COLUMN users.is_master IS 'Flag indicating if user has unlimited message quota (1 = master, 0 = regular user)';
COMMENT ON COLUMN users.created_at IS 'Account creation timestamp';

-- =============================================================================
-- TABLE: sessions
-- Description: Stores data analysis sessions for each user
-- =============================================================================

CREATE TABLE IF NOT EXISTS sessions (
    id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes for sessions table
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_updated_at ON sessions(updated_at DESC);

-- Comments for sessions table
COMMENT ON TABLE sessions IS 'Data analysis sessions containing datasets and chat history';
COMMENT ON COLUMN sessions.id IS 'Unique session identifier (UUID)';
COMMENT ON COLUMN sessions.user_id IS 'Owner of the session (foreign key to users)';
COMMENT ON COLUMN sessions.name IS 'Optional session name/title';
COMMENT ON COLUMN sessions.created_at IS 'Session creation timestamp';
COMMENT ON COLUMN sessions.updated_at IS 'Last update timestamp (auto-updated)';

-- Trigger function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_sessions_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to execute the function on sessions update
DROP TRIGGER IF EXISTS sessions_updated_at_trigger ON sessions;
CREATE TRIGGER sessions_updated_at_trigger
    BEFORE UPDATE ON sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_sessions_updated_at();

-- =============================================================================
-- TABLE: messages
-- Description: Stores chat messages and AI analysis results within sessions
-- =============================================================================

CREATE TABLE IF NOT EXISTS messages (
    id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    chart_data JSONB,
    data_preview JSONB,
    suggested_actions JSONB,
    function_calls JSONB,
    error TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes for messages table
CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages(session_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_messages_role ON messages(role);

-- JSONB GIN indexes for better query performance on JSON data
CREATE INDEX IF NOT EXISTS idx_messages_chart_data ON messages USING GIN (chart_data);
CREATE INDEX IF NOT EXISTS idx_messages_data_preview ON messages USING GIN (data_preview);

-- Comments for messages table
COMMENT ON TABLE messages IS 'Chat messages and AI analysis results';
COMMENT ON COLUMN messages.id IS 'Unique message identifier (UUID)';
COMMENT ON COLUMN messages.session_id IS 'Parent session (foreign key to sessions)';
COMMENT ON COLUMN messages.role IS 'Message sender: user or assistant';
COMMENT ON COLUMN messages.content IS 'Message text content';
COMMENT ON COLUMN messages.chart_data IS 'Plotly chart data (JSON format)';
COMMENT ON COLUMN messages.data_preview IS 'Data table preview (JSON format)';
COMMENT ON COLUMN messages.suggested_actions IS 'AI-suggested next actions (JSON array)';
COMMENT ON COLUMN messages.function_calls IS 'AI function calls executed (JSON array)';
COMMENT ON COLUMN messages.error IS 'Error message if processing failed';
COMMENT ON COLUMN messages.created_at IS 'Message timestamp';

-- =============================================================================
-- MASTER USER SETUP
-- =============================================================================

-- To set a user as master (unlimited message quota), run:
-- UPDATE users SET is_master = 1 WHERE email = 'your-email@example.com';

-- To verify master user status:
-- SELECT id, email, username, is_master FROM users WHERE is_master = 1;

-- =============================================================================
-- USEFUL QUERIES
-- =============================================================================

-- Get all sessions for a user with message counts:
-- SELECT 
--     s.id,
--     s.name,
--     s.created_at,
--     s.updated_at,
--     COUNT(m.id) as message_count
-- FROM sessions s
-- LEFT JOIN messages m ON m.session_id = s.id
-- WHERE s.user_id = 'user-uuid-here'
-- GROUP BY s.id
-- ORDER BY s.updated_at DESC;

-- Get full chat history for a session:
-- SELECT 
--     id,
--     role,
--     content,
--     chart_data,
--     data_preview,
--     suggested_actions,
--     created_at
-- FROM messages
-- WHERE session_id = 'session-uuid-here'
-- ORDER BY created_at ASC;

-- Find sessions with errors:
-- SELECT DISTINCT s.*, m.error
-- FROM sessions s
-- INNER JOIN messages m ON m.session_id = s.id
-- WHERE m.error IS NOT NULL
-- ORDER BY s.updated_at DESC;

-- Get all master users:
-- SELECT id, email, username, created_at
-- FROM users
-- WHERE is_master = 1;

-- =============================================================================
-- CLEANUP QUERIES (USE WITH CAUTION)
-- =============================================================================

-- Delete old sessions (older than 90 days):
-- DELETE FROM sessions WHERE created_at < NOW() - INTERVAL '90 days';

-- Delete sessions with no messages:
-- DELETE FROM sessions WHERE id NOT IN (SELECT DISTINCT session_id FROM messages);

-- =============================================================================
-- DATABASE STATISTICS
-- =============================================================================

-- Get table sizes:
-- SELECT 
--     tablename,
--     pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
-- FROM pg_tables
-- WHERE schemaname = 'public'
-- ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Get row counts:
-- SELECT 
--     'users' as table_name, COUNT(*) as row_count FROM users
-- UNION ALL
-- SELECT 'sessions', COUNT(*) FROM sessions
-- UNION ALL
-- SELECT 'messages', COUNT(*) FROM messages;
