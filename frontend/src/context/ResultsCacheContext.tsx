import { createContext, useContext, useState, type ReactNode } from 'react';
import type { Mode1Response, Mode2Response, Mode3Response } from '../services/api';

interface ResultsCacheContextType {
  mode1Result: Mode1Response | null;
  mode2Result: Mode2Response | null;
  mode3Result: Mode3Response | null;
  setMode1Result: (result: Mode1Response | null) => void;
  setMode2Result: (result: Mode2Response | null) => void;
  setMode3Result: (result: Mode3Response | null) => void;
  clearAllResults: () => void;
}

const ResultsCacheContext = createContext<ResultsCacheContextType | undefined>(undefined);

export const ResultsCacheProvider = ({ children }: { children: ReactNode }) => {
  const [mode1Result, setMode1Result] = useState<Mode1Response | null>(null);
  const [mode2Result, setMode2Result] = useState<Mode2Response | null>(null);
  const [mode3Result, setMode3Result] = useState<Mode3Response | null>(null);

  const clearAllResults = () => {
    setMode1Result(null);
    setMode2Result(null);
    setMode3Result(null);
  };

  return (
    <ResultsCacheContext.Provider value={{ 
      mode1Result, mode2Result, mode3Result,
      setMode1Result, setMode2Result, setMode3Result,
      clearAllResults 
    }}>
      {children}
    </ResultsCacheContext.Provider>
  );
};

export const useResultsCache = () => {
  const context = useContext(ResultsCacheContext);
  if (!context) throw new Error('useResultsCache must be used within ResultsCacheProvider');
  return context;
};
