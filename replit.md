# DataLix AI - AI-Powered Data Analysis Platform

## Overview

DataLix AI is a conversational AI platform for data analysis that allows users to upload datasets (CSV, Excel, JSON, Parquet) and interact with them using natural language. The application combines a React/TypeScript frontend with a Python FastAPI backend, leveraging AI providers (Gemini and Groq) to process user queries and perform data operations like cleaning, statistical analysis, visualization, and machine learning tasks.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack:**
- **Framework**: React with TypeScript, built using Vite
- **Routing**: Wouter (lightweight client-side routing)
- **State Management**: Zustand for global state (authentication, chat sessions, datasets)
- **UI Components**: Shadcn/ui with Radix UI primitives
- **Styling**: Tailwind CSS with custom design system
- **Data Fetching**: TanStack React Query

**Design System:**
- Typography: Inter for interface, JetBrains Mono for code/data
- Inspired by Linear's clean professionalism, ChatGPT's conversational interface, and Observable's data visualization clarity
- Custom color system supporting light/dark modes with HSL variables
- Component variants using class-variance-authority

**Key Components:**
- Chat interface with message bubbles supporting markdown rendering
- File upload with drag-and-drop (react-dropzone)
- Data preview tables with sorting capabilities
- Chart rendering using Plotly.js
- Quality score dashboard with metrics visualization
- Suggested actions as clickable prompts

**State Management Strategy:**
- `useAuthStore`: User authentication state, JWT token management
- `useChatStore`: Session management, messages, current dataset, quality scores, AI provider selection
- Local storage for token persistence

### Backend Architecture

**Primary Backend: Python FastAPI**
- RESTful API handling all data operations and AI interactions
- Modular architecture with separated concerns:
  - `main.py`: API routes and request handling
  - `data_processor.py`: Dataset upload, parsing, session management
  - `ai_service.py`: AI provider integration and function calling
  - `auth.py`: Authentication with bcrypt password hashing
  - Domain-specific modules: `data_cleaning.py`, `statistics_module.py`, `visualizations.py`, `ml_analysis.py`, `data_quality.py`

**Secondary Backend: Node.js/Express**
- Serves as proxy layer between frontend and Python backend
- Handles Vite development server in dev mode
- Production build serving
- Proxies `/api` requests to Python backend on port 8001

**AI Integration:**
- **Dual Provider Support**: Gemini (Google) and Groq with automatic fallback
- **Function Calling**: AI models can invoke specific operations (statistics, visualization, cleaning, ML analysis)
- **Conversational Context**: AI maintains awareness of current dataset and previous operations

**Data Processing Pipeline:**
1. File upload → Parse (pandas) → Validate
2. Data quality analysis (completeness, consistency, uniqueness, validity)
3. Store in-memory session with metadata
4. Generate data preview and initial quality metrics
5. AI responds with insights and suggested actions

**Python Libraries:**
- **Data**: pandas, numpy
- **ML/Stats**: scikit-learn (clustering, anomaly detection, PCA, feature importance)
- **Visualization**: plotly (generates JSON charts consumed by frontend)
- **AI**: google-generativeai, groq

### Data Storage Solutions

**Database: PostgreSQL with Drizzle ORM**
- Schema defined in TypeScript (`shared/schema.ts`)
- Three main tables:
  - `users`: Authentication (bcrypt hashed passwords)
  - `sessions`: Data analysis sessions
  - `messages`: Chat history with embedded results (chart data, data previews, function calls)

**In-Memory Storage:**
- Active datasets stored in Python backend memory (`DataProcessor.sessions` dictionary)
- Session-based architecture: each upload creates new session with unique ID
- Trade-off: Fast access, no persistence between restarts (suitable for analysis workflows)

**Schema Design Decisions:**
- UUIDs for all primary keys (PostgreSQL `gen_random_uuid()`)
- JSONB columns for flexible data storage (chart configurations, data previews, suggested actions)
- Timestamps with automatic `NOW()` defaults
- Foreign key constraints with cascading behavior

### Authentication and Authorization

**Dual Authentication Strategy:**
- **Primary**: Supabase Authentication (configurable via environment variables)
- **Fallback**: In-memory bcrypt-based authentication when Supabase unavailable
- **Token Management**: JWT tokens stored in localStorage, included in API requests via Authorization header
- **Session Validation**: Middleware checks for valid tokens on protected routes

**Security Measures:**
- Bcrypt password hashing (never plain text storage)
- CORS middleware configured for cross-origin requests
- Authorization header requirement for data operations
- Environment-based configuration for API keys

## External Dependencies

### Third-Party Services

**AI Providers:**
- **Google Gemini AI** (GEMINI_API_KEY required)
  - Primary AI for natural language understanding and function calling
  - Configured with structured tool definitions for dataset operations
- **Groq** (GROQ_API_KEY required)
  - Ultra-fast inference alternative
  - Fallback when Gemini unavailable or user preference

**Authentication:**
- **Supabase** (optional, SUPABASE_URL + SUPABASE_ANON_KEY + SUPABASE_SERVICE_ROLE_KEY)
  - Managed authentication service
  - Falls back to local authentication if not configured

### Database

**PostgreSQL:**
- Configured via `DATABASE_URL` environment variable
- Managed through Drizzle ORM
- Migration system using `drizzle-kit`
- Connection via `@neondatabase/serverless` for serverless compatibility

### Frontend Libraries

**Core:**
- React 18+ with TypeScript
- Vite for build tooling
- TanStack React Query for server state management

**UI Components:**
- Radix UI primitives (30+ component primitives)
- Shadcn/ui component system
- Tailwind CSS for styling
- Lucide React for icons

**Specialized:**
- Plotly.js for interactive charts
- React Markdown with remark-gfm for markdown rendering
- React Dropzone for file uploads
- React Hook Form with Zod for form validation

### Python Libraries

**Data Processing:**
- pandas: DataFrame operations
- numpy: Numerical computations
- openpyxl: Excel file support
- pyarrow: Parquet file support

**Machine Learning:**
- scikit-learn: ML algorithms (KMeans, DBSCAN, IsolationForest, PCA, t-SNE)
- StandardScaler for normalization

**Visualization:**
- plotly: Chart generation (returns JSON for frontend rendering)

**API Framework:**
- FastAPI with uvicorn server
- python-multipart for file uploads
- python-dotenv for environment configuration

### Development Tools

- TypeScript compiler for type checking
- ESBuild for production builds
- Drizzle Kit for database migrations
- Replit-specific plugins for development environment integration