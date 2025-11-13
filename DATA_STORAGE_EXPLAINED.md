# DataLix AI - Data Storage Architecture

## Overview

DataLix AI uses a **hybrid storage architecture** that combines two different storage systems, each optimized for specific types of data:

1. **PostgreSQL Database** - For persistent user data and metadata
2. **In-Memory Python Sessions** - For active dataset analysis

## Why Two Storage Systems?

### The Problem
When analyzing datasets, you need:
- **Fast access** to perform calculations, transformations, and AI operations
- **Persistent storage** for user accounts, chat history, and session metadata
- **Temporary storage** that doesn't clutter your database with large datasets

### The Solution
We separate concerns by storing different types of data in different places:

---

## 1. PostgreSQL Database Storage

### What's Stored Here?
- **User accounts** (email, username, hashed passwords)
- **Session metadata** (session IDs, creation dates, user ownership)
- **Chat message history** (conversation text, timestamps, AI responses)
- **Embedded results** (chart configurations, data previews, function calls)

### Why PostgreSQL?
✅ **Persistent** - Data survives server restarts  
✅ **Searchable** - Query your past conversations  
✅ **Secure** - Passwords are hashed with bcrypt  
✅ **Relational** - Connect users → sessions → messages  
✅ **Rollback support** - Integrated with Replit's database features  

### Database Schema
```
users
├─ id (UUID)
├─ email
├─ username
└─ password_hash

sessions
├─ id (UUID)
├─ user_id → users.id
├─ created_at
├─ dataset_name
└─ quality_score

messages
├─ id (UUID)
├─ session_id → sessions.id
├─ role (user/assistant)
├─ content (text)
├─ chart_data (JSONB)
├─ data_preview (JSONB)
└─ timestamp
```

### What This Means for You
- Your **account information** is always safe
- Your **conversation history** is saved and searchable
- You can **close the app** and come back later to see your past analyses
- **Multiple users** can use the system simultaneously without conflicts

---

## 2. In-Memory Python Session Storage

### What's Stored Here?
- **Full datasets** (pandas DataFrames with all your data)
- **Active transformations** (cleaned data, engineered features)
- **Calculation results** (statistics, correlations, ML models)
- **Temporary files** (for exports and processing)

### Why In-Memory?
✅ **Lightning fast** - No database queries needed for calculations  
✅ **Pandas native** - Direct access to all pandas/scikit-learn operations  
✅ **No storage limits** - Database doesn't get bloated with large datasets  
✅ **Automatic cleanup** - Old sessions are garbage collected  

### Data Structure
```python
DataProcessor.sessions = {
    "session_abc123": {
        "user_id": "user_xyz",
        "dataset": pandas.DataFrame(...),  # Your actual data
        "metadata": {
            "filename": "sales.csv",
            "rows": 10000,
            "columns": 15,
            "upload_time": datetime(...)
        },
        "quality_metrics": {...},
        "transformations": [...]
    }
}
```

### What This Means for You
- **Upload a file** → It's loaded into Python's memory instantly
- **Run analysis** → Calculations happen at pandas speed
- **Server restarts** → Active datasets are lost (but metadata remains in database)
- **Large files** → No database bloat, just Python memory usage

---

## Data Flow Example

Let's walk through what happens when you upload and analyze a dataset:

### Step 1: Upload
```
You: Upload "sales.csv" (500 MB)
↓
Python Backend: 
  ✓ Read file with pandas
  ✓ Generate session_id: "abc123"
  ✓ Store DataFrame in memory
  ✓ Calculate quality score: 87/100
  ✓ Save session metadata to PostgreSQL
    → sessions table: {id: "abc123", user_id: "you", dataset_name: "sales.csv"}
  ✓ Save initial AI message to PostgreSQL
    → messages table: {content: "Dataset loaded...", data_preview: {...}}
```

### Step 2: Analysis
```
You: "Show correlation matrix"
↓
Python Backend:
  ✓ Lookup session "abc123" in memory (fast!)
  ✓ Calculate correlation on DataFrame
  ✓ Generate Plotly chart JSON
  ✓ Save AI response to PostgreSQL
    → messages table: {content: "Here's your correlation...", chart_data: {...}}
```

### Step 3: Transformation
```
You: "Remove outliers from price column"
↓
Python Backend:
  ✓ Modify DataFrame in memory
  ✓ Update session.dataset with cleaned data
  ✓ Calculate new quality score
  ✓ Save transformation result to PostgreSQL
    → messages table: {content: "Removed 23 outliers...", data_preview: {...}}
```

### Step 4: Export
```
You: "Export as CSV"
↓
Python Backend:
  ✓ Get DataFrame from memory session
  ✓ Write to temporary file
  ✓ Send file download to browser
  ✓ (File gets deleted after download)
```

---

## Important Behaviors

### ✅ Persistent (Survives Restarts)
- Your login credentials
- All chat conversations
- Session history (names, dates, quality scores)
- Chart configurations and previews

### ❌ Temporary (Lost on Restart)
- The actual dataset (full DataFrame)
- In-progress transformations not yet saved
- Calculated statistics cached in memory
- ML models and clustering results

### 💡 Best Practices

**For Long Analysis Sessions:**
1. Upload your dataset
2. Perform all your analysis and transformations
3. **Export the cleaned dataset** before closing
4. Your chat history will show what you did
5. Next time, re-upload the cleaned version

**For Quick Queries:**
1. Upload dataset
2. Ask questions, get insights
3. Download any charts you need
4. No need to save - conversation is already stored

**For Production Use:**
If you need datasets to persist across restarts, you can:
- Use Supabase Storage (integrated with Replit)
- Connect to external S3/GCS buckets
- Store datasets in PostgreSQL (for smaller files <10MB)

---

## Storage Limits

### PostgreSQL Database
- **Messages/Chat**: Virtually unlimited (text is compressed)
- **Chart data**: JSONB columns handle complex visualizations
- **Users/Sessions**: No practical limit

### In-Memory Python
- **Dataset size**: Limited by server RAM
- **Concurrent sessions**: Multiple users share memory pool
- **Session lifetime**: Active until server restart or explicit deletion

---

## Data Privacy & Security

### Database (PostgreSQL)
- ✅ Passwords hashed with bcrypt (never stored plain text)
- ✅ User data isolated by user_id foreign keys
- ✅ Sessions belong to specific users (no cross-user access)
- ✅ Managed by Replit's secure database service

### In-Memory (Python)
- ✅ Sessions isolated by session_id
- ✅ Authentication required for all operations
- ✅ Automatic cleanup of old sessions
- ⚠️ No encryption at rest (data in RAM)
- ⚠️ Lost on server restart

---

## Supabase Integration

When Supabase is configured (via environment variables), the authentication system uses:

- **Supabase Auth** for user management and JWT tokens
- **PostgreSQL** for session and message storage (as before)
- **In-Memory** for dataset storage (as before)

This gives you:
- Professional authentication with email verification
- Secure JWT token management
- Password reset capabilities
- OAuth integration options (Google, GitHub, etc.)

---

## Summary Table

| Data Type | Storage Location | Persistent? | Speed | Size Limit |
|-----------|-----------------|-------------|-------|------------|
| User accounts | PostgreSQL | ✅ Yes | Normal | Unlimited |
| Chat history | PostgreSQL | ✅ Yes | Normal | Unlimited |
| Session metadata | PostgreSQL | ✅ Yes | Normal | Unlimited |
| Full datasets | Python Memory | ❌ No | ⚡ Fast | RAM limit |
| Transformations | Python Memory | ❌ No | ⚡ Fast | RAM limit |
| Calculations | Python Memory | ❌ No | ⚡ Fast | RAM limit |

---

## Questions & Answers

**Q: What happens if the server restarts?**  
A: Your account, chat history, and session list remain intact. However, you'll need to re-upload datasets to continue analysis.

**Q: Can I access my old analyses?**  
A: Yes! Your chat history shows all past conversations, visualizations, and insights. You just need to re-upload the dataset to perform new operations.

**Q: Why not store everything in the database?**  
A: Databases are optimized for queries, not high-speed numerical calculations. Pandas operations on 1M rows in memory are 100x faster than database operations.

**Q: Is my data safe?**  
A: Yes. User authentication is secure (bcrypt hashing), and session access is protected by JWT tokens. Datasets in memory are isolated by session ID.

**Q: How long are datasets kept in memory?**  
A: Until the server restarts or the session is explicitly deleted. We recommend exporting important results.

---

## Future Enhancements

Planned improvements to the storage architecture:

1. **Redis caching** - For faster session lookups
2. **S3 integration** - Optional persistent dataset storage
3. **Automatic backups** - Periodic exports to cloud storage
4. **Session resurrection** - Auto-reload last dataset on login
5. **Collaborative sessions** - Share datasets with team members

---

*Last updated: 2025-11-11*
