import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface BirthDataPayload {
  name: string;
  birth_date: string;
  birth_time: string;
  latitude: number;
  longitude: number;
}

export interface LoveReadingResponse {
  person: BirthDataPayload;
  love_profile: {
    venus_sign: string;
    mars_sign: string;
    moon_sign: string;
    seventh_house_sign: string;
  };
  love_bugs: Array<{
    code: string;
    severity: string;
    message: string;
    recommendation: string;
  }>;
  system_status: string;
}

export interface CelebrityMatchResponse {
  person: BirthDataPayload;
  top_matches: Array<{
    name: string;
    similarity_score: number;
    compatibility_percentage: number;
    match_reason: string;
  }>;
  system_status: string;
}

export interface CoupleMatchResponse {
  person1: BirthDataPayload;
  person2: BirthDataPayload;
  compatibility_score: number;
  emotional_sync: number;
  chemistry_index: number;
  stability_index: number;
  love_bugs: Array<{
    code: string;
    severity: string;
    message: string;
    recommendation: string;
  }>;
  system_status: string;
}

export const submitLoveReading = async (data: BirthDataPayload): Promise<LoveReadingResponse> => {
  const response = await api.post<LoveReadingResponse>('/api/mode1/love-reading', data);
  return response.data;
};

export const submitCelebrityMatch = async (data: BirthDataPayload): Promise<CelebrityMatchResponse> => {
  const response = await api.post<CelebrityMatchResponse>('/api/mode2/celebrity-match', data);
  return response.data;
};

export const submitCoupleMatch = async (
  person1: BirthDataPayload,
  person2: BirthDataPayload
): Promise<CoupleMatchResponse> => {
  const response = await api.post<CoupleMatchResponse>('/api/mode3/couple-match', {
    person1,
    person2,
  });
  return response.data;
};
