import express from "express";
import { createServer } from "http";
import { createProxyMiddleware } from "http-proxy-middleware";
import { spawn } from "child_process";

const app = express();

// Install Python dependencies and start backend
let pythonProcess: any = null;

console.log('Installing Python dependencies...');
const pipInstall = spawn('pip', ['install', '-r', 'requirements.txt'], {
  cwd: './python_backend',
  env: { ...process.env },
  stdio: 'inherit'
});

pipInstall.on('exit', (code) => {
  if (code !== 0) {
    console.error('Failed to install Python dependencies');
    return;
  }
  
  console.log('Starting Python backend...');
  pythonProcess = spawn('python', ['main.py'], {
    cwd: './python_backend',
    env: { ...process.env },
    stdio: 'inherit'
  });

  pythonProcess.on('error', (error: Error) => {
    console.error('Failed to start Python backend:', error);
  });

  pythonProcess.on('exit', (code: number) => {
    console.log(`Python backend exited with code ${code}`);
  });
});

process.on('exit', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
});

// Proxy /api requests to Python backend using http-proxy-middleware
app.use('/api', createProxyMiddleware({
  target: 'http://localhost:8000',
  changeOrigin: true,
  logLevel: 'debug',
  onProxyReq: (proxyReq, req) => {
    // Forward authorization headers
    if (req.headers.authorization) {
      proxyReq.setHeader('Authorization', req.headers.authorization);
    }
  },
  onError: (err, req, res) => {
    console.error('Proxy error:', err);
    res.writeHead(500, {
      'Content-Type': 'application/json',
    });
    res.end(JSON.stringify({
      error: 'Backend proxy error',
      message: err.message
    }));
  }
}));

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
  console.log(`Proxying /api requests to Python backend on http://localhost:8000`);
});
