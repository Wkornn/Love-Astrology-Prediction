import { useState } from 'react';
import { useBirthData } from '../context/BirthDataContext';
import { useResultsCache } from '../context/ResultsCacheContext';
import { BirthDataForm, type BirthData } from '../components/forms/BirthDataForm';
import { Mode3Results } from '../components/results/Mode3Results';
import { validateBirthData } from '../utils/validation';
import { submitCoupleMatch } from '../services/api';

const Mode3Page = () => {
  const { birthData: person1 } = useBirthData();
  const { mode3Result, setMode3Result } = useResultsCache();
  const [person2, setPerson2] = useState<BirthData>({
    date: '',
    time: '',
    latitude: '',
    longitude: '',
  });
  const [errors2, setErrors2] = useState<Partial<Record<keyof BirthData, string>>>({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const handleSubmit = async () => {
    const validationErrors1 = validateBirthData(person1);
    const validationErrors2 = validateBirthData(person2);
    setErrors2(validationErrors2);
    
    if (Object.keys(validationErrors1).length > 0 || Object.keys(validationErrors2).length > 0) {
      setApiError('Please fill in all required fields for both people');
      return;
    }

    setLoading(true);
    setApiError(null);
    
    try {
      const response = await submitCoupleMatch(
        {
          date: person1.date,
          time: person1.time,
          latitude: parseFloat(person1.latitude),
          longitude: parseFloat(person1.longitude),
          timezone: 'UTC',
        },
        {
          date: person2.date,
          time: person2.time,
          latitude: parseFloat(person2.latitude),
          longitude: parseFloat(person2.longitude),
          timezone: 'UTC',
        }
      );
      
      setMode3Result(response);
    } catch (error: any) {
      setApiError(error.response?.data?.error || error.message || 'Failed to analyze compatibility');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Mode 3: Couple Match</h1>
        <p className="text-[#a0a6b0]">Two-person compatibility analysis</p>
      </div>

      <div className="mb-8">
        <h3 className="text-lg font-semibold text-[#B5A593] mb-4">Person 2 Birth Data</h3>
        <BirthDataForm data={person2} onChange={setPerson2} errors={errors2} />
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
        {loading ? 'Analyzing...' : 'Analyze Compatibility'}
      </button>

      {mode3Result && mode3Result.status === 'success' && (
        <Mode3Results
          overallScore={mode3Result.data.overall_score}
          vectorComponent={mode3Result.data.vector_component}
          ruleComponent={mode3Result.data.rule_component}
          emotionalSync={mode3Result.data.emotional_sync}
          chemistryIndex={mode3Result.data.chemistry_index}
          stabilityIndex={mode3Result.data.stability_index}
          strengths={mode3Result.data.strengths}
          challenges={mode3Result.data.challenges}
          narrative={mode3Result.data.narrative}
        />
      )}
    </div>
  );
};

export default Mode3Page;
