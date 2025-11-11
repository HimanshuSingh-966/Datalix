# DataLix 2.0 Database Schema

This document describes the complete database schema for DataLix 2.0, an AI-powered data analysis platform.

## Overview

The application uses PostgreSQL as its primary database with three main tables:
- `users` - User authentication and profiles
- `sessions` - Data analysis sessions
- `messages` - Chat messages and analysis results

---

## Table: `users`

Stores user authentication information and profiles.

### SQL Schema

```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,  -- Bcrypt hashed password
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

### Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique user identifier (UUID) |
| username | TEXT | NOT NULL, UNIQUE | User's unique username |
| email | TEXT | NOT NULL, UNIQUE | User's email address |
| password | TEXT | NOT NULL | Bcrypt hashed password |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |

### Notes
- Passwords are hashed using bcrypt before storage (never stored in plain text)
- Both username and email must be unique across all users
- The application supports both Supabase authentication and local authentication

---

## Table: `sessions`

Stores data analysis sessions for each user.

### SQL Schema

```sql
CREATE TABLE sessions (
    id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_updated_at ON sessions(updated_at DESC);

-- Trigger to update updated_at
CREATE OR REPLACE FUNCTION update_sessions_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER sessions_updated_at_trigger
    BEFORE UPDATE ON sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_sessions_updated_at();
```

### Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique session identifier (UUID) |
| user_id | VARCHAR | NOT NULL, FOREIGN KEY → users(id) | Owner of the session |
| name | TEXT | NULL | Optional session name/title |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Session creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

### Notes
- Each session belongs to exactly one user
- Sessions are automatically deleted when the user is deleted (CASCADE)
- The `updated_at` field is automatically updated on any modification
- A session represents one data analysis workflow (dataset + all interactions)

---

## Table: `messages`

Stores chat messages and AI analysis results within sessions.

### SQL Schema

```sql
CREATE TABLE messages (
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

-- Indexes
CREATE INDEX idx_messages_session_id ON messages(session_id);
CREATE INDEX idx_messages_created_at ON messages(created_at DESC);
CREATE INDEX idx_messages_role ON messages(role);

-- JSONB indexes for better query performance
CREATE INDEX idx_messages_chart_data ON messages USING GIN (chart_data);
CREATE INDEX idx_messages_data_preview ON messages USING GIN (data_preview);
```

### Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique message identifier (UUID) |
| session_id | VARCHAR | NOT NULL, FOREIGN KEY → sessions(id) | Parent session |
| role | TEXT | NOT NULL, CHECK IN ('user', 'assistant') | Message sender ('user' or 'assistant') |
| content | TEXT | NOT NULL | Message text content |
| chart_data | JSONB | NULL | Plotly chart data (JSON) |
| data_preview | JSONB | NULL | Data table preview (JSON) |
| suggested_actions | JSONB | NULL | AI-suggested next actions (JSON array) |
| function_calls | JSONB | NULL | AI function calls executed (JSON array) |
| error | TEXT | NULL | Error message if processing failed |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Message timestamp |

### JSONB Column Structures

#### `chart_data` Structure
```json
{
  "data": [...],      // Plotly data traces
  "layout": {...},    // Plotly layout configuration
  "config": {...}     // Plotly config options
}
```

#### `data_preview` Structure
```json
{
  "columns": [
    {
      "name": "column_name",
      "type": "int64",
      "nullCount": 0,
      "uniqueCount": 100,
      "sampleValues": [1, 2, 3]
    }
  ],
  "rows": [
    {"col1": "value1", "col2": "value2"}
  ],
  "totalRows": 1000,
  "totalColumns": 5,
  "fileName": "data.csv"
}
```

#### `suggested_actions` Structure
```json
[
  {
    "label": "View Statistics",
    "prompt": "Show me descriptive statistics for all columns",
    "icon": "trending-up"
  }
]
```

#### `function_calls` Structure
```json
[
  "upload_data",
  "get_statistics",
  "create_visualization"
]
```

### Notes
- Messages are automatically deleted when the session is deleted (CASCADE)
- The `role` field is constrained to only allow 'user' or 'assistant'
- JSONB columns use GIN indexes for efficient querying
- AI responses (role='assistant') can include charts, data previews, and suggested actions
- The `error` field is only populated if the AI processing failed

---

## Relationships

```
users (1) ──< (many) sessions
sessions (1) ──< (many) messages
```

- One user can have many sessions
- One session can have many messages
- Deleting a user cascades to delete all their sessions and messages
- Deleting a session cascades to delete all its messages

---

## Migration Commands

### Using Drizzle ORM (TypeScript)

```bash
# Generate migration
npm run db:generate

# Run migration
npm run db:migrate

# Studio (database GUI)
npm run db:studio
```

### Direct SQL

```sql
-- Create all tables in order
CREATE TABLE users (...);
CREATE TABLE sessions (...);
CREATE TABLE messages (...);

-- Create indexes
CREATE INDEX ...;

-- Create triggers
CREATE TRIGGER ...;
```

---

## Environment Variables

Required environment variables for database connection:

```bash
# PostgreSQL Database
DATABASE_URL=postgresql://user:password@host:port/database

# OR for Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

---

## Authentication Modes

The application supports two authentication modes:

### 1. Supabase Authentication (Production)
- Uses Supabase Auth service
- Automatic user management
- JWT tokens for session management
- Set `SUPABASE_URL` and `SUPABASE_ANON_KEY`

### 2. Local Authentication (Development)
- In-memory user storage
- Bcrypt password hashing
- JWT tokens for session management
- No environment variables needed

---

## Data Storage Strategy

### Session Data (In-Memory)
- Uploaded datasets are stored in-memory per session
- Not persisted to database (for performance)
- Lost on server restart
- Session metadata is persisted in `sessions` table

### Chat History (Database)
- All chat messages are persisted
- Includes AI responses with charts and data previews
- Enables session history and replay
- JSONB columns for flexible data structures

---

## Security Considerations

1. **Password Storage**: Always use bcrypt hashing (never plain text)
2. **SQL Injection**: Use parameterized queries (Drizzle ORM handles this)
3. **Authentication**: JWT tokens with expiration
4. **Authorization**: Users can only access their own sessions/messages
5. **Data Validation**: All inputs validated with Zod schemas
6. **HTTPS**: Required for production (handles by Replit deployment)

---

## Performance Optimization

1. **Indexes**: All foreign keys and frequently queried columns are indexed
2. **JSONB GIN Indexes**: Enable fast queries on JSON data
3. **Cascading Deletes**: Automatic cleanup of related records
4. **Connection Pooling**: Managed by Drizzle ORM
5. **In-Memory Dataset Storage**: Avoids database overhead for large datasets

---

## Backup and Recovery

### Database Backup
```bash
# PostgreSQL dump
pg_dump -h host -U user -d database > backup.sql

# Restore
psql -h host -U user -d database < backup.sql
```

### Supabase Backup
- Automatic daily backups (Pro plan)
- Point-in-time recovery available
- Manual backups via Supabase dashboard

---

## Example Queries

### Get user's recent sessions
```sql
SELECT s.*, COUNT(m.id) as message_count
FROM sessions s
LEFT JOIN messages m ON m.session_id = s.id
WHERE s.user_id = 'user-uuid'
GROUP BY s.id
ORDER BY s.updated_at DESC
LIMIT 10;
```

### Get session chat history with charts
```sql
SELECT 
    id,
    role,
    content,
    chart_data,
    data_preview,
    suggested_actions,
    created_at
FROM messages
WHERE session_id = 'session-uuid'
ORDER BY created_at ASC;
```

### Find sessions with errors
```sql
SELECT DISTINCT s.*
FROM sessions s
INNER JOIN messages m ON m.session_id = s.id
WHERE m.error IS NOT NULL
ORDER BY s.updated_at DESC;
```

---

## TypeScript Types

The schema definitions are available in `shared/schema.ts`:

```typescript
import type { InsertUser, User } from '@shared/schema';
import type { InsertSession, Session } from '@shared/schema';
import type { InsertMessage, Message } from '@shared/schema';
```

For runtime data structures:
```typescript
import type { 
  ChatMessage, 
  DataPreview, 
  PlotlyChartData,
  SuggestedAction 
} from '@shared/schema';
```

---

## Additional Resources

- **Drizzle ORM Docs**: https://orm.drizzle.team/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Supabase Docs**: https://supabase.com/docs
