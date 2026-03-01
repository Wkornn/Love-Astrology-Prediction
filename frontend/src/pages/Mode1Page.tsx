import { useState } from 'react';
import { useBirthData } from '../context/BirthDataContext';
import { Mode1Results } from '../components/results/Mode1Results';
import { validateBirthData } from '../utils/validation';
import { submitLoveReading, type Mode1Response } from '../services/api';

const Mode1Page = () => {
  const { birthData } = useBirthData();
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);
  const [result, setResult] = useState<Mode1Response | null>(null);

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
      
      setResult(response);
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
        className="w-full mb-8 bg-[#B5A593] hover:bg-[#9d8a78] disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-colors"
      >
        {loading ? 'Analyzing...' : 'Generate Love Reading'}
      </button>

      {result && result.status === 'success' && (
        <Mode1Results
          loveProfile={result.data.love_profile}
          personalityVector={result.data.personality_vector}
          diagnostics={result.diagnostics.bugs}
          narrative={result.data.narrative}
          aspects={result.data.debug?.aspects}
          aspectScores={result.data.debug?.aspect_scores}
        />
      )}
    </div>
  );
};

export default Mode1Page;
