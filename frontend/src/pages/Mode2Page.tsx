import { useState } from 'react';
import { BirthDataForm, type BirthData } from '../components/forms/BirthDataForm';
import { Mode2Results } from '../components/results/Mode2Results';
import { validateBirthData } from '../utils/validation';
import { mockMode2Result } from '../data/mockResults';

const Mode2Page = () => {
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
        <h1 className="text-3xl font-bold mb-2">Mode 2: Celebrity Match</h1>
        <p className="text-[#a0a6b0]">Match against public figure database</p>
      </div>

      <BirthDataForm data={data} onChange={setData} errors={errors} />

      <button
        onClick={handleSubmit}
        className="w-full mt-6 bg-[#00d9ff] hover:bg-[#00c4e6] text-black font-semibold py-3 px-6 rounded-lg transition-colors"
      >
        Find Celebrity Matches
      </button>

      {showResults && (
        <div className="mt-8">
          <Mode2Results
            matches={mockMode2Result.matches}
            userVector={mockMode2Result.userVector}
            totalCelebrities={mockMode2Result.totalCelebrities}
          />
        </div>
      )}
    </div>
  );
};

export default Mode2Page;
