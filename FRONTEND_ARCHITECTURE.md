# Frontend Architecture - Love Debugging Lab v2.0

## Tech Stack

- **Framework**: React 18 + Vite
- **Language**: TypeScript
- **Styling**: Tailwind CSS (dark theme)
- **State Management**: React Context API + Hooks
- **HTTP Client**: Axios
- **Routing**: React Router v6

---

## Folder Structure

```
frontend/
├── public/
│   └── favicon.ico
│
├── src/
│   ├── main.tsx                    # App entry point
│   ├── App.tsx                     # Root component
│   │
│   ├── pages/
│   │   ├── Home.tsx                # Mode selection
│   │   ├── Mode1Page.tsx           # Love Reading
│   │   ├── Mode2Page.tsx           # Celebrity Match
│   │   └── Mode3Page.tsx           # Couple Match
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx          # App header
│   │   │   ├── Footer.tsx          # App footer
│   │   │   └── Layout.tsx          # Page wrapper
│   │   │
│   │   ├── forms/
│   │   │   ├── BirthDataForm.tsx   # Reusable birth data input
│   │   │   ├── FormInput.tsx       # Input field component
│   │   │   └── FormButton.tsx      # Button component
│   │   │
│   │   ├── results/
│   │   │   ├── LoveProfile.tsx     # Mode 1 results
│   │   │   ├── CelebrityMatches.tsx # Mode 2 results
│   │   │   ├── CompatibilityReport.tsx # Mode 3 results
│   │   │   ├── DiagnosticBugs.tsx  # Bug list display
│   │   │   ├── ScoreGauge.tsx      # Score visualization
│   │   │   └── ProgressBar.tsx     # Progress indicator
│   │   │
│   │   └── common/
│   │       ├── Card.tsx            # Card container
│   │       ├── Loading.tsx         # Loading spinner
│   │       └── ErrorMessage.tsx    # Error display
│   │
│   ├── services/
│   │   └── api.ts                  # API service layer
│   │
│   ├── types/
│   │   └── index.ts                # TypeScript interfaces
│   │
│   ├── context/
│   │   └── AppContext.tsx          # Global state
│   │
│   ├── hooks/
│   │   ├── useApi.ts               # API call hook
│   │   └── useForm.ts              # Form handling hook
│   │
│   ├── utils/
│   │   ├── validation.ts           # Form validation
│   │   └── formatters.ts           # Data formatting
│   │
│   └── styles/
│       └── globals.css             # Global styles
│
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
└── README.md
```

---

## Component Hierarchy

```
App
├── Layout
│   ├── Header
│   └── Footer
│
└── Router
    ├── Home (Mode Selection)
    │   └── ModeCard (x3)
    │
    ├── Mode1Page (Love Reading)
    │   ├── BirthDataForm
    │   │   ├── FormInput (x4)
    │   │   └── FormButton
    │   └── LoveProfile (Results)
    │       ├── ScoreGauge (x5)
    │       ├── DiagnosticBugs
    │       └── Card
    │
    ├── Mode2Page (Celebrity Match)
    │   ├── BirthDataForm
    │   └── CelebrityMatches (Results)
    │       ├── Card (per match)
    │       └── ProgressBar
    │
    └── Mode3Page (Couple Match)
        ├── BirthDataForm (x2)
        └── CompatibilityReport (Results)
            ├── ScoreGauge (x3)
            ├── DiagnosticBugs
            └── Card
```

---

## State Management

### **Approach: Context API + Hooks**

**Why not Redux?**
- App is relatively simple
- Context API sufficient for 3 modes
- Less boilerplate
- Easier to understand

### **AppContext Structure**

```typescript
interface AppState {
  mode: 'mode1' | 'mode2' | 'mode3' | null;
  loading: boolean;
  error: string | null;
  results: {
    mode1?: Mode1Result;
    mode2?: Mode2Result;
    mode3?: Mode3Result;
  };
}

interface AppContextType {
  state: AppState;
  setMode: (mode: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setResults: (mode: string, data: any) => void;
  clearResults: () => void;
}
```

---

## Page Designs

### **1. Home Page (Mode Selection)**

```
┌─────────────────────────────────────────────────┐
│  LOVE DEBUGGING LAB v2.0                        │
│  Professional Astrological Compatibility System │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │  MODE 1   │  │  MODE 2   │  │  MODE 3   │  │
│  │           │  │           │  │           │  │
│  │   Love    │  │ Celebrity │  │  Couple   │  │
│  │  Reading  │  │   Match   │  │   Match   │  │
│  │           │  │           │  │           │  │
│  │  [Start]  │  │  [Start]  │  │  [Start]  │  │
│  └───────────┘  └───────────┘  └───────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

### **2. Input Form (Dynamic)**

```
┌─────────────────────────────────────────────────┐
│  MODE 1: LOVE READING                           │
├─────────────────────────────────────────────────┤
│                                                 │
│  Birth Data                                     │
│  ┌─────────────────────────────────────────┐   │
│  │ Date: [YYYY-MM-DD]                      │   │
│  └─────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────┐   │
│  │ Time: [HH:MM]                           │   │
│  └─────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────┐   │
│  │ Latitude: [40.7128]                     │   │
│  └─────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────┐   │
│  │ Longitude: [-74.0060]                   │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  [Analyze] [Back]                               │
│                                                 │
└─────────────────────────────────────────────────┘
```

### **3. Results Dashboard**

```
┌─────────────────────────────────────────────────┐
│  SYSTEM DIAGNOSTIC REPORT                       │
├─────────────────────────────────────────────────┤
│                                                 │
│  Love Profile                                   │
│  ┌─────────────────────────────────────────┐   │
│  │ Love Readiness      [████████░░] 75%    │   │
│  │ Emotional Maturity  [█████████░] 82%    │   │
│  │ Passion Level       [████████░░] 85%    │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  System Diagnostics                             │
│  ┌─────────────────────────────────────────┐   │
│  │ 🟢 [INFO] READINESS_HIGH_300            │   │
│  │    High love readiness detected.        │   │
│  │    → Proceed with partner search.       │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  [New Analysis] [Export]                        │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Key Components

### **1. BirthDataForm.tsx**

**Reusable form for all modes**

```typescript
interface BirthDataFormProps {
  onSubmit: (data: BirthData) => void;
  label?: string;
}

const BirthDataForm: React.FC<BirthDataFormProps> = ({ onSubmit, label }) => {
  // Form state and validation
  // Returns structured birth data
}
```

**Used in:**
- Mode 1: Single form
- Mode 2: Single form
- Mode 3: Two forms (Person 1, Person 2)

---

### **2. DiagnosticBugs.tsx**

**Display love bugs with severity**

```typescript
interface Bug {
  severity: 'CRITICAL' | 'WARNING' | 'INFO';
  code: string;
  message: string;
  recommendation: string;
}

const DiagnosticBugs: React.FC<{ bugs: Bug[] }> = ({ bugs }) => {
  // Map severity to colors
  // Display bug cards
}
```

**Styling:**
- CRITICAL: Red border, red icon
- WARNING: Yellow border, yellow icon
- INFO: Green border, green icon

---

### **3. ScoreGauge.tsx**

**Visual score display**

```typescript
interface ScoreGaugeProps {
  label: string;
  value: number; // 0-100
  color?: string;
}

const ScoreGauge: React.FC<ScoreGaugeProps> = ({ label, value, color }) => {
  // Progress bar or circular gauge
  // Color-coded by value
}
```

---

## API Service Layer

### **services/api.ts**

```typescript
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export const api = {
  mode1: async (birthData: BirthData) => {
    const response = await axios.post(`${API_BASE}/mode1/love-reading`, {
      birth_data: birthData
    });
    return response.data;
  },

  mode2: async (birthData: BirthData, topN: number = 5) => {
    const response = await axios.post(`${API_BASE}/mode2/celebrity-match`, {
      birth_data: birthData,
      top_n: topN
    });
    return response.data;
  },

  mode3: async (person1: BirthData, person2: BirthData) => {
    const response = await axios.post(`${API_BASE}/mode3/couple-match`, {
      person1,
      person2
    });
    return response.data;
  }
};
```

**Benefits:**
- Centralized API calls
- Easy to mock for testing
- Type-safe with TypeScript
- Error handling in one place

---

## Custom Hooks

### **useApi.ts**

```typescript
const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const callApi = async (apiFunc: () => Promise<any>) => {
    setLoading(true);
    setError(null);
    try {
      const result = await apiFunc();
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { loading, error, callApi };
};
```

---

## Dark Theme Design

### **Color Palette**

```css
:root {
  --bg-primary: #0a0e27;      /* Deep space blue */
  --bg-secondary: #1a1f3a;    /* Card background */
  --bg-tertiary: #2a2f4a;     /* Hover states */
  
  --text-primary: #e0e6ed;    /* Main text */
  --text-secondary: #a0a6b0;  /* Secondary text */
  --text-muted: #6a7080;      /* Muted text */
  
  --accent-primary: #00d9ff;  /* Cyan accent */
  --accent-secondary: #7c3aed; /* Purple accent */
  
  --success: #10b981;         /* Green */
  --warning: #f59e0b;         /* Yellow */
  --error: #ef4444;           /* Red */
  --info: #3b82f6;            /* Blue */
}
```

### **Typography**

```css
font-family: 'Inter', 'Roboto Mono', monospace;
```

**Monospace for:**
- Bug codes
- System status
- Diagnostic messages

---

## Routing

### **React Router Setup**

```typescript
<BrowserRouter>
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/mode1" element={<Mode1Page />} />
    <Route path="/mode2" element={<Mode2Page />} />
    <Route path="/mode3" element={<Mode3Page />} />
  </Routes>
</BrowserRouter>
```

---

## Responsive Design

### **Breakpoints**

```css
sm: 640px   /* Mobile */
md: 768px   /* Tablet */
lg: 1024px  /* Desktop */
xl: 1280px  /* Large desktop */
```

### **Layout Strategy**

- **Mobile**: Single column, stacked forms
- **Tablet**: Two columns for Mode 3
- **Desktop**: Three columns for mode selection

---

## Setup Commands

```bash
# Create Vite project
npm create vite@latest frontend -- --template react-ts

cd frontend

# Install dependencies
npm install
npm install react-router-dom
npm install axios
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Run dev server
npm run dev
```

---

## Package.json Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext ts,tsx"
  }
}
```

---

## TypeScript Interfaces

### **types/index.ts**

```typescript
export interface BirthData {
  date: string;
  time: string;
  latitude: number;
  longitude: number;
  timezone?: string;
}

export interface LoveBug {
  severity: 'CRITICAL' | 'WARNING' | 'INFO';
  code: string;
  message: string;
  recommendation: string;
}

export interface Mode1Result {
  love_profile: {
    love_readiness: number;
    emotional_maturity: number;
    relationship_focus: number;
    passion_level: number;
    stability_potential: number;
  };
  diagnostics: {
    bugs: LoveBug[];
    system_status: string;
    recommendation_summary: string;
  };
}

export interface CelebrityMatch {
  name: string;
  occupation: string;
  similarity_score: number;
  match_reason: string;
}

export interface Mode2Result {
  matches: CelebrityMatch[];
  user_vector: Record<string, number>;
}

export interface Mode3Result {
  overall_score: number;
  emotional_sync: number;
  chemistry_index: number;
  stability_index: number;
  strengths: string[];
  challenges: string[];
  diagnostics: {
    bugs: LoveBug[];
    drama_risk_level: string;
    system_status: string;
    recommendation_summary: string;
  };
}
```

---

## Development Workflow

### **1. Start Backend**
```bash
cd backend
uvicorn app.main:app --reload
```

### **2. Start Frontend**
```bash
cd frontend
npm run dev
```

### **3. Access**
- Frontend: http://localhost:5173
- Backend: http://localhost:8000

---

## Summary

✅ **React + Vite + TypeScript** - Modern stack  
✅ **Dark theme** - Lab/debugging aesthetic  
✅ **Modular components** - Reusable, testable  
✅ **Context API** - Simple state management  
✅ **Service layer** - Clean API abstraction  
✅ **Responsive** - Mobile-first design  
✅ **Type-safe** - Full TypeScript coverage  

**Architecture is production-ready and scalable!**
