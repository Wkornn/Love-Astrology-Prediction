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
}

export const Mode1Results = ({ loveProfile, personalityVector, diagnostics = [] }: LoveProfileProps) => {
  const getScoreColor = (score: number) => {
    if (score >= 0.75) return '#00d9ff';
    if (score >= 0.5) return '#8b5cf6';
    return '#f59e0b';
  };

  const formatPercent = (val: number) => Math.round(val * 100);

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
    </div>
  );
};
