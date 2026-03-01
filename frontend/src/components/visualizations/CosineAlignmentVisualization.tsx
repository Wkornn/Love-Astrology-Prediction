import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect, useMemo } from 'react';

interface CelebrityMatch {
  name: string;
  occupation?: string;
  similarityScore: number;
  matchReason: string;
  funnyJoke?: string;
}

interface CosineAlignmentVisualizationProps {
  matches: CelebrityMatch[];
}

const COLORS = [
  { gradient: 'celebGradient1', start: '#ff00ff', end: '#ff6b9d', arrow: '#ff6b9d' },
  { gradient: 'celebGradient2', start: '#00d9ff', end: '#00ffaa', arrow: '#00ffaa' },
  { gradient: 'celebGradient3', start: '#fbbf24', end: '#f59e0b', arrow: '#f59e0b' },
  { gradient: 'celebGradient4', start: '#a78bfa', end: '#8b5cf6', arrow: '#8b5cf6' },
  { gradient: 'celebGradient5', start: '#34d399', end: '#10b981', arrow: '#10b981' },
];

export const CosineAlignmentVisualization = ({ matches }: CosineAlignmentVisualizationProps) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [phase, setPhase] = useState<'init' | 'animating' | 'final'>('init');
  const [currentAngle, setCurrentAngle] = useState(120);
  
  const size = 600;
  const center = size / 2;
  const vectorLength = 200;

  const currentMatch = matches[currentIndex];
  const color = COLORS[currentIndex];

  const finalAngle = useMemo(() => {
    if (!currentMatch) return 90;
    const score = currentMatch.similarityScore;
    if (score === undefined || score < -1 || score > 1) return 90;
    return Math.acos(Math.max(-1, Math.min(1, score))) * (180 / Math.PI);
  }, [currentMatch]);

  useEffect(() => {
    setPhase('init');
    setCurrentAngle(120);
    
    const timer1 = setTimeout(() => {
      setPhase('animating');
      const duration = 400;
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
  }, [finalAngle, currentIndex]);

  const nextMatch = () => {
    if (currentIndex < matches.length - 1) {
      setCurrentIndex(i => i + 1);
    }
  };

  const prevMatch = () => {
    if (currentIndex > 0) {
      setCurrentIndex(i => i - 1);
    }
  };

  if (!matches || matches.length === 0) {
    return (
      <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6 text-center">
        <p className="text-cyan-400 text-sm">Waiting for top match compatibility result...</p>
      </div>
    );
  }

  const userVectorX = vectorLength;
  const userVectorY = 0;
  const celebVectorX = vectorLength * Math.cos(currentAngle * Math.PI / 180);
  const celebVectorY = -vectorLength * Math.sin(currentAngle * Math.PI / 180);

  return (
    <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-radial from-purple-500/5 to-transparent pointer-events-none" />
      
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg xl:text-xl font-semibold text-[#B5A593]">
          COSINE SIMILARITY ALIGNMENT
        </h3>
        <div className="flex items-center gap-2">
          <button 
            onClick={prevMatch} 
            disabled={currentIndex === 0}
            className="text-sm bg-purple-500/20 hover:bg-purple-500/30 disabled:opacity-30 disabled:cursor-not-allowed border border-purple-500/50 rounded px-3 py-1 transition-colors text-purple-400"
          >
            ←
          </button>
          <span className="text-sm text-gray-400">#{currentIndex + 1} / {matches.length}</span>
          <button 
            onClick={nextMatch}
            disabled={currentIndex === matches.length - 1}
            className="text-sm bg-purple-500/20 hover:bg-purple-500/30 disabled:opacity-30 disabled:cursor-not-allowed border border-purple-500/50 rounded px-3 py-1 transition-colors text-purple-400"
          >
            →
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 items-start">
        {/* Left: Vector Graph */}
        <div className="flex flex-col items-center">
          <motion.div className="text-center mb-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }} key={currentIndex}>
            <p className="text-base text-purple-400">
              {phase === 'init' && 'Initializing Vector Alignment...'}
              {phase === 'animating' && (
                <span className="font-mono">
                  cos(θ) = A·B / (|A| × |B|) = {currentMatch.similarityScore.toFixed(3)}
                </span>
              )}
              {phase === 'final' && `${(currentMatch.similarityScore * 100).toFixed(0)}% Match`}
            </p>
          </motion.div>

          <div className="relative" style={{ height: size, width: size }}>
            <svg width={size} height={size}>
              <defs>
                <linearGradient id="userGradient" x1="0%" y1="0%" x2="100%">
                  <stop offset="0%" stopColor="#10b981" />
                  <stop offset="100%" stopColor="#34d399" />
                </linearGradient>
                <linearGradient id={color.gradient} x1="0%" y1="0%" x2="100%">
                  <stop offset="0%" stopColor={color.start} />
                  <stop offset="100%" stopColor={color.end} />
                </linearGradient>
                <filter id="glow">
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

              {/* User vector (green) - static - FIRST */}
              <line
                x1={center}
                y1={center}
                x2={center + userVectorX}
                y2={center + userVectorY}
                stroke="#34d399"
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
                  key={`arc-${currentIndex}`}
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

              {/* Celebrity vector */}
              <motion.line
                key={`celeb-line-${currentIndex}`}
                x1={center}
                y1={center}
                x2={center}
                y2={center}
                stroke={color.arrow}
                strokeWidth="8"
                strokeOpacity="1"
                animate={{ x2: center + celebVectorX, y2: center + celebVectorY }}
                transition={{ duration: 0.8, delay: 0.3 }}
              />
            </svg>
          </div>

          {/* Legend */}
          <div className="flex items-center gap-4 mt-4 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-4 h-1 bg-gradient-to-r from-green-400 to-emerald-400"></div>
              <span className="text-gray-400">You</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-1" style={{ background: `linear-gradient(to right, ${color.start}, ${color.end})` }}></div>
              <span className="text-gray-400">{currentMatch.name}</span>
            </div>
          </div>
        </div>

        {/* Right: Match Card */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentIndex}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.3 }}
            className="flex flex-col justify-center h-full"
          >
            <div className="bg-[#2a2d38] border border-[#4E5564] rounded-lg p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-3xl font-bold text-[#E07A5F]">#{currentIndex + 1}</span>
                    <div>
                      <h4 className="text-2xl font-bold text-white">{currentMatch.name}</h4>
                      {currentMatch.occupation && (
                        <p className="text-sm text-gray-400">{currentMatch.occupation}</p>
                      )}
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-4xl font-bold text-[#B5A593]">
                    {(currentMatch.similarityScore * 100).toFixed(0)}%
                  </div>
                  <div className="text-xs text-gray-400">MATCH</div>
                </div>
              </div>

              {/* Math info */}
              <div className="bg-[#1A1D29] rounded-lg p-3 mb-4 font-mono text-sm">
                <p className="text-gray-400">cos(θ) = <span className="text-[#E07A5F] font-bold">{currentMatch.similarityScore.toFixed(3)}</span></p>
                <p className="text-gray-400">θ = <span className="text-[#B5A593] font-bold">{finalAngle.toFixed(1)}°</span></p>
              </div>

              {/* Match reason */}
              <div className="bg-[#1A1D29] rounded px-3 py-2 border-l-2 border-[#E07A5F] mb-3">
                <p className="text-base text-gray-300 leading-relaxed">{currentMatch.matchReason}</p>
              </div>
              
              {/* Funny Joke */}
              {currentMatch.funnyJoke && (
                <div className="bg-[#1A1D29] rounded-lg p-3 border-l-2 border-[#f59e0b]">
                  <p className="text-base text-gray-300 italic leading-relaxed">😄 {currentMatch.funnyJoke}</p>
                </div>
              )}
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
};
