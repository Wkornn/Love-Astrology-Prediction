# Love Astrology Prediction - Love Debugging Lab v2.0

Professional astrological love compatibility analysis system using Python FastAPI backend and React TypeScript frontend.

## 🎯 Features

- **Mode 1**: Single-person love reading with natal chart analysis
- **Mode 2**: Celebrity matching using cosine similarity
- **Mode 3**: Couple compatibility analysis
- **Aspect Engine**: Real-time planetary aspect detection
- **Demo Safety Mode**: Graceful fallbacks prevent crashes
- **Mock Celebrity Database**: 7 in-memory celebrities when DB is empty

## 🚀 Quick Start

```bash
# Backend
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Frontend
cd frontend
npm install
npm run dev
```

Visit: http://localhost:5173

## 📚 Documentation

See [docs/README_DOCS.md](docs/README_DOCS.md) for complete documentation index.

**Key Documents:**
- [Integration Guide](docs/INTEGRATION_GUIDE.md) - Setup instructions
- [API Documentation](docs/API_DOCUMENTATION.md) - Endpoint reference
- [Test Checklist](docs/INTEGRATION_TEST_CHECKLIST.md) - Integration tests
- [Bug Fixes](docs/BUG_FIX_SUMMARY.md) - Recent fixes

## 🧪 Testing

```bash
# Run integration tests
./run_integration_tests.sh
```

## 🏗️ Architecture

- **Backend**: FastAPI + Swiss Ephemeris + SQLite
- **Frontend**: React + TypeScript + Vite + Tailwind v4
- **Feature Vector**: 16-dimensional normalized vector (0-1)
- **Similarity**: Cosine similarity (60%) + Rule-based (40%)

## 📦 Tech Stack

**Backend:**
- FastAPI 0.104.1
- pyswisseph 2.10.3.2
- SQLite3
- Pydantic 2.5.0

**Frontend:**
- React 18
- TypeScript
- Vite
- Tailwind CSS v4
- Axios

## 🎨 UI Theme

Dark lab theme with purple (#8b5cf6) and cyan (#00d9ff) accents.

## 📝 License

University booth project - Educational use only.
