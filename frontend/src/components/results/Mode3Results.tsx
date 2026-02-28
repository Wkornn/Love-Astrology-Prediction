interface Mode3ResultsProps {
  overallScore: number;
  vectorComponent: number;
  ruleComponent: number;
  emotionalSync: number;
  chemistryIndex: number;
  stabilityIndex: number;
  strengths: string[];
  challenges: string[];
  diagnostics?: Array<{
    code: string;
    severity: string;
    message: string;
    recommendation: string;
  }>;
}

export const Mode3Results = ({
  overallScore,
  vectorComponent,
  ruleComponent,
  emotionalSync,
  chemistryIndex,
  stabilityIndex,
  strengths,
  challenges,
  diagnostics = [],
}: Mode3ResultsProps) => {
  const getScoreColor = (score: number) => {
    if (score >= 75) return '#00d9ff';
    if (score >= 50) return '#8b5cf6';
    return '#f59e0b';
  };

  const formatScore = (val: number) => Math.round(val);

  return (
    <div className="space-y-6">
      {/* Overall Score */}
      <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-8 text-center">
        <div className="text-sm text-gray-400 mb-2">OVERALL COMPATIBILITY</div>
        <div className="text-7xl font-bold mb-2" style={{ color: getScoreColor(overallScore) }}>
          {formatScore(overallScore)}%
        </div>
        <div className="flex justify-center gap-6 text-sm">
          <div>
            <span className="text-gray-400">Vector: </span>
            <span className="text-[#8b5cf6] font-semibold">{formatScore(vectorComponent)}%</span>
          </div>
          <div>
            <span className="text-gray-400">Rules: </span>
            <span className="text-[#00d9ff] font-semibold">{formatScore(ruleComponent)}%</span>
          </div>
        </div>
      </div>

      {/* Compatibility Indices */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-6">
          <div className="text-xs text-gray-400 mb-2">EMOTIONAL SYNC</div>
          <div className="text-4xl font-bold mb-2" style={{ color: getScoreColor(emotionalSync) }}>
            {formatScore(emotionalSync)}%
          </div>
          <div className="h-2 bg-[#1a1a24] rounded-full overflow-hidden">
            <div
              className="h-full bg-[#00d9ff]"
              style={{ width: `${emotionalSync}%` }}
            />
          </div>
        </div>

        <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-6">
          <div className="text-xs text-gray-400 mb-2">CHEMISTRY INDEX</div>
          <div className="text-4xl font-bold mb-2" style={{ color: getScoreColor(chemistryIndex) }}>
            {formatScore(chemistryIndex)}%
          </div>
          <div className="h-2 bg-[#1a1a24] rounded-full overflow-hidden">
            <div
              className="h-full bg-[#8b5cf6]"
              style={{ width: `${chemistryIndex}%` }}
            />
          </div>
        </div>

        <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-6">
          <div className="text-xs text-gray-400 mb-2">STABILITY INDEX</div>
          <div className="text-4xl font-bold mb-2" style={{ color: getScoreColor(stabilityIndex) }}>
            {formatScore(stabilityIndex)}%
          </div>
          <div className="h-2 bg-[#1a1a24] rounded-full overflow-hidden">
            <div
              className="h-full bg-[#00d9ff]"
              style={{ width: `${stabilityIndex}%` }}
            />
          </div>
        </div>
      </div>

      {/* Strengths & Challenges */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Strengths */}
        <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-6">
          <h3 className="text-lg font-semibold text-[#00d9ff] mb-4 flex items-center gap-2">
            <span>✓</span> STRENGTHS
          </h3>
          <div className="space-y-3">
            {strengths.map((strength, idx) => (
              <div key={idx} className="flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-[#00d9ff] mt-2 flex-shrink-0" />
                <p className="text-sm text-gray-300">{strength}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Challenges */}
        <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-6">
          <h3 className="text-lg font-semibold text-[#f59e0b] mb-4 flex items-center gap-2">
            <span>⚠</span> CHALLENGES
          </h3>
          <div className="space-y-3">
            {challenges.map((challenge, idx) => (
              <div key={idx} className="flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-[#f59e0b] mt-2 flex-shrink-0" />
                <p className="text-sm text-gray-300">{challenge}</p>
              </div>
            ))}
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
