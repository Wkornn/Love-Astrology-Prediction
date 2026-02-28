"""Public Figure Database - Stores celebrity/public figure data with caching"""

import sqlite3
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import os

class PublicFigureDatabase:
    """
    Manages public figure data with SQLite backend
    
    Features:
    - Persistent storage of birth data
    - Cached feature vectors
    - Efficient querying and matching
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file (default: app/database/figures.db)
        """
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(__file__),
                '../database/figures.db'
            )
        
        self.db_path = db_path
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """Create database and tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main figures table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS public_figures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                occupation TEXT,
                birth_date TEXT NOT NULL,
                birth_time TEXT,
                birth_latitude REAL NOT NULL,
                birth_longitude REAL NOT NULL,
                birth_timezone TEXT DEFAULT 'UTC',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Cached vectors table (separate for flexibility)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cached_vectors (
                figure_id INTEGER PRIMARY KEY,
                feature_vector TEXT NOT NULL,
                computed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (figure_id) REFERENCES public_figures(id) ON DELETE CASCADE
            )
        ''')
        
        # Index for fast name lookup
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_figure_name 
            ON public_figures(name)
        ''')
        
        conn.commit()
        conn.close()
    
    def add_figure(self, name: str, birth_date: str, latitude: float, longitude: float,
                   occupation: str = None, birth_time: str = None, 
                   timezone: str = 'UTC', feature_vector: List[float] = None) -> int:
        """
        Add a public figure to database
        
        Args:
            name: Full name
            birth_date: Date in 'YYYY-MM-DD' format
            latitude: Birth latitude
            longitude: Birth longitude
            occupation: Occupation/category (optional)
            birth_time: Time in 'HH:MM' format (optional)
            timezone: Timezone string (default: 'UTC')
            feature_vector: Pre-computed feature vector (optional)
            
        Returns:
            Figure ID
            
        Raises:
            ValueError: If figure already exists or data is invalid
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO public_figures 
                (name, occupation, birth_date, birth_time, birth_latitude, 
                 birth_longitude, birth_timezone)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, occupation, birth_date, birth_time, latitude, longitude, timezone))
            
            figure_id = cursor.lastrowid
            
            # Cache vector if provided
            if feature_vector:
                self._cache_vector(cursor, figure_id, feature_vector)
            
            conn.commit()
            return figure_id
            
        except sqlite3.IntegrityError:
            raise ValueError(f"Figure '{name}' already exists")
        finally:
            conn.close()
    
    def _cache_vector(self, cursor, figure_id: int, vector: List[float]):
        """Cache computed feature vector"""
        vector_json = json.dumps(vector)
        cursor.execute('''
            INSERT OR REPLACE INTO cached_vectors (figure_id, feature_vector, computed_at)
            VALUES (?, ?, ?)
        ''', (figure_id, vector_json, datetime.utcnow().isoformat()))
    
    def get_all_figures(self, include_vectors: bool = False) -> List[Dict]:
        """
        Get all public figures
        
        Args:
            include_vectors: Include cached feature vectors
            
        Returns:
            List of figure dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if include_vectors:
            query = '''
                SELECT f.*, v.feature_vector, v.computed_at as vector_computed_at
                FROM public_figures f
                LEFT JOIN cached_vectors v ON f.id = v.figure_id
                ORDER BY f.name
            '''
        else:
            query = 'SELECT * FROM public_figures ORDER BY f.name'
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        figures = []
        for row in rows:
            figure = dict(row)
            if include_vectors and figure.get('feature_vector'):
                figure['feature_vector'] = json.loads(figure['feature_vector'])
            figures.append(figure)
        
        return figures
    
    def find_by_name(self, name: str, fuzzy: bool = False) -> Optional[Dict]:
        """
        Find figure by name
        
        Args:
            name: Figure name
            fuzzy: Use fuzzy matching (LIKE query)
            
        Returns:
            Figure dictionary or None
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if fuzzy:
            cursor.execute('''
                SELECT f.*, v.feature_vector
                FROM public_figures f
                LEFT JOIN cached_vectors v ON f.id = v.figure_id
                WHERE f.name LIKE ?
                LIMIT 1
            ''', (f'%{name}%',))
        else:
            cursor.execute('''
                SELECT f.*, v.feature_vector
                FROM public_figures f
                LEFT JOIN cached_vectors v ON f.id = v.figure_id
                WHERE f.name = ?
            ''', (name,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            figure = dict(row)
            if figure.get('feature_vector'):
                figure['feature_vector'] = json.loads(figure['feature_vector'])
            return figure
        return None
    
    def get_cached_vector(self, figure_id: int) -> Optional[List[float]]:
        """Get cached feature vector for figure"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT feature_vector FROM cached_vectors WHERE figure_id = ?',
            (figure_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return json.loads(row[0])
        return None
    
    def cache_vector(self, figure_id: int, vector: List[float]):
        """Cache feature vector for figure"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        self._cache_vector(cursor, figure_id, vector)
        conn.commit()
        conn.close()
    
    def match_user_to_all(self, user_vector: List[float], 
                          similarity_func, top_n: int = 10) -> List[Tuple[Dict, float]]:
        """
        Match user vector against all figures with cached vectors
        
        Args:
            user_vector: User's feature vector
            similarity_func: Function(vec1, vec2) -> similarity_score
            top_n: Number of top matches to return
            
        Returns:
            List of (figure_dict, similarity_score) tuples, sorted by score
        """
        figures = self.get_all_figures(include_vectors=True)
        
        matches = []
        for figure in figures:
            if figure.get('feature_vector'):
                similarity = similarity_func(user_vector, figure['feature_vector'])
                matches.append((figure, similarity))
        
        # Sort by similarity (descending)
        matches.sort(key=lambda x: x[1], reverse=True)
        
        return matches[:top_n]
    
    def bulk_import(self, figures: List[Dict]) -> int:
        """
        Bulk import figures from list
        
        Args:
            figures: List of figure dictionaries
            
        Returns:
            Number of figures imported
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        imported = 0
        for fig in figures:
            try:
                cursor.execute('''
                    INSERT INTO public_figures 
                    (name, occupation, birth_date, birth_time, birth_latitude, 
                     birth_longitude, birth_timezone)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    fig['name'],
                    fig.get('occupation'),
                    fig['birth_date'],
                    fig.get('birth_time'),
                    fig['latitude'],
                    fig['longitude'],
                    fig.get('timezone', 'UTC')
                ))
                
                figure_id = cursor.lastrowid
                
                # Cache vector if provided
                if 'feature_vector' in fig:
                    self._cache_vector(cursor, figure_id, fig['feature_vector'])
                
                imported += 1
                
            except sqlite3.IntegrityError:
                # Skip duplicates
                continue
        
        conn.commit()
        conn.close()
        
        return imported
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM public_figures')
        total_figures = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM cached_vectors')
        cached_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_figures': total_figures,
            'cached_vectors': cached_count,
            'cache_percentage': round(cached_count / total_figures * 100, 1) if total_figures > 0 else 0
        }
