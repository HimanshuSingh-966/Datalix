import express, { type Request, Response, NextFunction } from "express";
import { createServer } from "http";
import { spawn } from "child_process";

const app = express();

// Start Python backend
const pythonProcess = spawn('python', ['main.py'], {
  cwd: './python_backend',
  env: { ...process.env },
  stdio: 'inherit'
});

pythonProcess.on('error', (error) => {
  console.error('Failed to start Python backend:', error);
});

process.on('exit', () => {
  pythonProcess.kill();
});

// Proxy API requests to Python backend
app.use('/api', async (req: Request, res: Response) => {
  const pythonUrl = `http://localhost:8000${req.url}`;
  
  try {
    const headers: HeadersInit = {};
    
    // Forward headers
    if (req.headers['authorization']) {
      headers['Authorization'] = req.headers['authorization'] as string;
    }
    if (req.headers['content-type']) {
      headers['Content-Type'] = req.headers['content-type'] as string;
    }
    
    const fetchOptions: RequestInit = {
      method: req.method,
      headers,
    };
    
    // Forward body for POST/PUT/PATCH
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      // Parse body
      let body = '';
      req.on('data', chunk => {
        body += chunk.toString();
      });
      
      await new Promise(resolve => {
        req.on('end', resolve);
      });
      
      if (body) {
        fetchOptions.body = body;
      }
    }
    
    const response = await fetch(pythonUrl, fetchOptions);
    
    // Forward response headers
    response.headers.forEach((value, key) => {
      res.setHeader(key, value);
    });
    
    res.status(response.status);
    
    // Handle different response types
    const contentType = response.headers.get('content-type');
    if (contentType?.includes('application/json')) {
      const data = await response.json();
      res.json(data);
    } else {
      const text = await response.text();
      res.send(text);
    }
  } catch (error) {
    console.error('Proxy error:', error);
    res.status(500).json({
      error: 'Failed to connect to backend',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

// Vite dev server setup
const { createServer: createViteServer } = await import("vite");
const vite = await createViteServer({
  server: {
    middlewareMode: true,
  },
  appType: "spa",
});

app.use(vite.middlewares);

const httpServer = createServer(app);

const PORT = Number(process.env.PORT) || 5000;
httpServer.listen(PORT, "0.0.0.0", () => {
  console.log(`Frontend server running on http://0.0.0.0:${PORT}`);
  console.log(`Python backend starting on http://localhost:8000`);
});
