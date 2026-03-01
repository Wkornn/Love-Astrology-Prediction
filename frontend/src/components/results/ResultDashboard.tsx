interface LoveBug {
  code: string;
  severity: 'CRITICAL' | 'WARNING' | 'INFO';
  message: string;
  recommendation: string;
}

interface ResultDashboardProps {
  compatibilityScore?: number;
  emotionalSync?: number;
  chemistryIndex?: number;
  stabilityIndex?: number;
  loveBugs: LoveBug[];
  systemStatus: string;
}

export const ResultDashboard = ({
  compatibilityScore,
  emotionalSync,
  chemistryIndex,
  stabilityIndex,
  loveBugs,
  systemStatus,
}: ResultDashboardProps) => {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'CRITICAL': return '#ef4444';
      case 'WARNING': return '#f59e0b';
      case 'INFO': return '#E07A5F';
      default: return '#6b7280';
    }
  };

  return (
    <div className="space-y-6">
      {/* Compatibility Score */}
      {compatibilityScore !== undefined && (
        <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-8 text-center">
          <div className="text-sm text-gray-400 mb-2">COMPATIBILITY SCORE</div>
          <div className="text-7xl font-bold text-[#B5A593] mb-2">
            {compatibilityScore}%
          </div>
          <div className="text-sm text-gray-500">{systemStatus}</div>
        </div>
      )}

      {/* Metrics Grid */}
      {(emotionalSync !== undefined || chemistryIndex !== undefined || stabilityIndex !== undefined) && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {emotionalSync !== undefined && (
            <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6">
              <div className="text-xs text-gray-400 mb-2">EMOTIONAL SYNC</div>
              <div className="text-3xl font-bold text-[#E07A5F]">{emotionalSync}%</div>
            </div>
          )}
          {chemistryIndex !== undefined && (
            <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6">
              <div className="text-xs text-gray-400 mb-2">CHEMISTRY INDEX</div>
              <div className="text-3xl font-bold text-[#B5A593]">{chemistryIndex}%</div>
            </div>
          )}
          {stabilityIndex !== undefined && (
            <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6">
              <div className="text-xs text-gray-400 mb-2">STABILITY INDEX</div>
              <div className="text-3xl font-bold text-[#E07A5F]">{stabilityIndex}%</div>
            </div>
          )}
        </div>
      )}

      {/* Radar Chart Placeholder */}
      <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-8">
        <div className="text-sm text-gray-400 mb-4">COMPATIBILITY ANALYSIS</div>
        <div className="h-64 flex items-center justify-center border-2 border-dashed border-[#4E5564] rounded-lg">
          <div className="text-center text-gray-500">
            <div className="text-4xl mb-2">📊</div>
            <div>Radar Chart Placeholder</div>
          </div>
        </div>
      </div>

      {/* Diagnostic Panel */}
      <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6">
        <div className="text-sm text-gray-400 mb-4">DIAGNOSTIC PANEL</div>
        <div className="space-y-3">
          {loveBugs.map((bug, index) => (
            <div
              key={index}
              className="bg-[#2a2d38] border border-[#4E5564] rounded-lg p-4"
            >
              <div className="flex items-start gap-3">
                <div
                  className="w-2 h-2 rounded-full mt-2 flex-shrink-0"
                  style={{ backgroundColor: getSeverityColor(bug.severity) }}
                />
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-mono text-gray-400">{bug.code}</span>
                    <span
                      className="text-xs font-semibold"
                      style={{ color: getSeverityColor(bug.severity) }}
                    >
                      {bug.severity}
                    </span>
                  </div>
                  <div className="text-sm text-white mb-2">{bug.message}</div>
                  <div className="text-xs text-gray-400">{bug.recommendation}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
