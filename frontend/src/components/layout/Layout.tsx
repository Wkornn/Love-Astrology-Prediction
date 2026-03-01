import type { ReactNode } from 'react';
import { useBirthData } from '../../context/BirthDataContext';
import { BirthDataForm } from '../forms/BirthDataForm';
import { validateBirthData } from '../../utils/validation';
import { useState } from 'react';
import Header from './Header';
import Footer from './Footer';

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const { birthData, setBirthData, clearBirthData } = useBirthData();
  const [errors, setErrors] = useState<Partial<Record<keyof typeof birthData, string>>>({});

  const handleClear = () => {
    clearBirthData();
    setErrors({});
  };

  const handleChange = (data: typeof birthData) => {
    setBirthData(data);
    setErrors(validateBirthData(data));
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Shared Birth Data Form */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-[#B5A593]">Your Birth Data</h2>
              <button
                onClick={handleClear}
                className="bg-[#4E5564] hover:bg-[#3a3a4a] text-white px-4 py-2 rounded-lg text-sm"
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
