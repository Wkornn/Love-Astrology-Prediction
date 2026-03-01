import { useState } from 'react';
import { useBirthData } from '../context/BirthDataContext';
import { useResultsCache } from '../context/ResultsCacheContext';
import { Mode1Results } from '../components/results/Mode1Results';
import { validateBirthData } from '../utils/validation';
import { submitLoveReading, type Mode1Response } from '../services/api';

const Mode1Page = () => {
  const { birthData } = useBirthData();
  const { mode1Result, setMode1Result } = useResultsCache();
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
      const response = await submitLoveReading({
        date: birthData.date,
        time: birthData.time,
        latitude: parseFloat(birthData.latitude),
        longitude: parseFloat(birthData.longitude),
        timezone: 'UTC',
      }, true);
      
      setMode1Result(response);
    } catch (error: any) {
      setApiError(error.response?.data?.error || error.message || 'Failed to generate love reading');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Mode 1: Love Reading</h1>
        <p className="text-[#a0a6b0]">Single-person natal chart analysis</p>
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
        {loading ? 'Analyzing...' : 'Generate Love Reading'}
      </button>

      {mode1Result && mode1Result.status === 'success' && (
        <Mode1Results
          loveProfile={mode1Result.data.love_profile}
          personalityVector={mode1Result.data.personality_vector}
          diagnostics={mode1Result.diagnostics.bugs}
          narrative={mode1Result.data.narrative}
          aspects={mode1Result.data.debug?.aspects}
          aspectScores={mode1Result.data.debug?.aspect_scores}
        />
      )}
    </div>
  );
};

export default Mode1Page;
