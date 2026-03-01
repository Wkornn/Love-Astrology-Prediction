interface Mode3ResultsProps {
  overallScore: number;
  vectorComponent: number;
  ruleComponent: number;
  emotionalSync: number;
  chemistryIndex: number;
  stabilityIndex: number;
  strengths: string[];
  challenges: string[];
  narrative?: {
    relationship_summary?: string;
    key_strengths?: string;
    main_challenges?: string;
    conflict_pattern?: string;
    growth_advice?: string;
    drama_explanation?: string;
  };
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
  narrative,
}: Mode3ResultsProps) => {
  const getScoreColor = (score: number) => {
    if (score >= 75) return '#E07A5F';
    if (score >= 50) return '#B5A593';
    return '#f59e0b';
  };

  const formatScore = (val: number) => Math.round(val);

  return (
    <div className="space-y-6">
      {/* Overall Score */}
      <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-8 text-center">
        <div className="text-base text-gray-400 mb-2">OVERALL COMPATIBILITY</div>
        <div className="text-sm text-[#B5A593] mb-3">ความเข้ากันได้โดยรวม</div>
        <div className="text-7xl font-bold mb-2" style={{ color: getScoreColor(overallScore) }}>
          {formatScore(overallScore)}%
        </div>
        <div className="flex justify-center gap-6 text-base">
          <div>
            <span className="text-gray-400">Vector: </span>
            <span className="text-[#B5A593] font-semibold">{formatScore(vectorComponent)}%</span>
          </div>
          <div>
            <span className="text-gray-400">Rules: </span>
            <span className="text-[#E07A5F] font-semibold">{formatScore(ruleComponent)}%</span>
          </div>
        </div>
      </div>

      {/* Compatibility Indices */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6">
          <div className="text-sm text-gray-400 mb-1">EMOTIONAL SYNC</div>
          <div className="text-base text-[#E07A5F] mb-2">ความสอดคล้องทางอารมณ์</div>
          <div className="text-4xl font-bold mb-2" style={{ color: getScoreColor(emotionalSync) }}>
            {formatScore(emotionalSync)}%
          </div>
          <div className="text-sm text-gray-500 mb-3 leading-relaxed">ความเข้าใจและเชื่อมโยงความรู้สึกของกันและกัน</div>
          <div className="h-2 bg-[#2a2d38] rounded-full overflow-hidden">
            <div
              className="h-full bg-[#E07A5F]"
              style={{ width: `${emotionalSync}%` }}
            />
          </div>
        </div>

        <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6">
          <div className="text-sm text-gray-400 mb-1">CHEMISTRY INDEX</div>
          <div className="text-base text-[#B5A593] mb-2">ดัชนีควาวมเคมี</div>
          <div className="text-4xl font-bold mb-2" style={{ color: getScoreColor(chemistryIndex) }}>
            {formatScore(chemistryIndex)}%
          </div>
          <div className="text-sm text-gray-500 mb-3 leading-relaxed">ความดึงดูดและประกายไฟระหว่างกัน</div>
          <div className="h-2 bg-[#2a2d38] rounded-full overflow-hidden">
            <div
              className="h-full bg-[#B5A593]"
              style={{ width: `${chemistryIndex}%` }}
            />
          </div>
        </div>

        <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6">
          <div className="text-sm text-gray-400 mb-1">STABILITY INDEX</div>
          <div className="text-base text-[#E07A5F] mb-2">ดัชนีความมั่นคง</div>
          <div className="text-4xl font-bold mb-2" style={{ color: getScoreColor(stabilityIndex) }}>
            {formatScore(stabilityIndex)}%
          </div>
          <div className="text-sm text-gray-500 mb-3 leading-relaxed">ความยั่งยืนและมั่นคงของความสัมพันธ์</div>
          <div className="h-2 bg-[#2a2d38] rounded-full overflow-hidden">
            <div
              className="h-full bg-[#E07A5F]"
              style={{ width: `${stabilityIndex}%` }}
            />
          </div>
        </div>
      </div>

      {/* Strengths & Challenges */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {/* Strengths */}
        <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6">
          <h3 className="text-lg font-semibold text-[#E07A5F] mb-4 flex items-center gap-2">
            <span>✓</span> STRENGTHS
          </h3>
          <div className="space-y-3">
            {strengths.map((strength, idx) => (
              <div key={idx} className="flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-[#E07A5F] mt-2 flex-shrink-0" />
                <p className="text-base text-gray-300 leading-relaxed">{strength}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Challenges */}
        <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6">
          <h3 className="text-lg font-semibold text-[#f59e0b] mb-4 flex items-center gap-2">
            <span>⚠</span> CHALLENGES
          </h3>
          <div className="space-y-3">
            {challenges.map((challenge, idx) => (
              <div key={idx} className="flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-[#f59e0b] mt-2 flex-shrink-0" />
                <p className="text-base text-gray-300 leading-relaxed">{challenge}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* LLM Narrative */}
      {narrative && (
        <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6">
          <h3 className="text-lg font-semibold text-[#B5A593] mb-4">💫 ดวงดาวบอกอะไร</h3>
          <div className="space-y-4">
            {narrative.relationship_summary && (
              <div className="bg-[#2a2d38] rounded-lg p-4 border-l-2 border-[#B5A593]">
                <div className="text-sm text-[#B5A593] mb-2 font-semibold">สรุปความสัมพันธ์</div>
                <p className="text-base text-gray-300 leading-relaxed">{narrative.relationship_summary}</p>
              </div>
            )}
            {narrative.key_strengths && (
              <div className="bg-[#2a2d38] rounded-lg p-4 border-l-2 border-[#E07A5F]">
                <div className="text-sm text-[#E07A5F] mb-2 font-semibold">จุดแข็ง</div>
                <p className="text-base text-gray-300 leading-relaxed">{narrative.key_strengths}</p>
              </div>
            )}
            {narrative.main_challenges && (
              <div className="bg-[#2a2d38] rounded-lg p-4 border-l-2 border-[#f59e0b]">
                <div className="text-sm text-[#f59e0b] mb-2 font-semibold">จุดที่ต้องระวัง</div>
                <p className="text-base text-gray-300 leading-relaxed">{narrative.main_challenges}</p>
              </div>
            )}
            {narrative.conflict_pattern && (
              <div className="bg-[#2a2d38] rounded-lg p-4 border-l-2 border-[#ef4444]">
                <div className="text-sm text-[#ef4444] mb-2 font-semibold">รูปแบบความขัดแย้ง</div>
                <p className="text-base text-gray-300 leading-relaxed">{narrative.conflict_pattern}</p>
              </div>
            )}
            {narrative.growth_advice && (
              <div className="bg-[#2a2d38] rounded-lg p-4 border-l-2 border-[#10b981]">
                <div className="text-sm text-[#10b981] mb-2 font-semibold">คำแนะนำ</div>
                <p className="text-base text-gray-300 leading-relaxed">{narrative.growth_advice}</p>
              </div>
            )}
            {narrative.drama_explanation && (
              <div className="bg-[#2a2d38] rounded-lg p-4 border-l-2 border-[#f59e0b]">
                <p className="text-base text-gray-300 italic leading-relaxed">🎭 {narrative.drama_explanation}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
