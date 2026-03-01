import { motion } from 'framer-motion';

interface CoordinatePlaneProps {
  size?: number;
}

export const CoordinatePlane = ({ size = 400 }: CoordinatePlaneProps) => {
  const gridLines = 10;
  const step = size / gridLines;

  return (
    <svg width={size} height={size} className="mx-auto">
      {/* Grid lines */}
      <g opacity="0.15">
        {Array.from({ length: gridLines + 1 }).map((_, i) => (
          <g key={i}>
            <line
              x1={i * step}
              y1={0}
              x2={i * step}
              y2={size}
              stroke="#4E5564"
              strokeWidth="1"
            />
            <line
              x1={0}
              y1={i * step}
              x2={size}
              y2={i * step}
              stroke="#4E5564"
              strokeWidth="1"
            />
          </g>
        ))}
      </g>

      {/* Axes */}
      <line
        x1={size / 2}
        y1={0}
        x2={size / 2}
        y2={size}
        stroke="#B5A593"
        strokeWidth="2"
        opacity="0.3"
      />
      <line
        x1={0}
        y1={size / 2}
        x2={size}
        y2={size / 2}
        stroke="#B5A593"
        strokeWidth="2"
        opacity="0.3"
      />

      {/* Origin point with pulse */}
      <motion.circle
        cx={size / 2}
        cy={size / 2}
        r="6"
        fill="#00d9ff"
        animate={{
          scale: [1, 1.3, 1],
          opacity: [0.8, 1, 0.8],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />
      <circle
        cx={size / 2}
        cy={size / 2}
        r="6"
        fill="#00d9ff"
        opacity="0.3"
        filter="url(#glow)"
      />

      {/* Glow filter */}
      <defs>
        <filter id="glow">
          <feGaussianBlur stdDeviation="3" result="coloredBlur" />
          <feMerge>
            <feMergeNode in="coloredBlur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
    </svg>
  );
};
