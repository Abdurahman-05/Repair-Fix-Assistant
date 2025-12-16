import express, { Express, Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app: Express = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.get('/api/health', (req: Request, res: Response) => {
  res.status(200).json({ status: 'OK', message: 'Server is running' });
});

app.get('/api/hello', (req: Request, res: Response) => {
  const name = req.query.name || 'World';
  res.json({ message: `Hello, ${name}!` });
});

app.post('/api/data', (req: Request, res: Response) => {
  const { data } = req.body;
  res.status(201).json({ received: data, timestamp: new Date() });
});

// Error handling middleware
app.use((err: any, req: Request, res: Response, next: any) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
});

// 404 handler
app.use((req: Request, res: Response) => {
  res.status(404).json({ error: 'Route not found' });
});

app.listen(port, () => {
  console.log(`⚡ Server is running at http://localhost:${port}`);
});