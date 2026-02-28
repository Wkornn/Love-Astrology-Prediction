import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log('[API Request]', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

// Response interceptor for logging
api.interceptors.response.use(
  (response) => {
    console.log('[API Response]', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('[API Response Error]', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

export interface BirthDataPayload {
  date: string;
  time: string;
  latitude: number;
  longitude: number;
  timezone?: string;
}

interface DiagnosticBug {
  code: string;
  severity: 'CRITICAL' | 'WARNING' | 'INFO';
  message: string;
  recommendation: string;
}

interface DiagnosticsSection {
  bugs: DiagnosticBug[];
  system_status?: string;
  drama_risk_level?: string;
  recommendation_summary?: string;
}

interface StandardResponse<T> {
  status: 'success' | 'error';
  mode: string;
  data: T;
  diagnostics: DiagnosticsSection;
  timestamp: string;
}

export interface Mode1Data {
  love_profile: {
    romantic_readiness: number;
    passion_drive: number;
    emotional_depth: number;
    commitment_capacity: number;
  };
  personality_vector: {
    venus_mars_harmony: number;
    sun_moon_balance: number;
    moon_stability: number;
    fire_score: number;
    earth_score: number;
    air_score: number;
    water_score: number;
    hard_aspect_density: number;
    soft_aspect_density: number;
  };
  debug?: {
    aspects?: Array<{
      planet_a: string;
      planet_b: string;
      aspect: string;
      orb: number;
      exact_angle: number;
      strength: number;
    }>;
    aspect_scores?: {
      total_score: number;
      harmonious_count: number;
      challenging_count: number;
      neutral_count: number;
      average_strength: number;
    };
    [key: string]: any;
  };
}

export interface CelebrityMatch {
  name: string;
  occupation?: string;
  similarity_score: number;
  match_reason: string;
}

export interface Mode2Data {
  matches: CelebrityMatch[];
  user_vector: Record<string, number>;
  total_celebrities: number;
}

export interface Mode3Data {
  overall_score: number;
  vector_component: number;
  rule_component: number;
  emotional_sync: number;
  chemistry_index: number;
  stability_index: number;
  strengths: string[];
  challenges: string[];
}

export type Mode1Response = StandardResponse<Mode1Data>;
export type Mode2Response = StandardResponse<Mode2Data>;
export type Mode3Response = StandardResponse<Mode3Data>;

export const submitLoveReading = async (data: BirthDataPayload, debug: boolean = false): Promise<Mode1Response> => {
  const response = await api.post<Mode1Response>('/api/mode1/love-reading', {
    birth_data: data,
    debug,
  });
  return response.data;
};

export const submitCelebrityMatch = async (
  data: BirthDataPayload,
  topN: number = 5
): Promise<Mode2Response> => {
  const response = await api.post<Mode2Response>('/api/mode2/celebrity-match', {
    birth_data: data,
    top_n: topN,
  });
  return response.data;
};

export const submitCoupleMatch = async (
  person1: BirthDataPayload,
  person2: BirthDataPayload
): Promise<Mode3Response> => {
  const response = await api.post<Mode3Response>('/api/mode3/couple-match', {
    person1,
    person2,
  });
  return response.data;
};
