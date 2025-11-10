import { 
  type User, 
  type InsertUser,
  type Session,
  type InsertSession,
  type Message,
  type InsertMessage,
  type DataPreview,
  type DataQuality,
  type UploadResponse,
} from "@shared/schema";
import { randomUUID } from "crypto";

// In-memory storage for sessions and datasets
export interface SessionData {
  sessionId: string;
  userId: string;
  dataset: any; // pandas DataFrame equivalent (will be stored as JSON-serializable object)
  dataPreview: DataPreview | null;
  qualityScore: DataQuality | null;
  metadata: {
    fileName?: string;
    uploadedAt: Date;
    rowCount: number;
    columnCount: number;
  };
}

export interface IStorage {
  // User management
  getUser(id: string): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  
  // Session management
  createSession(session: InsertSession): Promise<Session>;
  getSession(id: string): Promise<Session | undefined>;
  getUserSessions(userId: string): Promise<Session[]>;
  deleteSession(id: string): Promise<void>;
  
  // Message management
  createMessage(message: InsertMessage): Promise<Message>;
  getSessionMessages(sessionId: string): Promise<Message[]>;
  
  // Dataset storage
  storeDataset(sessionId: string, data: any, preview: DataPreview, quality: DataQuality, metadata: any): Promise<void>;
  getDataset(sessionId: string): Promise<SessionData | undefined>;
  updateDataset(sessionId: string, data: any, preview: DataPreview): Promise<void>;
}

export class MemStorage implements IStorage {
  private users: Map<string, User>;
  private sessions: Map<string, Session>;
  private messages: Map<string, Message[]>;
  private datasets: Map<string, SessionData>;

  constructor() {
    this.users = new Map();
    this.sessions = new Map();
    this.messages = new Map();
    this.datasets = new Map();
  }

  // User management
  async getUser(id: string): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username === username,
    );
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = randomUUID();
    const createdAt = new Date();
    const user: User = { ...insertUser, id, createdAt };
    this.users.set(id, user);
    return user;
  }

  // Session management
  async createSession(insertSession: InsertSession): Promise<Session> {
    const id = randomUUID();
    const now = new Date();
    const session: Session = { 
      ...insertSession, 
      id, 
      createdAt: now,
      updatedAt: now,
    };
    this.sessions.set(id, session);
    this.messages.set(id, []);
    return session;
  }

  async getSession(id: string): Promise<Session | undefined> {
    return this.sessions.get(id);
  }

  async getUserSessions(userId: string): Promise<Session[]> {
    return Array.from(this.sessions.values())
      .filter(session => session.userId === userId)
      .sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime());
  }

  async deleteSession(id: string): Promise<void> {
    this.sessions.delete(id);
    this.messages.delete(id);
    this.datasets.delete(id);
  }

  // Message management
  async createMessage(insertMessage: InsertMessage): Promise<Message> {
    const id = randomUUID();
    const createdAt = new Date();
    const message: Message = { ...insertMessage, id, createdAt };
    
    const sessionMessages = this.messages.get(insertMessage.sessionId) || [];
    sessionMessages.push(message);
    this.messages.set(insertMessage.sessionId, sessionMessages);
    
    return message;
  }

  async getSessionMessages(sessionId: string): Promise<Message[]> {
    return this.messages.get(sessionId) || [];
  }

  // Dataset storage
  async storeDataset(
    sessionId: string, 
    data: any, 
    preview: DataPreview, 
    quality: DataQuality,
    metadata: any
  ): Promise<void> {
    const sessionData: SessionData = {
      sessionId,
      userId: '', // Will be set from session
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

export const storage = new MemStorage();
