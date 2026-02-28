# Public Figure Database - Schema Design

## Overview

SQLite-based storage for public figures with cached feature vectors for efficient matching.

---

## Database Schema

### **Table: public_figures**

Primary storage for celebrity/public figure data.

```sql
CREATE TABLE public_figures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    occupation TEXT,
    birth_date TEXT NOT NULL,           -- 'YYYY-MM-DD'
    birth_time TEXT,                    -- 'HH:MM' (nullable)
    birth_latitude REAL NOT NULL,
    birth_longitude REAL NOT NULL,
    birth_timezone TEXT DEFAULT 'UTC',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_figure_name ON public_figures(name);
```

**Fields:**
- `id`: Auto-incrementing primary key
- `name`: Unique figure name (indexed for fast lookup)
- `occupation`: Category (Actor, Musician, Athlete, etc.)
- `birth_date`: Required (YYYY-MM-DD format)
- `birth_time`: Optional (HH:MM format) - nullable for unknown times
- `birth_latitude/longitude`: Geographic coordinates
- `birth_timezone`: IANA timezone string
- `created_at/updated_at`: Audit timestamps

---

### **Table: cached_vectors**

Separate table for computed feature vectors (caching layer).

```sql
CREATE TABLE cached_vectors (
    figure_id INTEGER PRIMARY KEY,
    feature_vector TEXT NOT NULL,      -- JSON array of floats
    computed_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (figure_id) REFERENCES public_figures(id) ON DELETE CASCADE
);
```

**Fields:**
- `figure_id`: Foreign key to public_figures (1-to-1 relationship)
- `feature_vector`: JSON-serialized array of 9 floats
- `computed_at`: When vector was computed (for cache invalidation)

**Why Separate Table?**
- Vectors are large (JSON text)
- Not all figures have vectors (missing birth time)
- Can be recomputed/invalidated independently
- Cleaner schema design

---

## Design Rationale

### **1. SQLite vs JSON**

| Aspect | SQLite | JSON File |
|--------|--------|-----------|
| Query speed | Fast (indexed) | Slow (full scan) |
| Concurrent access | Safe | Risky |
| Scalability | 1000s of records | <100 records |
| Transactions | ACID compliant | Manual |
| Caching | Built-in | Manual |

**Recommendation: SQLite** for production, JSON for prototyping.

### **2. Nullable Birth Time**

Many public figures have unknown birth times. Design handles this:
- `birth_time` is nullable
- Vector computation skipped if time missing
- Can still store figure for future updates

### **3. Separate Caching Table**

**Benefits:**
- Query figures without loading vectors
- Recompute vectors without touching figure data
- Clear cache without deleting figures
- Foreign key cascade deletes orphaned vectors

### **4. JSON Vector Storage**

Vectors stored as JSON text:
```json
"[0.5, 1.0, 0.6, 0.4, 0.6, 0.7, 0.7, 1.0, 0.67]"
```

**Alternatives considered:**
- BLOB: Less readable, harder to debug
- Separate columns: Inflexible (9 columns for 9 features)
- Separate table: Over-engineering for fixed-size vectors

**JSON chosen for:** Readability, flexibility, SQLite JSON support.

---

## API Methods

### **CRUD Operations**

```python
# Create
figure_id = db.add_figure(
    name="Taylor Swift",
    birth_date="1989-12-13",
    birth_time="05:17",
    latitude=40.5853,
    longitude=-75.6184,
    occupation="Musician"
)

# Read
figure = db.find_by_name("Taylor Swift")
all_figures = db.get_all_figures(include_vectors=True)

# Update (via cache)
db.cache_vector(figure_id, computed_vector)

# Delete (manual SQL for now)
```

### **Caching Operations**

```python
# Check if vector cached
vector = db.get_cached_vector(figure_id)

# Cache new vector
db.cache_vector(figure_id, feature_vector)

# Get stats
stats = db.get_stats()
# → {'total_figures': 50, 'cached_vectors': 42, 'cache_percentage': 84.0}
```

### **Matching Operations**

```python
# Match user against all cached figures
matches = db.match_user_to_all(
    user_vector,
    similarity_func=lambda v1, v2: cosine_similarity(v1, v2),
    top_n=10
)
# → [(figure_dict, similarity_score), ...]
```

### **Bulk Operations**

```python
# Import from JSON
figures = [
    {'name': 'Celebrity A', 'birth_date': '1990-01-01', ...},
    {'name': 'Celebrity B', 'birth_date': '1985-05-15', ...}
]
imported = db.bulk_import(figures)
```

---

## Caching Strategy

### **When to Cache**

1. **On Import**: If vector provided in bulk import
2. **On Demand**: When figure is first queried for matching
3. **Batch Processing**: Nightly job to compute missing vectors

### **Cache Invalidation**

Recompute vectors when:
- Birth data corrected
- Feature extraction algorithm updated
- Vector dimensions change

### **Cache Hit Rate**

```python
stats = db.get_stats()
hit_rate = stats['cache_percentage']

if hit_rate < 80:
    # Trigger batch vector computation
    compute_missing_vectors()
```

---

## Scaling Considerations

### **Current Capacity**

SQLite handles:
- **100K+ records** easily
- **10MB+ database** no problem
- **Concurrent reads** efficiently

### **Future Scaling Path**

**Phase 1 (0-1K figures):** SQLite file  
**Phase 2 (1K-10K figures):** SQLite + connection pooling  
**Phase 3 (10K-100K figures):** PostgreSQL migration  
**Phase 4 (100K+ figures):** Sharding + vector database (Pinecone, Weaviate)  

### **Migration Path**

```python
# Export from SQLite
figures = db.get_all_figures(include_vectors=True)

# Import to PostgreSQL
pg_db = PostgreSQLDatabase()
pg_db.bulk_import(figures)
```

Schema is database-agnostic (standard SQL).

---

## Performance Optimization

### **1. Indexing**

```sql
CREATE INDEX idx_figure_name ON public_figures(name);
CREATE INDEX idx_occupation ON public_figures(occupation);
```

### **2. Query Optimization**

```python
# Bad: Load all vectors into memory
figures = db.get_all_figures(include_vectors=True)
for fig in figures:
    similarity = compute(user_vec, fig['feature_vector'])

# Good: Stream and filter
matches = db.match_user_to_all(user_vec, similarity_func, top_n=10)
```

### **3. Batch Operations**

```python
# Bad: Insert one by one
for fig in figures:
    db.add_figure(**fig)

# Good: Bulk import
db.bulk_import(figures)
```

---

## Security Considerations

### **1. SQL Injection Prevention**

All queries use parameterized statements:
```python
cursor.execute('SELECT * FROM public_figures WHERE name = ?', (name,))
```

### **2. Data Validation**

```python
# Validate date format
datetime.strptime(birth_date, '%Y-%m-%d')

# Validate coordinates
assert -90 <= latitude <= 90
assert -180 <= longitude <= 180
```

### **3. Access Control**

For production:
- Read-only API for public access
- Admin API for write operations
- Rate limiting on matching queries

---

## Example Usage

### **Setup Database**

```python
from database.public_figure_db import PublicFigureDatabase

db = PublicFigureDatabase()  # Creates figures.db if not exists
```

### **Add Figures**

```python
# Single figure
db.add_figure(
    name="Ariana Grande",
    birth_date="1993-06-26",
    birth_time="09:16",
    latitude=26.1224,
    longitude=-80.1373,
    occupation="Musician"
)

# Bulk import
with open('celebrities.json') as f:
    figures = json.load(f)
db.bulk_import(figures)
```

### **Compute and Cache Vectors**

```python
calculator = BirthChartCalculator()
builder = FeatureVectorBuilder()

for figure in db.get_all_figures():
    if not db.get_cached_vector(figure['id']):
        chart = calculator.calculate_chart_json(...)
        vector = builder.build_vector(chart['data'], aspects)
        db.cache_vector(figure['id'], vector['feature_vector'])
```

### **Match User to Celebrities**

```python
user_vector = [0.5, 1.0, 0.6, ...]

matches = db.match_user_to_all(
    user_vector,
    lambda v1, v2: cosine_similarity(v1, v2)['percentage'],
    top_n=5
)

for figure, score in matches:
    print(f"{figure['name']}: {score}%")
```

---

## Testing

```bash
cd backend
python example_database.py
```

**Output:**
1. Database initialization
2. Sample data import
3. Vector computation and caching
4. Query operations
5. Celebrity matching demo

---

## Summary

✅ **SQLite backend** - Fast, reliable, ACID-compliant  
✅ **Separate caching table** - Clean design, easy invalidation  
✅ **Nullable birth time** - Handles incomplete data  
✅ **Indexed queries** - Fast name lookup  
✅ **Bulk operations** - Efficient data import  
✅ **Scalable design** - Clear migration path to PostgreSQL  
✅ **Production-ready** - SQL injection prevention, validation  

**Ready for Mode 2 (Celebrity Matching) integration!**
