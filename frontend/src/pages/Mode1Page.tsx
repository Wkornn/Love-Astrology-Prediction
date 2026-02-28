import { useState } from 'react';
import { BirthDataForm, type BirthData } from '../components/forms/BirthDataForm';
import { Mode1Results } from '../components/results/Mode1Results';
import { validateBirthData } from '../utils/validation';
import { mockMode1Result } from '../data/mockResults';

const Mode1Page = () => {
  const [data, setData] = useState<BirthData>({
    name: '',
    date: '',
    time: '',
    latitude: '',
    longitude: '',
  });
  const [errors, setErrors] = useState<Partial<Record<keyof BirthData, string>>>({});
  const [showResults, setShowResults] = useState(false);

  const handleSubmit = () => {
    const validationErrors = validateBirthData(data);
    setErrors(validationErrors);
    if (Object.keys(validationErrors).length === 0) {
      setShowResults(true);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Mode 1: Love Reading</h1>
        <p className="text-[#a0a6b0]">Single-person natal chart analysis</p>
      </div>

      <BirthDataForm data={data} onChange={setData} errors={errors} />

      <button
        onClick={handleSubmit}
        className="w-full mt-6 bg-[#8b5cf6] hover:bg-[#7c3aed] text-white font-semibold py-3 px-6 rounded-lg transition-colors"
      >
        Generate Love Reading
      </button>

      {showResults && (
        <div className="mt-8">
          <Mode1Results
            loveProfile={mockMode1Result.loveProfile}
            personalityVector={mockMode1Result.personalityVector}
            diagnostics={mockMode1Result.diagnostics}
          />
        </div>
      )}
    </div>
  );
};

export default Mode1Page;
