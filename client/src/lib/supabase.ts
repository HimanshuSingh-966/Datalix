import { createClient } from '@supabase/supabase-js';

let supabase: ReturnType<typeof createClient> | null = null;

async function initSupabase() {
  if (supabase) return supabase;

  try {
    const response = await fetch('/api/auth/config');
    const { supabaseUrl, supabaseAnonKey } = await response.json();
    
    if (!supabaseUrl || !supabaseAnonKey) {
      throw new Error('Supabase configuration not available');
    }

    supabase = createClient(supabaseUrl, supabaseAnonKey, {
      auth: {
        autoRefreshToken: true,
        persistSession: true,
        detectSessionInUrl: true,
      },
    });

    return supabase;
  } catch (error) {
    console.error('Failed to initialize Supabase:', error);
    throw error;
  }
}

export { initSupabase };
export const getSupabase = async () => {
  if (!supabase) {
    await initSupabase();
  }
  return supabase!;
};
