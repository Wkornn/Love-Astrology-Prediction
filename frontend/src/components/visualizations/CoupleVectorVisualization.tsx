import { motion } from 'framer-motion';
import { useState, useEffect, useMemo } from 'react';

interface CoupleVectorVisualizationProps {
  vectorSimilarity: number;
  person1Name?: string;
  person2Name?: string;
}

export const CoupleVectorVisualization = ({ 
  vectorSimilarity, 
  person1Name = "Person 1", 
  person2Name = "Person 2" 
}: CoupleVectorVisualizationProps) => {
  const [phase, setPhase] = useState<'init' | 'animating' | 'final'>('init');
  const [currentAngle, setCurrentAngle] = useState(120);
  
  const size = 600;
  const center = size / 2;
  const vectorLength = 200;

  const finalAngle = useMemo(() => {
    const score = vectorSimilarity / 100;
    if (score === undefined || score < -1 || score > 1) return 90;
    return Math.acos(Math.max(-1, Math.min(1, score))) * (180 / Math.PI);
  }, [vectorSimilarity]);

  useEffect(() => {
    setPhase('init');
    setCurrentAngle(120);
    
    const timer1 = setTimeout(() => {
      setPhase('animating');
      const duration = 800;
      const startTime = Date.now();
      const startAngle = 120;
      
      const animate = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const angle = startAngle + (finalAngle - startAngle) * eased;
        setCurrentAngle(angle);
        
        if (progress < 1) {
          requestAnimationFrame(animate);
        } else {
          setPhase('final');
        }
      };
      animate();
    }, 300);
    
    return () => clearTimeout(timer1);
  }, [finalAngle]);

  if (vectorSimilarity === undefined) {
    return (
      <div className="bg-[#1A1D29]/40 backdrop-blur-md border border-[#4E5564] rounded-xl p-6 text-center">
        <p className="text-cyan-400 text-sm">Waiting for compatibility analysis...</p>
      </div>
    );
  }

  const person1VectorX = vectorLength;
  const person1VectorY = 0;
  const person2VectorX = vectorLength * Math.cos(currentAngle * Math.PI / 180);
  const person2VectorY = -vectorLength * Math.sin(currentAngle * Math.PI / 180);

  return (
    <div className="bg-[#1A1D29]/40 backdrop-blur-md border border-[#4E5564] rounded-xl p-6 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-radial from-pink-500/5 to-transparent pointer-events-none" />
      
      <h3 className="text-lg xl:text-xl font-semibold text-[#B5A593] text-center mb-4">
        COUPLE VECTOR ALIGNMENT
      </h3>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 items-center">
        {/* Left: Vector Graph */}
        <div className="flex flex-col items-center">
          <motion.div 
            className="text-center mb-4" 
            initial={{ opacity: 0 }} 
            animate={{ opacity: 1 }} 
            transition={{ duration: 0.5 }}
          >
            <p className="text-base text-pink-400">
              {phase === 'init' && 'Initializing Couple Alignment...'}
              {phase === 'animating' && (
                <span className="font-mono">
                  cos(θ) = {(vectorSimilarity / 100).toFixed(3)}
                </span>
              )}
              {phase === 'final' && `${vectorSimilarity.toFixed(0)}% Vector Match`}
            </p>
          </motion.div>

          <div className="relative" style={{ height: size, width: size }}>
            <svg width={size} height={size}>
              <defs>
                <filter id="glowCouple">
                  <feGaussianBlur stdDeviation="4" result="coloredBlur" />
                  <feMerge>
                    <feMergeNode in="coloredBlur" />
                    <feMergeNode in="SourceGraphic" />
                  </feMerge>
                </filter>
              </defs>

              {/* Grid circles */}
              <g opacity="0.1">
                {[50, 100, 150, 200].map(r => (
                  <circle key={r} cx={center} cy={center} r={r} fill="none" stroke="#4E5564" strokeWidth="1" />
                ))}
              </g>

              {/* Person 1 vector (cyan) */}
              <line
                x1={center}
                y1={center}
                x2={center + person1VectorX}
                y2={center + person1VectorY}
                stroke="#00d9ff"
                strokeWidth="8"
                strokeOpacity="1"
              />

              {/* Origin point */}
              <circle 
                cx={center} 
                cy={center} 
                r="6" 
                fill="#B5A593"
              />

              {/* Angle arc */}
              {phase !== 'init' && (
                <motion.path
                  d={`M ${center + 80} ${center} A 80 80 0 0 0 ${center + 80 * Math.cos(currentAngle * Math.PI / 180)} ${center - 80 * Math.sin(currentAngle * Math.PI / 180)}`}
                  fill="none"
                  stroke="#B5A593"
                  strokeWidth="2"
                  opacity="0.5"
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{ duration: 0.8 }}
                />
              )}

              {/* Person 2 vector (pink) */}
              <motion.line
                x1={center}
                y1={center}
                x2={center}
                y2={center}
                stroke="#ff6b9d"
                strokeWidth="8"
                strokeOpacity="1"
                animate={{ x2: center + person2VectorX, y2: center + person2VectorY }}
                transition={{ duration: 0.8, delay: 0.3 }}
              />
            </svg>
          </div>

          {/* Legend */}
          <div className="flex items-center gap-4 mt-4 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-4 h-1 bg-cyan-400"></div>
              <span className="text-gray-400">{person1Name}</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-1 bg-pink-400"></div>
              <span className="text-gray-400">{person2Name}</span>
            </div>
          </div>
        </div>

        {/* Right: Stats */}
        <div className="flex flex-col justify-center">
          <div className="bg-[#2a2d38] border border-[#4E5564] rounded-lg p-6">
            <h4 className="text-xl font-bold text-[#E07A5F] mb-4 text-center">Vector Compatibility</h4>
            
            {/* Math info */}
            <div className="bg-[#1A1D29]/40 backdrop-blur-md rounded-lg p-4 mb-4 font-mono text-sm">
              <p className="text-gray-400">cos(θ) = <span className="text-[#E07A5F] font-bold">{(vectorSimilarity / 100).toFixed(3)}</span></p>
              <p className="text-gray-400">θ = <span className="text-[#B5A593] font-bold">{finalAngle.toFixed(1)}°</span></p>
            </div>

            {/* Similarity score */}
            <div className="text-center">
              <div className="text-5xl font-bold text-[#B5A593] mb-2">
                {vectorSimilarity.toFixed(0)}%
              </div>
              <p className="text-sm text-gray-400">Vector Similarity</p>
            </div>

            {/* Interpretation */}
            <div className="mt-4 bg-[#1A1D29]/40 backdrop-blur-md rounded-lg p-3 border-l-2 border-[#E07A5F]">
              <p className="text-sm text-gray-300">
                {vectorSimilarity >= 80 ? '🎯 Highly aligned personalities - Strong compatibility' :
                 vectorSimilarity >= 60 ? '✨ Good alignment - Compatible traits' :
                 vectorSimilarity >= 40 ? '🔄 Moderate alignment - Some differences' :
                 '🌀 Divergent personalities - Complementary opposites'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
