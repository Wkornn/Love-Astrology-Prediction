import { useState } from 'react';
import { BirthDataForm, type BirthData } from '../components/forms/BirthDataForm';
import { Mode2Results } from '../components/results/Mode2Results';
import { validateBirthData } from '../utils/validation';
import { submitCelebrityMatch, type Mode2Response } from '../services/api';

const Mode2Page = () => {
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
  const [result, setResult] = useState<Mode2Response | null>(null);

  const handleSubmit = async () => {
    const validationErrors = validateBirthData(data);
    setErrors(validationErrors);
    setApiError(null);
    
    if (Object.keys(validationErrors).length === 0) {
      setLoading(true);
      console.log('[Mode2] Submitting:', data);
      
      try {
        const response = await submitCelebrityMatch({
          date: data.date,
          time: data.time,
          latitude: parseFloat(data.latitude),
          longitude: parseFloat(data.longitude),
          timezone: 'UTC',
        }, 5);
        
        console.log('[Mode2] Response:', response);
        setResult(response);
      } catch (error: any) {
        console.error('[Mode2] Error:', error);
        const errorMsg = error.response?.data?.error || error.message || 'Failed to match celebrities';
        setApiError(errorMsg);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Mode 2: Celebrity Match</h1>
        <p className="text-[#a0a6b0]">Match against public figure database</p>
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
        className="w-full mt-6 bg-[#00d9ff] hover:bg-[#00c4e6] disabled:bg-gray-600 disabled:cursor-not-allowed text-black font-semibold py-3 px-6 rounded-lg transition-colors"
      >
        {loading ? 'Matching...' : 'Find Celebrity Matches'}
      </button>

      {result && result.status === 'success' && (
        <div className="mt-8">
          <Mode2Results
            matches={result.data.matches}
            userVector={result.data.user_vector}
            totalCelebrities={result.data.total_celebrities}
          />
        </div>
      )}
    </div>
  );
};

export default Mode2Page;
