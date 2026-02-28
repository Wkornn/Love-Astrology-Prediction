import { useState } from 'react';
import { BirthDataForm, type BirthData } from '../components/forms/BirthDataForm';
import { Mode3Results } from '../components/results/Mode3Results';
import { validateBirthData } from '../utils/validation';
import { mockMode3Result } from '../data/mockResults';

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
  const [showResults, setShowResults] = useState(false);

  const handleSubmit = () => {
    const validationErrors1 = validateBirthData(person1);
    const validationErrors2 = validateBirthData(person2);
    setErrors1(validationErrors1);
    setErrors2(validationErrors2);
    if (Object.keys(validationErrors1).length === 0 && Object.keys(validationErrors2).length === 0) {
      setShowResults(true);
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

      <button
        onClick={handleSubmit}
        className="w-full mt-6 bg-[#8b5cf6] hover:bg-[#7c3aed] text-white font-semibold py-3 px-6 rounded-lg transition-colors"
      >
        Analyze Compatibility
      </button>

      {showResults && (
        <div className="mt-8">
          <Mode3Results
            overallScore={mockMode3Result.overallScore}
            vectorComponent={mockMode3Result.vectorComponent}
            ruleComponent={mockMode3Result.ruleComponent}
            emotionalSync={mockMode3Result.emotionalSync}
            chemistryIndex={mockMode3Result.chemistryIndex}
            stabilityIndex={mockMode3Result.stabilityIndex}
            strengths={mockMode3Result.strengths}
            challenges={mockMode3Result.challenges}
            diagnostics={mockMode3Result.diagnostics}
          />
        </div>
      )}
    </div>
  );
};

export default Mode3Page;
