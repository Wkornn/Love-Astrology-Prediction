# Frontend-Backend Integration Guide

## ✅ Integration Complete

### Changes Made

#### 1. Environment Configuration
**File**: `frontend/.env`
```
VITE_API_URL=http://localhost:8000
```

#### 2. API Service Layer
**File**: `frontend/src/services/api.ts`
- Updated to match standardized backend response format
- Added request/response interceptors for logging
- Proper TypeScript interfaces for all responses
- Environment variable for base URL

#### 3. Mode Pages
**Files**: `Mode1Page.tsx`, `Mode2Page.tsx`, `Mode3Page.tsx`
- Connected to real API endpoints
- Loading states with disabled buttons
- Error handling with red error banners
- Console logging for debugging
- Real-time data display from API

## 🚀 How to Run

### Terminal 1: Backend
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

### Access
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🧪 Testing Guide

### Mode 1: Love Reading

**Test Data**:
```
Date: 1990-06-15
Time: 14:30
Latitude: 40.7128
Longitude: -74.0060
```

**Expected Result**:
- Love profile metrics (4 values)
- Personality vector (9 values)
- Elemental profile bars
- Diagnostic insights

**Console Output**:
```
[API Request] POST /api/mode1/love-reading
[Mode1] Submitting: {...}
[API Response] 200 /api/mode1/love-reading
[Mode1] Response: {status: 'success', mode: 'mode1', ...}
```

### Mode 2: Celebrity Match

**Test Data**:
```
Date: 1992-03-20
Time: 10:00
Latitude: 34.0522
Longitude: -118.2437
```

**Expected Result**:
- 5-7 celebrity matches (mock data)
- Similarity scores
- Match reasons
- User profile summary

**Console Output**:
```
[API Request] POST /api/mode2/celebrity-match
[Mode2] Submitting: {...}
[API Response] 200 /api/mode2/celebrity-match
[Mode2] Response: {status: 'success', mode: 'mode2', ...}
```

**Note**: Uses mock celebrity data (Alex Rivera, Jordan Chen, etc.)

### Mode 3: Couple Compatibility

**Test Data**:
```
Person 1:
  Date: 1990-06-15
  Time: 14:30
  Latitude: 40.7128
  Longitude: -74.0060

Person 2:
  Date: 1992-03-20
  Time: 10:00
  Latitude: 34.0522
  Longitude: -118.2437
```

**Expected Result**:
- Overall compatibility score
- Vector/Rule component breakdown
- 3 compatibility indices
- Strengths list
- Challenges list
- Diagnostic insights

**Console Output**:
```
[API Request] POST /api/mode3/couple-match
[Mode3] Submitting: {person1: {...}, person2: {...}}
[API Response] 200 /api/mode3/couple-match
[Mode3] Response: {status: 'success', mode: 'mode3', ...}
```

## 🔍 Debugging

### Check Backend is Running
```bash
curl http://localhost:8000/health
```

Expected: `{"status":"healthy","timestamp":"..."}`

### Check CORS
Open browser console and look for CORS errors. Should see:
```
Access-Control-Allow-Origin: *
```

### Check API Logs
Backend terminal shows:
```
INFO:     127.0.0.1:xxxxx - "POST /api/mode1/love-reading HTTP/1.1" 200 OK
```

### Check Frontend Logs
Browser console shows:
```
[API Request] POST /api/mode1/love-reading
[Mode1] Submitting: {...}
[API Response] 200 /api/mode1/love-reading
[Mode1] Response: {...}
```

## ⚠️ Common Issues

### Issue: "Network Error"
**Cause**: Backend not running
**Fix**: Start backend with `uvicorn app.main:app --reload`

### Issue: "Failed to generate love reading"
**Cause**: Invalid birth data or backend error
**Fix**: Check backend logs for detailed error

### Issue: CORS Error
**Cause**: Backend CORS not configured
**Fix**: Already configured in `app/main.py` with `allow_origins=["*"]`

### Issue: "Using mock celebrity dataset for demo mode"
**Cause**: Database is empty (expected)
**Fix**: This is normal - mock data is used automatically

## 📊 Response Format

All endpoints return:
```json
{
  "status": "success",
  "mode": "mode1|mode2|mode3",
  "data": { ... },
  "diagnostics": {
    "bugs": [...],
    "system_status": "...",
    "drama_risk_level": "...",
    "recommendation_summary": "..."
  },
  "timestamp": "2024-02-28T12:34:56.789Z"
}
```

## 🎨 UI Features

### Loading States
- Button text changes: "Generate Love Reading" → "Analyzing..."
- Button disabled during API call
- Prevents double submissions

### Error Handling
- Red error banner appears below form
- Shows user-friendly error message
- Errors logged to console for debugging

### Success Display
- Results appear below submit button
- Smooth transition
- Real data from API

## 🔧 Configuration

### Change Backend URL
Edit `frontend/.env`:
```
VITE_API_URL=https://your-production-api.com
```

### Disable Console Logging
Remove interceptors from `frontend/src/services/api.ts`:
```typescript
// Comment out or remove:
api.interceptors.request.use(...)
api.interceptors.response.use(...)
```

## ✅ Integration Checklist

- [x] Backend running on port 8000
- [x] Frontend running on port 5173
- [x] CORS configured
- [x] Environment variables set
- [x] API service updated
- [x] All 3 modes connected
- [x] Loading states working
- [x] Error handling working
- [x] Console logging active
- [x] Real data displaying
- [x] Mock celebrity data working

## 🎉 Success Criteria

✅ Mode 1 returns love profile and personality vector
✅ Mode 2 returns 5-7 celebrity matches
✅ Mode 3 returns compatibility scores and insights
✅ Loading states show during API calls
✅ Errors display in red banners
✅ Console logs show request/response flow
✅ No CORS errors
✅ No TypeScript errors
✅ UI updates with real data

## 📝 Next Steps

1. Test with various birth data combinations
2. Verify all diagnostic messages display correctly
3. Test error scenarios (invalid dates, network errors)
4. Add real celebrity data to database (optional)
5. Remove console logging before production
6. Update CORS to specific domains for production
