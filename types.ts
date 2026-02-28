// Core TypeScript Data Structures for Love Debugging Lab v2.0

export type ZodiacSign = 
  | 'Aries' | 'Taurus' | 'Gemini' | 'Cancer' 
  | 'Leo' | 'Virgo' | 'Libra' | 'Scorpio' 
  | 'Sagittarius' | 'Capricorn' | 'Aquarius' | 'Pisces';

export type PlanetName = 'Sun' | 'Moon' | 'Mercury' | 'Venus' | 'Mars' | 'Jupiter' | 'Saturn';

export type AspectType = 'Conjunction' | 'Opposition' | 'Trine' | 'Square' | 'Sextile';

export interface Planet {
  name: PlanetName;
  sign: ZodiacSign;
  degree: number;
  house: number;
}

export interface Aspect {
  planetA: PlanetName;
  planetB: PlanetName;
  type: AspectType;
  orb: number;
  angle: number;
}

export interface BirthChart {
  planets: Planet[];
  aspects: Aspect[];
  ascendant?: ZodiacSign;
}

export interface BirthData {
  date: string;
  time: string;
  latitude: number;
  longitude: number;
  timezone: string;
}

export type BugSeverity = 'CRITICAL' | 'WARNING' | 'INFO';

export interface LoveBug {
  severity: BugSeverity;
  code: string;
  message: string;
  stackTrace?: string;
}

export interface CompatibilityScores {
  emotional: number;
  physical: number;
  stability: number;
  drama: number;
  overall: number;
}

export interface CompatibilityResult {
  archetype: string;
  scores: CompatibilityScores;
  bugs: LoveBug[];
  emotionalRiskIndex: number;
  forecast: string[];
  debugSummary: string;
}
