import postgres from 'postgres';
import type {
  User,
  InsertUser,
  Session,
  InsertSession,
  Message,
  InsertMessage,
} from '@shared/schema';
import type { IStorage, SessionData } from './storage';
import type { DataPreview, DataQuality } from '@shared/schema';

export class SupabaseStorage implements IStorage {
  private sql: postgres.Sql;
  private datasets: Map<string, SessionData>;

  constructor(connectionString: string) {
    this.sql = postgres(connectionString);
    this.datasets = new Map();
  }

  async getUser(id: string): Promise<User | undefined> {
    const result = await this.sql`
      SELECT * FROM profiles WHERE id = ${id} LIMIT 1
    `;
    return result[0] as User | undefined;
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    const result = await this.sql`
      SELECT * FROM profiles WHERE username = ${username} LIMIT 1
    `;
    return result[0] as User | undefined;
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const result = await this.sql`
      INSERT INTO profiles (username, email)
      VALUES (${insertUser.username}, ${insertUser.email})
      RETURNING *
    `;
    return result[0] as User;
  }

  async updateUserMasterStatus(userId: string, isMaster: boolean): Promise<void> {
    await this.sql`
      UPDATE profiles 
      SET is_master = ${isMaster ? 1 : 0}
      WHERE id = ${userId}
    `;
  }

  async createSession(insertSession: InsertSession): Promise<Session> {
    const result = await this.sql`
      INSERT INTO sessions (user_id, name)
      VALUES (${insertSession.userId}, ${insertSession.name ?? null})
      RETURNING *
    `;
    return result[0] as Session;
  }

  async getSession(id: string): Promise<Session | undefined> {
    const result = await this.sql`
      SELECT * FROM sessions WHERE id = ${id} LIMIT 1
    `;
    return result[0] as Session | undefined;
  }

  async getUserSessions(userId: string): Promise<Session[]> {
    const result = await this.sql`
      SELECT * FROM sessions 
      WHERE user_id = ${userId}
      ORDER BY updated_at DESC
    `;
    return Array.from(result) as Session[];
  }

  async deleteSession(id: string): Promise<void> {
    await this.sql`
      DELETE FROM sessions WHERE id = ${id}
    `;
  }

  async updateSessionName(sessionId: string, name: string): Promise<void> {
    await this.sql`
      UPDATE sessions 
      SET name = ${name}, updated_at = NOW()
      WHERE id = ${sessionId}
    `;
  }

  async createMessage(insertMessage: InsertMessage): Promise<Message> {
    const result = await this.sql`
      INSERT INTO messages (
        session_id, role, content, chart_data, data_preview, 
        suggested_actions, function_calls, error
      )
      VALUES (
        ${insertMessage.sessionId}, 
        ${insertMessage.role}, 
        ${insertMessage.content},
        ${insertMessage.chartData ? this.sql.json(insertMessage.chartData) : null},
        ${insertMessage.dataPreview ? this.sql.json(insertMessage.dataPreview) : null},
        ${insertMessage.suggestedActions ? this.sql.json(insertMessage.suggestedActions) : null},
        ${insertMessage.functionCalls ? this.sql.json(insertMessage.functionCalls) : null},
        ${insertMessage.error ?? null}
      )
      RETURNING *
    `;
    
    await this.sql`
      UPDATE sessions 
      SET updated_at = NOW()
      WHERE id = ${insertMessage.sessionId}
    `;
    
    return result[0] as Message;
  }

  async getSessionMessages(sessionId: string): Promise<Message[]> {
    const result = await this.sql`
      SELECT * FROM messages 
      WHERE session_id = ${sessionId}
      ORDER BY created_at ASC
    `;
    return Array.from(result) as Message[];
  }

  async getUserMessageCountToday(userId: string): Promise<number> {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const result = await this.sql`
      SELECT COUNT(*) as count
      FROM messages m
      JOIN sessions s ON m.session_id = s.id
      WHERE s.user_id = ${userId}
        AND m.role = 'user'
        AND m.created_at >= ${today}
    `;
    
    return parseInt(result[0].count as string);
  }

  async storeDataset(
    sessionId: string,
    data: any,
    preview: DataPreview,
    quality: DataQuality,
    metadata: any
  ): Promise<void> {
    const sessionData: SessionData = {
      sessionId,
      userId: '',
      dataset: data,
      dataPreview: preview,
      qualityScore: quality,
      metadata,
    };
    this.datasets.set(sessionId, sessionData);
  }

  async getDataset(sessionId: string): Promise<SessionData | undefined> {
    return this.datasets.get(sessionId);
  }

  async updateDataset(sessionId: string, data: any, preview: DataPreview): Promise<void> {
    const existing = this.datasets.get(sessionId);
    if (existing) {
      existing.dataset = data;
      existing.dataPreview = preview;
      existing.metadata.rowCount = preview.totalRows;
      existing.metadata.columnCount = preview.totalColumns;
      this.datasets.set(sessionId, existing);
    }
  }
}
