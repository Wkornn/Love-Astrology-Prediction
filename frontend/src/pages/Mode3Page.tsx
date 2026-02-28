import { useState } from 'react';
import { BirthDataForm, type BirthData } from '../components/forms/BirthDataForm';
import { Mode3Results } from '../components/results/Mode3Results';
import { validateBirthData } from '../utils/validation';
import { submitCoupleMatch, type Mode3Response } from '../services/api';

const Mode3Page = () => {
  const [person1, setPerson1] = useState<BirthData>({
    name: '',
    date: '',
    time: '',
    latitude: '',
    longitude: '',
  });
  const [person2, setPerson2] = useState<BirthData>({
    name: '',
    date: '',
    time: '',
    latitude: '',
    longitude: '',
  });
  const [errors1, setErrors1] = useState<Partial<Record<keyof BirthData, string>>>({});
  const [errors2, setErrors2] = useState<Partial<Record<keyof BirthData, string>>>({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);
  const [result, setResult] = useState<Mode3Response | null>(null);

  const handleSubmit = async () => {
    const validationErrors1 = validateBirthData(person1);
    const validationErrors2 = validateBirthData(person2);
    setErrors1(validationErrors1);
    setErrors2(validationErrors2);
    setApiError(null);
    
    if (Object.keys(validationErrors1).length === 0 && Object.keys(validationErrors2).length === 0) {
      setLoading(true);
      console.log('[Mode3] Submitting:', { person1, person2 });
      
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
        
        console.log('[Mode3] Response:', response);
        setResult(response);
      } catch (error: any) {
        console.error('[Mode3] Error:', error);
        const errorMsg = error.response?.data?.error || error.message || 'Failed to analyze compatibility';
        setApiError(errorMsg);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Mode 3: Couple Match</h1>
        <p className="text-[#a0a6b0]">Two-person compatibility analysis</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <BirthDataForm data={person1} onChange={setPerson1} label="Person 1" errors={errors1} />
        <BirthDataForm data={person2} onChange={setPerson2} label="Person 2" errors={errors2} />
      </div>

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
        {loading ? 'Analyzing...' : 'Analyze Compatibility'}
      </button>

      {result && result.status === 'success' && (
        <div className="mt-8">
          <Mode3Results
            overallScore={result.data.overall_score}
            vectorComponent={result.data.vector_component}
            ruleComponent={result.data.rule_component}
            emotionalSync={result.data.emotional_sync}
            chemistryIndex={result.data.chemistry_index}
            stabilityIndex={result.data.stability_index}
            strengths={result.data.strengths}
            challenges={result.data.challenges}
            diagnostics={result.diagnostics.bugs}
          />
        </div>
      )}
    </div>
  );
};

export default Mode3Page;
