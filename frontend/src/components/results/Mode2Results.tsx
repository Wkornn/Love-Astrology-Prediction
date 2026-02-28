interface CelebrityMatch {
  name: string;
  occupation?: string;
  similarity_score: number;
  match_reason: string;
  narrative?: {
    funny_joke?: string;
  };
}

interface Mode2ResultsProps {
  matches: CelebrityMatch[];
  userVector: Record<string, number>;
  totalCelebrities: number;
}

export const Mode2Results = ({ matches, userVector, totalCelebrities }: Mode2ResultsProps) => {
  const formatPercent = (val: number) => Math.round(val);

  return (
    <div className="space-y-6">
      {/* Stats Header */}
      <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-6 text-center">
        <div className="text-sm text-gray-400 mb-2">ANALYZED AGAINST</div>
        <div className="text-4xl font-bold text-[#00d9ff] mb-1">{totalCelebrities}</div>
        <div className="text-sm text-gray-500">Public Figures</div>
      </div>

      {/* Top Matches */}
      <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-6">
        <h3 className="text-lg font-semibold text-[#8b5cf6] mb-4">TOP CELEBRITY MATCHES</h3>
        <div className="space-y-4">
          {matches.map((match, idx) => (
            <div
              key={idx}
              className="bg-[#1a1a24] border border-[#2a2a3a] rounded-lg p-5 hover:border-[#8b5cf6] transition-colors"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-1">
                    <span className="text-2xl font-bold text-[#00d9ff]">#{idx + 1}</span>
                    <div>
                      <h4 className="text-lg font-bold text-white">{match.name}</h4>
                      {match.occupation && (
                        <p className="text-sm text-gray-400">{match.occupation}</p>
                      )}
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-[#8b5cf6]">
                    {formatPercent(match.similarity_score)}%
                  </div>
                  <div className="text-xs text-gray-400">MATCH</div>
                </div>
              </div>
              <div className="bg-[#0f0f14] rounded px-3 py-2 border-l-2 border-[#00d9ff]">
                <p className="text-sm text-gray-300">{match.match_reason}</p>
              </div>
              
              {/* Funny Joke */}
              {match.narrative?.funny_joke && (
                <div className="mt-3 bg-[#1a1a24] rounded-lg p-3 border-l-2 border-[#f59e0b]">
                  <p className="text-sm text-gray-300 italic">😄 {match.narrative.funny_joke}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Your Profile Summary */}
      <div className="bg-[#0f0f14] border border-[#2a2a3a] rounded-xl p-6">
        <h3 className="text-lg font-semibold text-[#8b5cf6] mb-4">YOUR PROFILE SUMMARY</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {Object.entries(userVector).slice(0, 8).map(([key, value]) => (
            <div key={key} className="bg-[#1a1a24] rounded-lg p-3 text-center">
              <div className="text-lg font-bold text-[#00d9ff]">
                {Math.round(value * 100)}%
              </div>
              <div className="text-xs text-gray-400 mt-1">
                {key.replace(/_/g, ' ').toUpperCase()}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
