# DataLix AI

![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Node](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)

**DataLix AI** is a conversational data analysis platform that democratizes data science through natural language chat. Upload datasets, receive automated quality assessments, perform analysis through AI-powered chat, and view interactive visualizations—all without requiring SQL, Python, or Excel expertise.

## 🌟 Key Features

### 💬 Natural Language Data Analysis
- Chat with your data using plain English
- Multi-provider AI support (Google Gemini & Groq)
- Context-aware conversation with memory
- Automated suggested actions for next steps

### 📊 Automated Data Quality Scoring
- Instant quality assessment on upload
- Detailed breakdown by category:
  - Completeness (missing values)
  - Validity (data types, ranges)
  - Consistency (duplicates, patterns)
  - Accuracy (outliers, anomalies)
- Actionable improvement recommendations

### 📈 Rich Interactive Visualizations
- Dynamic Plotly charts (bar, line, scatter, heatmap, box plots)
- Data preview tables with sorting
- Statistical summaries
- Export-ready visualizations

### 💾 Session Persistence
- Resume conversations anytime
- Full chat history with all visualizations
- Switch between multiple analysis sessions
- Automatic session management

### 📁 Multi-Format File Support
- CSV files
- Excel (.xlsx, .xls)
- JSON datasets
- Parquet files

### 🎨 Modern User Interface
- Clean, intuitive chat interface
- Dark mode optimized
- Responsive design
- Real-time typing indicators
- Keyboard shortcuts

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Supabase account (for database)
- At least one AI provider API key:
  - Google Gemini API key, OR
  - Groq API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/datalix-ai.git
   cd datalix-ai
   ```

2. **Install dependencies**
   ```bash
   # Install Node.js dependencies
   npm install

   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # Supabase Configuration
   SUPABASE_URL=your-supabase-project-url
   SUPABASE_ANON_KEY=your-supabase-anon-key
   SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
   DATABASE_URL=your-postgres-connection-string

   # AI Provider (at least one required)
   GEMINI_API_KEY=your-gemini-api-key
   GROQ_API_KEY=your-groq-api-key

   # Frontend Configuration
   VITE_SUPABASE_URL=your-supabase-project-url
   VITE_SUPABASE_ANON_KEY=your-supabase-anon-key

   # Server Configuration
   NODE_ENV=development
   PORT=5000
   ```

4. **Initialize the database**
   
   Run the SQL script in your Supabase SQL editor:
   ```bash
   # Use the init_database_with_rls.sql file
   ```

5. **Start the application**
   ```bash
   npm run dev
   ```

6. **Access the application**
   
   Open your browser to `http://localhost:5000`

## 📖 Usage Guide

### Getting Started

1. **Create an account** - Sign up with email and password
2. **Upload a dataset** - Click "Upload Data" and select your file
3. **Review quality score** - See automated assessment and recommendations
4. **Start chatting** - Ask questions in natural language:
   - "Show me a summary of the data"
   - "What are the top 5 cities by sales?"
   - "Create a bar chart of revenue by month"
   - "Find correlations between columns"
   - "Clean this dataset"

### Example Questions

**Data Exploration:**
- "What columns are in this dataset?"
- "Show me the first 10 rows"
- "What's the distribution of age?"

**Statistical Analysis:**
- "Calculate mean, median, and mode for all numeric columns"
- "Show correlation matrix"
- "Find outliers in the price column"

**Visualization:**
- "Create a scatter plot of x vs y"
- "Show a bar chart of category counts"
- "Generate a heatmap of correlations"

**Data Cleaning:**
- "Remove duplicate rows"
- "Fill missing values in column X"
- "Identify and handle outliers"

### Session Management

- **New Session** - Start fresh analysis (coming soon)
- **Switch Sessions** - Resume previous analyses
- **Delete Session** - Remove old conversations

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- React 18 with TypeScript
- Wouter for routing
- TanStack Query for data fetching
- Shadcn UI components
- Tailwind CSS for styling
- Plotly.js for charts

**Backend:**
- Node.js with Express
- FastAPI (Python) for data processing
- Supabase (PostgreSQL) for database
- Session-based authentication

**AI Integration:**
- Google Gemini API
- Groq API
- Function calling for data operations

**Data Processing:**
- Pandas for data manipulation
- NumPy for numerical operations
- Scikit-learn for ML features
- Plotly for visualization generation

### Project Structure

```
datalix-ai/
├── client/               # React frontend
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/       # Route pages
│   │   ├── lib/         # Utilities
│   │   └── hooks/       # Custom hooks
├── server/              # Express backend
│   ├── routes.ts        # API endpoints
│   ├── storage.ts       # Data storage interface
│   └── index.ts         # Server entry
├── python_backend/      # FastAPI service
│   ├── main.py          # FastAPI app
│   ├── data_processor.py # Data analysis
│   ├── ai_chat.py       # AI integration
│   └── auth.py          # Authentication
├── shared/              # Shared TypeScript types
│   └── schema.ts        # Data models
└── supabase_migrations/ # Database migrations
```

## 🔧 Configuration

### AI Provider Configuration

**Google Gemini:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add to `.env`: `GEMINI_API_KEY=your-key`

**Groq:**
1. Visit [Groq Console](https://console.groq.com)
2. Generate an API key
3. Add to `.env`: `GROQ_API_KEY=your-key`

### Supabase Setup

1. Create a project at [Supabase](https://supabase.com)
2. Get credentials from Project Settings → API
3. Run `init_database_with_rls.sql` in SQL Editor
4. Add credentials to `.env`

### Environment Variables

See `.env.example` for all available configuration options.

## 🚀 Deployment

### Deploy to Render

See [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy:**
1. Push code to GitHub
2. Create two Render services (Web + Python Backend)
3. Configure environment variables
4. Deploy

### Deploy to Other Platforms

**Vercel/Netlify (Frontend):**
- Build command: `npm run build`
- Output directory: `dist`
- Node version: 18+

**Railway/Fly.io (Backend):**
- Supports both Node.js and Python services
- Use provided Dockerfiles

## 🔐 Security

- Row-level security (RLS) enabled on all tables
- Secure session management
- API key encryption
- CORS protection
- Input validation and sanitization

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Bug Reports & Feature Requests

Please use the [GitHub Issues](https://github.com/yourusername/datalix-ai/issues) page to report bugs or request features.

## 📚 Documentation

- [Full Documentation](./DOCUMENTATION.md)
- [Deployment Guide](./RENDER_DEPLOYMENT.md)
- [Changelog](./CHANGELOG_v3.0.0.md)

## 🙏 Acknowledgments

- Built with [Replit](https://replit.com)
- UI components from [Shadcn UI](https://ui.shadcn.com)
- Charts powered by [Plotly](https://plotly.com)
- Database by [Supabase](https://supabase.com)
- AI by [Google Gemini](https://deepmind.google/technologies/gemini/) and [Groq](https://groq.com)

## 📧 Contact

For questions or support, please open an issue or contact the maintainers.

---

**Made with ❤️ for data enthusiasts everywhere**
