import { motion } from 'framer-motion';
import { useState, useEffect, useMemo } from 'react';

interface LoveVector3DProps {
  emotionalIntensity: number;
  passionIndex: number;
  conflictReactivity: number;
  onComplete?: () => void;
}

export const LoveVector3D = ({ emotionalIntensity, passionIndex, conflictReactivity, onComplete }: LoveVector3DProps) => {
  const [phase, setPhase] = useState<'init' | 'vector' | 'labels' | 'final'>('init');
  const [key, setKey] = useState(0);
  const size = 600;
  const center = size / 2;

  const x = useMemo(() => emotionalIntensity / 100, [emotionalIntensity]);
  const y = useMemo(() => passionIndex / 100, [passionIndex]);
  const z = useMemo(() => conflictReactivity / 100, [conflictReactivity]);

  const scale = 360;
  const vectorScale = scale / 1.5; // Make vector 1.5x shorter
  const vectorX = useMemo(() => (x - z) * vectorScale * 0.866, [x, z]);
  const vectorY = useMemo(() => (x + z) * vectorScale * 0.5 - y * vectorScale, [x, y, z]);
  const magnitude = useMemo(() => Math.sqrt(x ** 2 + y ** 2 + z ** 2), [x, y, z]);

  // Axis projections
  const xAxisLen = useMemo(() => x * vectorScale * 0.866, [x]);
  const xAxisY = useMemo(() => x * vectorScale * 0.5, [x]);
  const zAxisLen = useMemo(() => -z * vectorScale * 0.866, [z]);
  const zAxisY = useMemo(() => z * vectorScale * 0.5, [z]);
  const yAxisLen = useMemo(() => -y * vectorScale, [y]);

  useEffect(() => {
    const timer1 = setTimeout(() => setPhase('vector'), 800);
    const timer2 = setTimeout(() => setPhase('labels'), 2000);
    const timer3 = setTimeout(() => {
      setPhase('final');
      onComplete?.();
    }, 3200);
    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearTimeout(timer3);
    };
  }, [key]);

  const replay = () => {
    setPhase('init');
    setKey(k => k + 1);
  };

  if (emotionalIntensity === undefined || passionIndex === undefined || conflictReactivity === undefined) {
    return (
      <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6 text-center">
        <p className="text-cyan-400 text-sm">Awaiting analysis data...</p>
      </div>
    );
  }

  return (
    <div className="bg-[#1A1D29] border border-[#4E5564] rounded-xl p-6 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-radial from-cyan-500/5 to-transparent pointer-events-none" />
      
      <div className="flex flex-col xl:flex-row items-center justify-between gap-2 mb-4">
        <div className="hidden xl:block xl:flex-1"></div>
        <h3 className="text-lg xl:text-xl font-semibold text-[#B5A593] xl:flex-1 text-center">
          3D ROMANTIC VECTOR ANALYSIS
        </h3>
        <div className="xl:flex-1 flex justify-center xl:justify-end">
          <button onClick={replay} className="text-xs xl:text-sm bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-500/50 rounded px-2 py-1 xl:px-3 xl:py-2 transition-colors text-cyan-400">
            ↻ Replay
          </button>
        </div>
      </div>

      <motion.div className="text-center mb-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }} key={key}>
        <p className="text-base text-cyan-400">
          {phase === 'init' && 'Initializing Romantic Vector...'}
          {phase === 'vector' && 'Projecting 3D Personality Space...'}
          {phase === 'labels' && 'Mapping Feature Dimensions...'}
          {phase === 'final' && 'Vector Profile Complete'}
        </p>
      </motion.div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 items-center justify-items-center">
        <div className="relative" style={{ height: size }}>
          <svg width={size} height={size} className="absolute top-0 left-0 mx-auto" style={{ left: '50%', transform: 'translateX(-50%)' }} key={key}>
          <defs>
            <linearGradient id="vectorGradient3D" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#00d9ff" />
              <stop offset="50%" stopColor="#ff00ff" />
              <stop offset="100%" stopColor="#00ff88" />
            </linearGradient>
            <filter id="vectorGlow">
              <feGaussianBlur stdDeviation="4" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {/* Isometric grid - table-like */}
          <g opacity="0.08">
            {Array.from({ length: 9 }).map((_, i) => {
              const offset = (i - 4) * 40;
              return (
                <g key={i}>
                  {/* X-direction lines */}
                  {Array.from({ length: 9 }).map((_, j) => {
                    const zOffset = (j - 4) * 40;
                    const startX = center + offset * 0.866 - zOffset * 0.866;
                    const startY = center + offset * 0.5 + zOffset * 0.5;
                    const endX = center + offset * 0.866 - (zOffset + 40) * 0.866;
                    const endY = center + offset * 0.5 + (zOffset + 40) * 0.5;
                    return <line key={`x${j}`} x1={startX} y1={startY} x2={endX} y2={endY} stroke="#4E5564" strokeWidth="1" />;
                  })}
                  {/* Z-direction lines */}
                  {Array.from({ length: 9 }).map((_, j) => {
                    const xOffset = (j - 4) * 40;
                    const startX = center + xOffset * 0.866 - offset * 0.866;
                    const startY = center + xOffset * 0.5 + offset * 0.5;
                    const endX = center + (xOffset + 40) * 0.866 - offset * 0.866;
                    const endY = center + (xOffset + 40) * 0.5 + offset * 0.5;
                    return <line key={`z${j}`} x1={startX} y1={startY} x2={endX} y2={endY} stroke="#4E5564" strokeWidth="1" />;
                  })}
                </g>
              );
            })}
          </g>

          {/* Bold axis lines */}
          <line x1={center} y1={center} x2={center + 180 * 0.866} y2={center + 180 * 0.5} stroke="#4E5564" strokeWidth="3" opacity="0.3" />
          <line x1={center} y1={center} x2={center - 180 * 0.866} y2={center + 180 * 0.5} stroke="#4E5564" strokeWidth="3" opacity="0.3" />
          <line x1={center} y1={center} x2={center} y2={center - 180} stroke="#4E5564" strokeWidth="3" opacity="0.3" />

          {/* Colored axis projections */}
          <motion.line x1={center} y1={center} x2={center} y2={center} stroke="#00d9ff" strokeWidth="3" opacity="0.6" initial={{ x2: center, y2: center }} animate={{ x2: center + xAxisLen, y2: center + xAxisY }} transition={{ duration: 0.8, delay: 0.2 }} />
          <motion.line x1={center} y1={center} x2={center} y2={center} stroke="#00ff88" strokeWidth="3" opacity="0.6" initial={{ y2: center }} animate={{ y2: center + yAxisLen }} transition={{ duration: 0.8, delay: 0.4 }} />
          <motion.line x1={center} y1={center} x2={center} y2={center} stroke="#ff00ff" strokeWidth="3" opacity="0.6" initial={{ x2: center, y2: center }} animate={{ x2: center + zAxisLen, y2: center + zAxisY }} transition={{ duration: 0.8, delay: 0.3 }} />

          <motion.circle cx={center} cy={center} r="8" fill="#00d9ff" animate={{ scale: [1, 1.3, 1], opacity: [0.8, 1, 0.8] }} transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }} />

          {phase !== 'init' && (
            <>
              <motion.line x1={center} y1={center} x2={center} y2={center} stroke="url(#vectorGradient3D)" strokeWidth="5" filter="url(#vectorGlow)" animate={{ x2: center + vectorX, y2: center + vectorY }} transition={{ duration: 1.2, ease: "easeOut" }} />
              <motion.polygon
                points="0,-10 -5,5 5,5"
                fill="#00ff88"
                filter="url(#vectorGlow)"
                initial={{ opacity: 0 }}
                animate={{ 
                  opacity: 1
                }}
                transition={{ duration: 1.2, ease: "easeOut" }}
                style={{ 
                  transform: `translate(${center + vectorX}px, ${center + vectorY}px) rotate(${Math.atan2(vectorY, vectorX) * 180 / Math.PI + 90}deg)`,
                  transformOrigin: 'center'
                }}
              />
            </>
          )}
        </svg>
        </div>

        <div className="space-y-6 flex flex-col items-center">
          {/* Vector equation with large brackets */}
          <div className="flex items-center gap-2 font-mono text-lg text-white">
            <span className="text-6xl" style={{ lineHeight: '0.8', fontWeight: 10 }}>[</span>
            <div className="flex flex-col justify-center" style={{ lineHeight: '1.8' }}>
              <span className="text-cyan-400">x</span>
              <span className="text-green-400">y</span>
              <span className="text-purple-400">z</span>
            </div>
            <span className="text-6xl" style={{ lineHeight: '0.8', fontWeight: 10 }}>]</span>
            <span className="mx-2">=</span>
            <span className="text-6xl" style={{ lineHeight: '0.8', fontWeight: 10 }}>[</span>
            <div className="flex flex-col justify-center" style={{ lineHeight: '1.8' }}>
              <span className="text-cyan-400">{x.toFixed(2)}</span>
              <span className="text-green-400">{y.toFixed(2)}</span>
              <span className="text-purple-400">{z.toFixed(2)}</span>
            </div>
            <span className="text-6xl" style={{ lineHeight: '0.8', fontWeight: 10 }}>]</span>
          </div>

          {/* Axis descriptions */}
          <div className="space-y-2 text-sm text-gray-400">
            <p><span className="text-cyan-400">X</span> = Emotional Intensity (ความเข้มข้นทางอารมณ์)</p>
            <p><span className="text-green-400">Y</span> = Passion Index (ระดับความหลงใหล)</p>
            <p><span className="text-purple-400">Z</span> = Conflict Reactivity (การตอบสนองต่อความขัดแย้ง)</p>
          </div>
        </div>
      </div>

      {phase === 'final' && (
        <motion.div className="mt-4 text-center" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
          <p className="text-2xl text-white">Vector Magnitude: {magnitude.toFixed(3)}</p>
          <p>3D Profile: [{x.toFixed(2)}, {y.toFixed(2)}, {z.toFixed(2)}]</p>
        </motion.div>
      )}
    </div>
  );
};
