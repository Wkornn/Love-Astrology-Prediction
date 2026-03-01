import { createContext, useContext, useState, ReactNode } from 'react';
import type { BirthData } from '../components/forms/BirthDataForm';

interface BirthDataContextType {
  birthData: BirthData;
  setBirthData: (data: BirthData) => void;
  clearBirthData: () => void;
}

const BirthDataContext = createContext<BirthDataContextType | undefined>(undefined);

const initialData: BirthData = {
  date: '',
  time: '',
  latitude: '',
  longitude: '',
};

export const BirthDataProvider = ({ children }: { children: ReactNode }) => {
  const [birthData, setBirthData] = useState<BirthData>(initialData);

  const clearBirthData = () => setBirthData(initialData);

  return (
    <BirthDataContext.Provider value={{ birthData, setBirthData, clearBirthData }}>
      {children}
    </BirthDataContext.Provider>
  );
};

export const useBirthData = () => {
  const context = useContext(BirthDataContext);
  if (!context) throw new Error('useBirthData must be used within BirthDataProvider');
  return context;
};
