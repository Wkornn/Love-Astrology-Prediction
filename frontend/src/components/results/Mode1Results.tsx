import { LoveVector3D } from '../visualizations/LoveVector3D';

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
  narrative?: {
    headline?: string;
    personality_summary?: string;
    love_style?: string;
    emotional_pattern?: string;
    relationship_advice?: string;
    bug_explanation?: string;
  };
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

export const Mode1Results = ({ loveProfile, personalityVector, diagnostics = [], narrative, aspects, aspectScores }: LoveProfileProps) => {
  const getScoreColor = (score: number) => {
    // Normalize to 0-1 range if it's a percentage
    const normalized = score > 1 ? score / 100 : score;
    if (normalized >= 0.75) return '#E07A5F';
    if (normalized >= 0.5) return '#B5A593';
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
    if (aspect === 'Trine' || aspect === 'Sextile') return '#E07A5F';
    if (aspect === 'Square' || aspect === 'Opposition') return '#f59e0b';
    return '#B5A593';
  };

  return (
    <div className="space-y-6">
      {/* Vector Visualization */}
      <LoveVector3D 
        emotionalIntensity={loveProfile.emotional_maturity || 0}
        passionIndex={loveProfile.passion_level || 0}
        conflictReactivity={loveProfile.relationship_focus || 0}
      />

      {/* LLM Narrative Section */}
      {narrative && (
        <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6">
          {narrative.headline && (
            <h2 className="text-2xl font-bold text-[#E07A5F] mb-4">{narrative.headline}</h2>
          )}
          {narrative.personality_summary && (
            <p className="text-gray-300 mb-4 text-lg leading-relaxed">{narrative.personality_summary}</p>
          )}
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-4 mt-4">
            {narrative.love_style && (
              <div className="bg-[#2a2d38] rounded-lg p-4">
                <div className="text-sm text-[#B5A593] font-semibold mb-2">LOVE STYLE</div>
                <p className="text-base text-gray-300 leading-relaxed">{narrative.love_style}</p>
              </div>
            )}
            {narrative.emotional_pattern && (
              <div className="bg-[#2a2d38] rounded-lg p-4">
                <div className="text-sm text-[#E07A5F] font-semibold mb-2">EMOTIONAL PATTERN</div>
                <p className="text-base text-gray-300 leading-relaxed">{narrative.emotional_pattern}</p>
              </div>
            )}
          </div>
          {narrative.relationship_advice && (
            <div className="bg-[#2a2d38] border-l-2 border-[#B5A593] rounded-lg p-4 mt-4">
              <div className="text-sm text-gray-400 font-semibold mb-2">ADVICE</div>
              <p className="text-base text-gray-300 leading-relaxed">{narrative.relationship_advice}</p>
            </div>
          )}
        </div>
      )}

      {/* Love Profile Metrics */}
      <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6">
        <h3 className="text-lg font-semibold text-[#B5A593] mb-4">LOVE PROFILE</h3>
        <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
          {Object.entries(loveProfile).map(([key, value]) => {
            const descriptions: Record<string, { thai: string; desc: string }> = {
              romantic_readiness: { 
                thai: 'ความพร้อมทางรัก', 
                desc: 'ความพร้อมที่จะเปิดใจรับความรักและเริ่มต้นความสัมพันธ์ใหม่' 
              },
              passion_drive: { 
                thai: 'พลังแห่งความหลงใหล', 
                desc: 'ความเข้มข้นของอารมณ์รักและความปรารถนาในความสัมพันธ์' 
              },
              emotional_depth: { 
                thai: 'ความลึกซึ้งทางอารมณ์', 
                desc: 'ความสามารถในการเข้าใจและแสดงออกทางอารมณ์อย่างลึกซึ้ง' 
              },
              commitment_capacity: { 
                thai: 'ความสามารถในการผูกพัน', 
                desc: 'ความพร้อมที่จะมุ่งมั่นและรักษาความสัมพันธ์ระยะยาว' 
              },
              // Backend actual field names
              love_readiness: { 
                thai: 'ความพร้อมทางรัก', 
                desc: 'ความพร้อมที่จะเปิดใจรับความรักและเริ่มต้นความสัมพันธ์ใหม่' 
              },
              emotional_maturity: { 
                thai: 'ความเป็นผู้ใหญ่ทางอารมณ์', 
                desc: 'ความสามารถในการจัดการอารมณ์และตอบสนองอย่างเหมาะสม' 
              },
              relationship_focus: { 
                thai: 'การมุ่งเน้นความสัมพันธ์', 
                desc: 'ความสำคัญที่ให้กับความสัมพันธ์และการรักษาความผูกพัน' 
              },
              passion_level: { 
                thai: 'ระดับความหลงใหล', 
                desc: 'ความเข้มข้นของอารมณ์รักและความปรารถนา' 
              },
              stability_potential: { 
                thai: 'ศักยภาพความมั่นคง', 
                desc: 'ความสามารถในการสร้างและรักษาความสัมพันธ์ที่มั่นคงยาวนาน' 
              }
            };
            const info = descriptions[key];
            return (
              <div key={key} className="text-center bg-[#2a2d38] rounded-lg p-4">
                <div className="text-2xl font-bold mb-1" style={{ color: getScoreColor(value) }}>
                  {formatPercent(value)}%
                </div>
                <div className="text-sm text-gray-400 uppercase mb-2">
                  {key.replace(/_/g, ' ')}
                </div>
                {info && (
                  <>
                    <div className="text-sm text-[#B5A593] mb-2">{info.thai}</div>
                    <div className="text-sm text-gray-500 leading-relaxed">{info.desc}</div>
                  </>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Element Distribution */}
      <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6">
        <h3 className="text-lg font-semibold text-[#B5A593] mb-4">ELEMENTAL PROFILE</h3>
        <p className="text-base text-gray-400 mb-4 leading-relaxed">องค์ประกอบธาตุทั้ง 4 ที่สะท้อนบุคลิกภาพและพลังงานภายในของคุณ</p>
        <div className="space-y-3">
          {['fire_score', 'earth_score', 'air_score', 'water_score'].map((element) => {
            const value = personalityVector[element as keyof typeof personalityVector];
            const name = element.replace('_score', '').toUpperCase();
            const descriptions: Record<string, { thai: string; desc: string }> = {
              fire_score: { thai: 'ไฟ', desc: 'ความกระตือรือร้น ความมั่นใจ และพลังแห่งการกระทำ' },
              earth_score: { thai: 'ดิน', desc: 'ความมั่นคง ความจริงจัง และความรับผิดชอบ' },
              air_score: { thai: 'ลม', desc: 'ความคิดสร้างสรรค์ การสื่อสาร และความยืดหยุ่น' },
              water_score: { thai: 'น้ำ', desc: 'ความอ่อนไหว ความเห็นอกเห็นใจ และสัญชาตญาณ' }
            };
            const info = descriptions[element];
            return (
              <div key={element}>
                <div className="flex justify-between text-base mb-1">
                  <div>
                    <span className="text-gray-300">{name}</span>
                    {info && <span className="text-[#B5A593] ml-2">({info.thai})</span>}
                  </div>
                  <span className="text-[#E07A5F]">{formatPercent(value)}%</span>
                </div>
                {info && <div className="text-sm text-gray-500 mb-2 leading-relaxed">{info.desc}</div>}
                <div className="h-2 bg-[#2a2d38] rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-[#B5A593] to-[#E07A5F]"
                    style={{ width: `${formatPercent(value)}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Personality Insights */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-4">
          <div className="text-sm text-gray-400 mb-1">VENUS-MARS HARMONY</div>
          <div className="text-base text-[#B5A593] mb-2">ความกลมกลืนระหว่างดาวศุกร์-ดาวอังคาร</div>
          <div className="text-2xl font-bold text-[#B5A593] mb-2">
            {formatPercent(personalityVector.venus_mars_harmony)}%
          </div>
          <div className="text-sm text-gray-500 leading-relaxed">
            ความสมดุลระหว่างความรักกับความปรารถนา แสดงถึงเคมีทางรักและความเข้ากันได้ทางกาย
          </div>
        </div>
        <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-4">
          <div className="text-sm text-gray-400 mb-1">SUN-MOON BALANCE</div>
          <div className="text-base text-[#E07A5F] mb-2">ความสมดุลระหว่างดวงอาทิตย์-ดวงจันทร์</div>
          <div className="text-2xl font-bold text-[#E07A5F] mb-2">
            {formatPercent(personalityVector.sun_moon_balance)}%
          </div>
          <div className="text-sm text-gray-500 leading-relaxed">
            ความกลมกลืนระหว่างตัวตนภายนอกกับอารมณ์ภายใน สะท้อนความสมบูรณ์ของบุคลิกภาพ
          </div>
        </div>
        <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-4">
          <div className="text-sm text-gray-400 mb-1">EMOTIONAL STABILITY</div>
          <div className="text-base text-[#B5A593] mb-2">ความมั่นคงทางอารมณ์</div>
          <div className="text-2xl font-bold text-[#B5A593] mb-2">
            {formatPercent(personalityVector.moon_stability)}%
          </div>
          <div className="text-sm text-gray-500 leading-relaxed">
            ความสามารถในการจัดการอารมณ์และรักษาสภาวะจิตใจให้สมดุลในความสัมพันธ์
          </div>
        </div>
      </div>

      {/* Diagnostics */}
      {diagnostics.length > 0 && (
        <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6">
          <h3 className="text-lg font-semibold text-[#B5A593] mb-4">DIAGNOSTIC INSIGHTS</h3>
          <div className="space-y-3">
            {diagnostics.map((diag, idx) => (
              <div key={idx} className="bg-[#2a2d38] border border-[#4E5564] rounded-lg p-4">
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
        <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6">
          <h3 className="text-lg font-semibold text-[#B5A593] mb-4">ASPECT ENGINE DATA</h3>
          
          {/* Aspect Summary */}
          {aspectScores && (
            <div className="grid grid-cols-2 xl:grid-cols-5 gap-4 mb-6">
              <div className="bg-[#2a2d38] rounded-lg p-3 text-center">
                <div className="text-xs text-gray-400 mb-1">TOTAL</div>
                <div className="text-xl font-bold text-white">{aspects.length}</div>
              </div>
              <div className="bg-[#2a2d38] rounded-lg p-3 text-center">
                <div className="text-xs text-gray-400 mb-1">HARMONIOUS</div>
                <div className="text-xl font-bold text-[#E07A5F]">{aspectScores.harmonious_count}</div>
              </div>
              <div className="bg-[#2a2d38] rounded-lg p-3 text-center">
                <div className="text-xs text-gray-400 mb-1">CHALLENGING</div>
                <div className="text-xl font-bold text-[#f59e0b]">{aspectScores.challenging_count}</div>
              </div>
              <div className="bg-[#2a2d38] rounded-lg p-3 text-center">
                <div className="text-xs text-gray-400 mb-1">NEUTRAL</div>
                <div className="text-xl font-bold text-[#B5A593]">{aspectScores.neutral_count}</div>
              </div>
              <div className="bg-[#2a2d38] rounded-lg p-3 text-center">
                <div className="text-xs text-gray-400 mb-1">AVG STRENGTH</div>
                <div className="text-xl font-bold text-white">{aspectScores.average_strength.toFixed(2)}</div>
              </div>
            </div>
          )}

          {/* Aspect List */}
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {aspects.map((aspect, idx) => (
              <div key={idx} className="bg-[#2a2d38] border border-[#4E5564] rounded-lg p-3 flex items-center justify-between">
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
                    <span className="text-[#E07A5F] ml-1">{(aspect.strength * 100).toFixed(0)}%</span>
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
