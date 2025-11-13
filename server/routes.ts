import type { Express, Request, Response, NextFunction } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { insertSessionSchema, insertMessageSchema } from "@shared/schema";

const DAILY_MESSAGE_LIMIT = 10;

interface AuthRequest extends Request {
  userId?: string;
}

async function getUserFromAuth(req: Request): Promise<string | null> {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    return null;
  }
  
  const token = authHeader.substring(7);
  
  try {
    const response = await fetch('http://localhost:8001/api/auth/verify', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      return null;
    }
    
    const userData = await response.json();
    return userData.id;
  } catch (error) {
    console.error('Token verification error:', error);
    return null;
  }
}

async function checkRateLimit(req: AuthRequest, res: Response, next: NextFunction) {
  try {
    const userId = req.userId;
    if (!userId) {
      return res.status(401).json({ error: 'Not authenticated' });
    }

    const user = await storage.getUser(userId);
    if (!user) {
      return res.status(401).json({ error: 'User not found' });
    }

    if (user.isMaster === 1) {
      return next();
    }

    const messageCount = await storage.getUserMessageCountToday(userId);
    
    if (messageCount >= DAILY_MESSAGE_LIMIT) {
      return res.status(429).json({ 
        error: 'Daily message limit reached (10/10). Limit resets at midnight.',
        limit: DAILY_MESSAGE_LIMIT,
        current: messageCount
      });
    }

    next();
  } catch (error) {
    console.error('Rate limit check error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}

export async function registerRoutes(app: Express, httpServer: Server): Promise<void> {
  app.get('/api/sessions', async (req: Request, res: Response) => {
    try {
      const userId = await getUserFromAuth(req);
      if (!userId) {
        return res.status(401).json({ error: 'Not authenticated' });
      }

      const sessions = await storage.getUserSessions(userId);
      res.json(sessions);
    } catch (error) {
      console.error('Error fetching sessions:', error);
      res.status(500).json({ error: 'Failed to fetch sessions' });
    }
  });

  app.post('/api/sessions', async (req: Request, res: Response) => {
    try {
      const userId = await getUserFromAuth(req);
      if (!userId) {
        return res.status(401).json({ error: 'Not authenticated' });
      }

      const validatedData = insertSessionSchema.parse({
        userId,
        name: req.body.name || null
      });

      const session = await storage.createSession(validatedData);
      res.json(session);
    } catch (error) {
      console.error('Error creating session:', error);
      res.status(500).json({ error: 'Failed to create session' });
    }
  });

  app.delete('/api/sessions/:id', async (req: Request, res: Response) => {
    try {
      const userId = await getUserFromAuth(req);
      if (!userId) {
        return res.status(401).json({ error: 'Not authenticated' });
      }

      const session = await storage.getSession(req.params.id);
      if (!session) {
        return res.status(404).json({ error: 'Session not found' });
      }

      if (session.userId !== userId) {
        return res.status(403).json({ error: 'Not authorized' });
      }

      await storage.deleteSession(req.params.id);
      res.json({ success: true });
    } catch (error) {
      console.error('Error deleting session:', error);
      res.status(500).json({ error: 'Failed to delete session' });
    }
  });

  app.patch('/api/sessions/:id/name', async (req: Request, res: Response) => {
    try {
      const userId = await getUserFromAuth(req);
      if (!userId) {
        return res.status(401).json({ error: 'Not authenticated' });
      }

      const session = await storage.getSession(req.params.id);
      if (!session) {
        return res.status(404).json({ error: 'Session not found' });
      }

      if (session.userId !== userId) {
        return res.status(403).json({ error: 'Not authorized' });
      }

      await storage.updateSessionName(req.params.id, req.body.name);
      res.json({ success: true });
    } catch (error) {
      console.error('Error updating session name:', error);
      res.status(500).json({ error: 'Failed to update session name' });
    }
  });

  app.get('/api/sessions/:id/messages', async (req: Request, res: Response) => {
    try {
      const userId = await getUserFromAuth(req);
      if (!userId) {
        return res.status(401).json({ error: 'Not authenticated' });
      }

      const session = await storage.getSession(req.params.id);
      if (!session) {
        return res.status(404).json({ error: 'Session not found' });
      }

      if (session.userId !== userId) {
        return res.status(403).json({ error: 'Not authorized' });
      }

      const messages = await storage.getSessionMessages(req.params.id);
      res.json(messages);
    } catch (error) {
      console.error('Error fetching messages:', error);
      res.status(500).json({ error: 'Failed to fetch messages' });
    }
  });

  app.get('/api/user/message-limit', async (req: Request, res: Response) => {
    try {
      const userId = await getUserFromAuth(req);
      if (!userId) {
        return res.status(401).json({ error: 'Not authenticated' });
      }

      const user = await storage.getUser(userId);
      if (!user) {
        return res.status(401).json({ error: 'User not found' });
      }

      const messageCount = await storage.getUserMessageCountToday(userId);
      const isMaster = user.isMaster === 1;

      res.json({
        limit: isMaster ? -1 : DAILY_MESSAGE_LIMIT,
        current: messageCount,
        remaining: isMaster ? -1 : Math.max(0, DAILY_MESSAGE_LIMIT - messageCount),
        isMaster
      });
    } catch (error) {
      console.error('Error fetching message limit:', error);
      res.status(500).json({ error: 'Failed to fetch message limit' });
    }
  });

}
