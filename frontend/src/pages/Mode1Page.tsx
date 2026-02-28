import { useState } from 'react';
import { BirthDataForm, type BirthData } from '../components/forms/BirthDataForm';
import { Mode1Results } from '../components/results/Mode1Results';
import { validateBirthData } from '../utils/validation';
import { submitLoveReading, type Mode1Response } from '../services/api';

const Mode1Page = () => {
  const [data, setData] = useState<BirthData>({
    name: '',
    date: '',
    time: '',
    latitude: '',
    longitude: '',
  });
  const [errors, setErrors] = useState<Partial<Record<keyof BirthData, string>>>({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);
  const [result, setResult] = useState<Mode1Response | null>(null);

  const handleSubmit = async () => {
    const validationErrors = validateBirthData(data);
    setErrors(validationErrors);
    setApiError(null);
    
    if (Object.keys(validationErrors).length === 0) {
      setLoading(true);
      console.log('[Mode1] Submitting:', data);
      
      try {
        const response = await submitLoveReading({
          date: data.date,
          time: data.time,
          latitude: parseFloat(data.latitude),
          longitude: parseFloat(data.longitude),
          timezone: 'UTC',
        }, true); // Enable debug mode
        
        console.log('[Mode1] Response:', response);
        setResult(response);
      } catch (error: any) {
        console.error('[Mode1] Error:', error);
        const errorMsg = error.response?.data?.error || error.message || 'Failed to generate love reading';
        setApiError(errorMsg);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Mode 1: Love Reading</h1>
        <p className="text-[#a0a6b0]">Single-person natal chart analysis</p>
      </div>

      <BirthDataForm data={data} onChange={setData} errors={errors} />

      {apiError && (
        <div className="mt-4 bg-red-900/20 border border-red-500 rounded-lg p-4">
          <p className="text-red-400 text-sm">{apiError}</p>
        </div>
      )}

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="w-full mt-6 bg-[#8b5cf6] hover:bg-[#7c3aed] disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-colors"
      >
        {loading ? 'Analyzing...' : 'Generate Love Reading'}
      </button>

      {result && result.status === 'success' && (
        <div className="mt-8">
          <Mode1Results
            loveProfile={result.data.love_profile}
            personalityVector={result.data.personality_vector}
            diagnostics={result.diagnostics.bugs}
            aspects={result.data.debug?.aspects}
            aspectScores={result.data.debug?.aspect_scores}
          />
        </div>
      )}
    </div>
  );
};

export default Mode1Page;
