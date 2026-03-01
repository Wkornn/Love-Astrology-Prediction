import { useState } from 'react';

interface LocationResult {
  display_name: string;
  lat: string;
  lon: string;
}

interface LocationSearchProps {
  onSelect: (lat: number, lon: number, name: string) => void;
  selectedLocation?: string;
  onClear?: () => void;
}

export const LocationSearch = ({ onSelect, selectedLocation, onClear }: LocationSearchProps) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<LocationResult[]>([]);
  const [loading, setLoading] = useState(false);

  const searchLocation = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&limit=5`,
        { headers: { 'User-Agent': 'LoveAstrologyApp/1.0' } }
      );
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Location search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setQuery('');
    setResults([]);
    onClear?.();
  };

  return (
    <div className="space-y-2">
      <div className="flex gap-2">
        <div className="flex-1 relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && searchLocation()}
            placeholder={selectedLocation || "Search: Bangkok, New York, Tokyo..."}
            className="w-full bg-[#1a1a24] border border-[#2a2a3a] rounded-lg px-4 py-2 pr-10 text-white placeholder-gray-500"
          />
          {(query || selectedLocation) && (
            <button
              onClick={handleClear}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
            >
              ✕
            </button>
          )}
        </div>
        <button
          onClick={searchLocation}
          disabled={loading}
          className="bg-[#E07A5F] hover:bg-[#c96a4f] disabled:bg-gray-600 text-white px-6 py-2 rounded-lg"
        >
          {loading ? '...' : 'Search'}
        </button>
      </div>

      {results.length > 0 && (
        <div className="bg-[#1a1a24] border border-[#2a2a3a] rounded-lg max-h-60 overflow-y-auto">
          {results.map((result, idx) => (
            <button
              key={idx}
              onClick={() => {
                onSelect(parseFloat(result.lat), parseFloat(result.lon), result.display_name);
                setResults([]);
                setQuery('');
              }}
              className="w-full text-left px-4 py-3 hover:bg-[#2a2a3a] border-b border-[#2a2a3a] last:border-b-0"
            >
              <div className="text-sm text-white">{result.display_name}</div>
              <div className="text-xs text-gray-400 mt-1">
                {parseFloat(result.lat).toFixed(4)}, {parseFloat(result.lon).toFixed(4)}
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
