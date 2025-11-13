# Database Migration Instructions

## Adding the is_master Column to Supabase

To enable master user functionality with unlimited messages, you need to add the `is_master` column to your Supabase users table.

### Step 1: Run the Migration Script

1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor** in the left sidebar
3. Click **New query**
4. Copy and paste the contents of `supabase_migrations/add_is_master_column.sql`
5. Click **Run** to execute the migration

### Step 2: Set Your User as Master

After running the migration, update your user account to have master privileges:

1. In the Supabase SQL Editor, run this query (replace with your email):

```sql
UPDATE public.users 
SET is_master = 1 
WHERE email = 'your-email@example.com';
```

2. Verify the update:

```sql
SELECT id, email, username, is_master 
FROM public.users 
WHERE email = 'your-email@example.com';
```

You should see `is_master` = 1 for your account.

### Step 3: Restart the Application

After making these changes, restart your application to apply the updates.

## What This Enables

Once you're set as a master user:
- **Unlimited Messages**: No daily message limit (regular users have 10 messages/day)
- **Master Badge**: Crown icon displayed in the UI showing "Unlimited" access
- **Full Access**: All features available without restrictions

## Regular Users

Regular users (is_master = 0) will have:
- Daily limit of 10 messages
- Message counter showing remaining messages
- Clear error message when limit is reached
- Automatic reset at midnight UTC
