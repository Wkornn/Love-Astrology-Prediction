import { useState } from 'react';
import { useBirthData } from '../context/BirthDataContext';
import { useResultsCache } from '../context/ResultsCacheContext';
import { Mode2Results } from '../components/results/Mode2Results';
import { validateBirthData } from '../utils/validation';
import { submitCelebrityMatch, type Mode2Response } from '../services/api';

const Mode2Page = () => {
  const { birthData } = useBirthData();
  const { mode2Result, setMode2Result } = useResultsCache();
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const handleSubmit = async () => {
    const validationErrors = validateBirthData(birthData);
    if (Object.keys(validationErrors).length > 0) {
      setApiError('Please fill in all required fields');
      return;
    }

    setLoading(true);
    setApiError(null);
    
    try {
      const response = await submitCelebrityMatch({
        date: birthData.date,
        time: birthData.time,
        latitude: parseFloat(birthData.latitude),
        longitude: parseFloat(birthData.longitude),
        timezone: 'UTC',
      }, 5);
      
      setMode2Result(response);
    } catch (error: any) {
      setApiError(error.response?.data?.error || error.message || 'Failed to match celebrities');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Mode 2: Celebrity Match</h1>
        <p className="text-[#a0a6b0]">Match against public figure database</p>
      </div>

      {apiError && (
        <div className="mb-4 bg-red-900/20 border border-red-500 rounded-lg p-4">
          <p className="text-red-400 text-sm">{apiError}</p>
        </div>
      )}

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="w-full mb-8 bg-[#B5A593] hover:bg-[#9d8a78] disabled:bg-gray-600 disabled:cursor-not-allowed text-black font-semibold py-3 px-6 rounded-lg transition-colors"
      >
        {loading ? 'Matching...' : 'Find Celebrity Matches'}
      </button>

      {mode2Result && mode2Result.status === 'success' && (
        <Mode2Results
          matches={mode2Result.data.matches}
          userVector={mode2Result.data.user_vector}
          totalCelebrities={mode2Result.data.total_celebrities}
        />
      )}
    </div>
  );
};

export default Mode2Page;
