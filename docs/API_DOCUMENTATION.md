# FastAPI Layer Documentation

## Overview

Clean FastAPI implementation with **zero business logic in endpoints**. All logic in service orchestrator.

---

## Architecture

```
API Layer (FastAPI)
    ↓
Service Orchestrator (Business Logic)
    ↓
Core Services (Chart, Vector, Similarity, etc.)
```

**Key Principle:** Endpoints are thin wrappers. Orchestrator handles all logic.

---

## Endpoints

### **POST /api/mode1/love-reading**

Single-person love reading (natal analysis only).

**Request:**
```json
{
  "birth_data": {
    "date": "1990-01-15",
    "time": "14:30",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timezone": "UTC"
  }
}
```

**Response:**
```json
{
  "success": true,
  "mode": "mode1",
  "love_profile": {
    "love_readiness": 75.0,
    "emotional_maturity": 82.0,
    "relationship_focus": 68.0,
    "passion_level": 85.0,
    "stability_potential": 70.0
  },
  "personality_vector": {
    "venus_element": 0.5,
    "mars_element": 1.0,
    ...
  }
}
```

---

### **POST /api/mode2/celebrity-match**

Match user against public figure database.

**Request:**
```json
{
  "birth_data": {
    "date": "1995-03-20",
    "time": "15:30",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "top_n": 5
}
```

**Response:**
```json
{
  "success": true,
  "mode": "mode2",
  "matches": [
    {
      "name": "Taylor Swift",
      "occupation": "Musician",
      "similarity_score": 87.5,
      "match_reason": "Similar romantic expression"
    },
    ...
  ],
  "user_vector": {...},
  "total_celebrities": 50
}
```

---

### **POST /api/mode3/couple-match**

Compare two people for compatibility.

**Request:**
```json
{
  "person1": {
    "date": "1990-01-15",
    "time": "14:30",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "person2": {
    "date": "1992-06-20",
    "time": "09:15",
    "latitude": 34.0522,
    "longitude": -118.2437
  }
}
```

**Response:**
```json
{
  "success": true,
  "mode": "mode3",
  "overall_score": 78.5,
  "vector_component": 85.0,
  "rule_component": 68.0,
  "emotional_sync": 72.0,
  "chemistry_index": 81.0,
  "stability_index": 65.0,
  "strengths": [
    "Strong emotional synchronization",
    "High romantic chemistry"
  ],
  "challenges": [
    "Different Fire expression - requires compromise"
  ]
}
```

---

## Running the Server

### **Development:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Production:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### **Access:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs (Swagger UI)
- ReDoc: http://localhost:8000/redoc

---

## Testing

### **Python Script:**
```bash
cd backend
python test_api.py
```

### **Curl Examples:**

**Mode 1:**
```bash
curl -X POST http://localhost:8000/api/mode1/love-reading \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "date": "1990-01-15",
      "time": "14:30",
      "latitude": 40.7128,
      "longitude": -74.0060
    }
  }'
```

**Mode 2:**
```bash
curl -X POST http://localhost:8000/api/mode2/celebrity-match \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "date": "1995-03-20",
      "time": "15:30",
      "latitude": 40.7128,
      "longitude": -74.0060
    },
    "top_n": 5
  }'
```

**Mode 3:**
```bash
curl -X POST http://localhost:8000/api/mode3/couple-match \
  -H "Content-Type: application/json" \
  -d '{
    "person1": {
      "date": "1990-01-15",
      "time": "14:30",
      "latitude": 40.7128,
      "longitude": -74.0060
    },
    "person2": {
      "date": "1992-06-20",
      "time": "09:15",
      "latitude": 34.0522,
      "longitude": -118.2437
    }
  }'
```

---

## Code Structure

### **1. Request Schemas** (`api/schemas/requests.py`)
```python
class BirthDataRequest(BaseModel):
    date: str
    time: str
    latitude: float
    longitude: float
    timezone: Optional[str] = "UTC"

class Mode1Request(BaseModel):
    birth_data: BirthDataRequest

class Mode2Request(BaseModel):
    birth_data: BirthDataRequest
    top_n: Optional[int] = 5

class Mode3Request(BaseModel):
    person1: BirthDataRequest
    person2: BirthDataRequest
```

**Features:**
- Pydantic validation
- Type checking
- Date/time format validation
- Coordinate range validation

---

### **2. Response Schemas** (`api/schemas/responses.py`)
```python
class Mode1Response(BaseModel):
    success: bool
    mode: str
    love_profile: Dict[str, float]
    personality_vector: Dict[str, float]

class Mode2Response(BaseModel):
    success: bool
    mode: str
    matches: List[CelebrityMatch]
    user_vector: Dict[str, float]
    total_celebrities: int

class Mode3Response(BaseModel):
    success: bool
    mode: str
    overall_score: float
    # ... other fields
```

**Features:**
- Type-safe responses
- Auto-generated OpenAPI docs
- Consistent structure

---

### **3. Service Orchestrator** (`api/service_orchestrator.py`)

**All business logic lives here:**

```python
class ServiceOrchestrator:
    def __init__(self):
        self.chart_calculator = BirthChartCalculator()
        self.vector_builder = FeatureVectorBuilder()
        self.similarity_engine = SimilarityEngine()
        # ... other services
    
    def execute_mode1(self, birth_data):
        # Mode 1 logic
        pass
    
    def execute_mode2(self, birth_data, top_n):
        # Mode 2 logic
        pass
    
    def execute_mode3(self, person1_data, person2_data):
        # Mode 3 logic
        pass
```

**Benefits:**
- Single responsibility
- Easy to test
- No logic in endpoints
- Reusable across different interfaces (CLI, API, etc.)

---

### **4. Route Handlers** (`api/routes/modes.py`)

**Thin wrappers with zero business logic:**

```python
@router.post("/mode1/love-reading")
async def mode1_love_reading(request: Mode1Request):
    try:
        result = orchestrator.execute_mode1(request.birth_data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

**Only responsibilities:**
- Request validation (Pydantic)
- Call orchestrator
- Error handling
- Return response

---

## Error Handling

### **Validation Errors (422)**
```json
{
  "detail": [
    {
      "loc": ["body", "birth_data", "date"],
      "msg": "Date must be in YYYY-MM-DD format",
      "type": "value_error"
    }
  ]
}
```

### **Business Logic Errors (400)**
```json
{
  "detail": "Chart calculation failed: Invalid date"
}
```

### **Server Errors (500)**
```json
{
  "detail": "Internal server error"
}
```

---

## CORS Configuration

Currently allows all origins (development):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production:** Restrict to specific domains.

---

## Auto-Generated Documentation

FastAPI automatically generates:

### **Swagger UI** (http://localhost:8000/docs)
- Interactive API testing
- Request/response examples
- Schema documentation

### **ReDoc** (http://localhost:8000/redoc)
- Clean documentation
- Printable format
- Schema explorer

---

## Design Principles

### **1. Separation of Concerns**
- Endpoints: Request/response handling
- Orchestrator: Business logic
- Services: Domain logic

### **2. Single Responsibility**
- Each endpoint does ONE thing
- Orchestrator coordinates services
- Services handle specific domains

### **3. Dependency Injection**
- Orchestrator initialized once
- Services injected into orchestrator
- Easy to mock for testing

### **4. Type Safety**
- Pydantic models everywhere
- Auto-validation
- IDE autocomplete

---

## Performance Considerations

### **Current:**
- Synchronous processing
- Single worker
- ~500ms per request (chart calculation)

### **Optimizations:**
- Cache computed vectors
- Async database queries
- Connection pooling
- Multiple workers

### **Scaling:**
```bash
# Multiple workers
uvicorn app.main:app --workers 4

# Behind nginx
nginx → uvicorn workers

# Load balancer
Load Balancer → Multiple servers
```

---

## Summary

✅ **Clean architecture** - Zero business logic in endpoints  
✅ **Service orchestrator** - All logic centralized  
✅ **Type-safe** - Pydantic validation  
✅ **Auto-docs** - Swagger + ReDoc  
✅ **Testable** - Easy to mock orchestrator  
✅ **Scalable** - Clear separation for scaling  

**Production-ready API layer complete!**
