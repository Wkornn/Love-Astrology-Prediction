import type { ReactNode } from 'react';
import { useBirthData } from '../../context/BirthDataContext';
import { useResultsCache } from '../../context/ResultsCacheContext';
import { BirthDataForm } from '../forms/BirthDataForm';
import { validateBirthData } from '../../utils/validation';
import { useState } from 'react';
import Footer from './Footer';

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const { birthData, setBirthData, clearBirthData } = useBirthData();
  const { clearAllResults } = useResultsCache();
  const [errors, setErrors] = useState<Partial<Record<keyof typeof birthData, string>>>({});

  const handleClear = () => {
    clearBirthData();
    clearAllResults();
    setErrors({});
  };

  const handleChange = (data: typeof birthData) => {
    setBirthData(data);
    setErrors(validateBirthData(data));
  };

  return (
    <div className="min-h-screen flex flex-col">
      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Title */}
          <div className="text-center mb-12">
            <h1 className="text-5xl xl:text-6xl font-bold mb-4 pb-2 bg-gradient-to-r from-[#B5A593] to-[#E07A5F] bg-clip-text text-transparent drop-shadow-lg">
              Love Debugging Lab
            </h1>
            <p className="text-[#e0e6ed] text-lg font-medium drop-shadow-md">Professional Astrological Compatibility System</p>
          </div>

          {/* Shared Birth Data Form */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-[#e0e6ed] drop-shadow-md">Your Birth Data</h2>
              <button
                onClick={handleClear}
                className="bg-[#2a2a3a]/80 backdrop-blur-sm hover:bg-[#3a3a4a]/80 text-white px-4 py-2 rounded-lg text-sm border border-[#4E5564]/50"
              >
                Clear All
              </button>
            </div>
            <BirthDataForm data={birthData} onChange={handleChange} errors={errors} />
          </div>

          {/* Page Content */}
          {children}
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Layout;
