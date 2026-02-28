interface LoveProfileProps {
  loveProfile: {
    romantic_readiness: number;
    passion_drive: number;
    emotional_depth: number;
    commitment_capacity: number;
  };
  personalityVector: {
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
  diagnostics?: Array<{
    code: string;
    severity: string;
    message: string;
    recommendation: string;
  }>;
  aspects?: Array<{
    planet_a: string;
    planet_b: string;
    aspect: string;
    orb: number;
    exact_angle: number;
    strength: number;
  }>;
  aspectScores?: {
    total_score: number;
    harmonious_count: number;
    challenging_count: number;
    neutral_count: number;
    average_strength: number;
  };
}

export const Mode1Results = ({ loveProfile, personalityVector, diagnostics = [], aspects, aspectScores }: LoveProfileProps) => {
  const getScoreColor = (score: number) => {
    // Normalize to 0-1 range if it's a percentage
    const normalized = score > 1 ? score / 100 : score;
    if (normalized >= 0.75) return '#00d9ff';
    if (normalized >= 0.5) return '#8b5cf6';
    return '#f59e0b';
  };

  const formatPercent = (val: number) => {
    // Backend returns love_profile as percentages (50.0) and personality_vector as decimals (0.5)
    // If value > 1, it's already a percentage
    if (val > 1) {
      return Math.round(val);
    }
    return Math.round(val * 100);
  };

  const getAspectColor = (aspect: string) => {
    if (aspect === 'Trine' || aspect === 'Sextile') return '#00d9ff';
    if (aspect === 'Square' || aspect === 'Opposition') return '#f59e0b';
    return '#8b5cf6';
  };

  return (
    <div className="space-y-6">
      {/* Love Profile Metrics */}
      <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-6">
        <h3 className="text-lg font-semibold text-[#8b5cf6] mb-4">LOVE PROFILE</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(loveProfile).map(([key, value]) => (
            <div key={key} className="text-center">
              <div className="text-2xl font-bold mb-1" style={{ color: getScoreColor(value) }}>
                {formatPercent(value)}%
              </div>
              <div className="text-xs text-gray-400 uppercase">
                {key.replace(/_/g, ' ')}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Element Distribution */}
      <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-6">
        <h3 className="text-lg font-semibold text-[#8b5cf6] mb-4">ELEMENTAL PROFILE</h3>
        <div className="space-y-3">
          {['fire_score', 'earth_score', 'air_score', 'water_score'].map((element) => {
            const value = personalityVector[element as keyof typeof personalityVector];
            const name = element.replace('_score', '').toUpperCase();
            return (
              <div key={element}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-300">{name}</span>
                  <span className="text-[#00d9ff]">{formatPercent(value)}%</span>
                </div>
                <div className="h-2 bg-[#1a1a24] rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-[#8b5cf6] to-[#00d9ff]"
                    style={{ width: `${formatPercent(value)}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Personality Insights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-4">
          <div className="text-xs text-gray-400 mb-1">VENUS-MARS HARMONY</div>
          <div className="text-2xl font-bold text-[#8b5cf6]">
            {formatPercent(personalityVector.venus_mars_harmony)}%
          </div>
        </div>
        <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-4">
          <div className="text-xs text-gray-400 mb-1">SUN-MOON BALANCE</div>
          <div className="text-2xl font-bold text-[#00d9ff]">
            {formatPercent(personalityVector.sun_moon_balance)}%
          </div>
        </div>
        <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-4">
          <div className="text-xs text-gray-400 mb-1">EMOTIONAL STABILITY</div>
          <div className="text-2xl font-bold text-[#8b5cf6]">
            {formatPercent(personalityVector.moon_stability)}%
          </div>
        </div>
      </div>

      {/* Diagnostics */}
      {diagnostics.length > 0 && (
        <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-6">
          <h3 className="text-lg font-semibold text-[#8b5cf6] mb-4">DIAGNOSTIC INSIGHTS</h3>
          <div className="space-y-3">
            {diagnostics.map((diag, idx) => (
              <div key={idx} className="bg-[#1a1a24] border border-[#2a2a3a] rounded-lg p-4">
                <div className="flex items-start gap-3">
                  <div className="text-sm font-mono text-gray-400">{diag.code}</div>
                  <div className="flex-1">
                    <div className="text-sm text-white mb-1">{diag.message}</div>
                    <div className="text-xs text-gray-400">{diag.recommendation}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Aspect Engine Data */}
      {aspects && aspects.length > 0 && (
        <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-6">
          <h3 className="text-lg font-semibold text-[#8b5cf6] mb-4">ASPECT ENGINE DATA</h3>
          
          {/* Aspect Summary */}
          {aspectScores && (
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
              <div className="bg-[#1a1a24] rounded-lg p-3 text-center">
                <div className="text-xs text-gray-400 mb-1">TOTAL</div>
                <div className="text-xl font-bold text-white">{aspects.length}</div>
              </div>
              <div className="bg-[#1a1a24] rounded-lg p-3 text-center">
                <div className="text-xs text-gray-400 mb-1">HARMONIOUS</div>
                <div className="text-xl font-bold text-[#00d9ff]">{aspectScores.harmonious_count}</div>
              </div>
              <div className="bg-[#1a1a24] rounded-lg p-3 text-center">
                <div className="text-xs text-gray-400 mb-1">CHALLENGING</div>
                <div className="text-xl font-bold text-[#f59e0b]">{aspectScores.challenging_count}</div>
              </div>
              <div className="bg-[#1a1a24] rounded-lg p-3 text-center">
                <div className="text-xs text-gray-400 mb-1">NEUTRAL</div>
                <div className="text-xl font-bold text-[#8b5cf6]">{aspectScores.neutral_count}</div>
              </div>
              <div className="bg-[#1a1a24] rounded-lg p-3 text-center">
                <div className="text-xs text-gray-400 mb-1">AVG STRENGTH</div>
                <div className="text-xl font-bold text-white">{aspectScores.average_strength.toFixed(2)}</div>
              </div>
            </div>
          )}

          {/* Aspect List */}
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {aspects.map((aspect, idx) => (
              <div key={idx} className="bg-[#1a1a24] border border-[#2a2a3a] rounded-lg p-3 flex items-center justify-between">
                <div className="flex items-center gap-3 flex-1">
                  <div className="text-sm font-semibold text-white">
                    {aspect.planet_a} <span className="text-gray-500">→</span> {aspect.planet_b}
                  </div>
                  <div 
                    className="px-2 py-1 rounded text-xs font-semibold"
                    style={{ 
                      backgroundColor: getAspectColor(aspect.aspect) + '20',
                      color: getAspectColor(aspect.aspect)
                    }}
                  >
                    {aspect.aspect}
                  </div>
                </div>
                <div className="flex items-center gap-4 text-xs">
                  <div>
                    <span className="text-gray-400">Orb:</span>
                    <span className="text-white ml-1">{aspect.orb.toFixed(2)}°</span>
                  </div>
                  <div>
                    <span className="text-gray-400">Strength:</span>
                    <span className="text-[#00d9ff] ml-1">{(aspect.strength * 100).toFixed(0)}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
