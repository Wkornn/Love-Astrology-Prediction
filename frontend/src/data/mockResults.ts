export const mockMode1Result = {
  loveProfile: {
    romantic_readiness: 0.78,
    passion_drive: 0.85,
    emotional_depth: 0.72,
    commitment_capacity: 0.68,
  },
  personalityVector: {
    venus_mars_harmony: 0.82,
    sun_moon_balance: 0.75,
    moon_stability: 0.71,
    fire_score: 0.65,
    earth_score: 0.45,
    air_score: 0.58,
    water_score: 0.72,
    hard_aspect_density: 0.38,
    soft_aspect_density: 0.62,
  },
  diagnostics: [
    {
      code: 'LOVE_VENUS_001',
      severity: 'INFO',
      message: 'Strong Venus placement indicates natural charm and romantic appeal',
      recommendation: 'Leverage your natural magnetism while maintaining authenticity in relationships',
    },
    {
      code: 'LOVE_MARS_002',
      severity: 'WARNING',
      message: 'High passion drive may lead to impulsive romantic decisions',
      recommendation: 'Practice patience and allow relationships to develop naturally over time',
    },
  ],
};

export const mockMode2Result = {
  matches: [
    {
      name: 'Taylor Swift',
      occupation: 'Singer-Songwriter',
      similarity_score: 87.5,
      match_reason: 'Similar romantic expression and emotional depth',
    },
    {
      name: 'Ryan Gosling',
      occupation: 'Actor',
      similarity_score: 84.2,
      match_reason: 'Compatible emotional balance and communication style',
    },
    {
      name: 'Emma Watson',
      occupation: 'Actress & Activist',
      similarity_score: 81.8,
      match_reason: 'Matching emotional stability and practical approach',
    },
    {
      name: 'Chris Evans',
      occupation: 'Actor',
      similarity_score: 79.3,
      match_reason: 'Shared passionate energy and commitment capacity',
    },
    {
      name: 'Zendaya',
      occupation: 'Actress & Singer',
      similarity_score: 76.9,
      match_reason: 'Compatible astrological profile and elemental balance',
    },
  ],
  userVector: {
    venus_mars_harmony: 0.82,
    sun_moon_balance: 0.75,
    moon_stability: 0.71,
    fire_score: 0.65,
    earth_score: 0.45,
    air_score: 0.58,
    water_score: 0.72,
    hard_aspect_density: 0.38,
  },
  totalCelebrities: 1247,
};

export const mockMode3Result = {
  overallScore: 78.5,
  vectorComponent: 82.3,
  ruleComponent: 74.7,
  emotionalSync: 81.2,
  chemistryIndex: 76.8,
  stabilityIndex: 77.5,
  strengths: [
    'Similar Fire energy - natural understanding and shared enthusiasm',
    'Compatible romantic and passionate expression',
    'Strong emotional synchronization',
  ],
  challenges: [
    'Different Earth expression - requires compromise on practical matters',
    'Emotional differences need attention during stressful periods',
    'Communication styles may clash under pressure',
  ],
  diagnostics: [
    {
      code: 'COMPAT_SYNC_001',
      severity: 'INFO',
      message: 'High compatibility score indicates strong relationship potential',
      recommendation: 'Focus on maintaining open communication and mutual respect',
    },
    {
      code: 'COMPAT_CHALLENGE_002',
      severity: 'WARNING',
      message: 'Moderate aspect tension detected in daily interaction patterns',
      recommendation: 'Establish clear boundaries and conflict resolution protocols',
    },
  ],
};
