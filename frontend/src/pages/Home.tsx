import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="max-w-6xl mx-auto">
      {/* Header Section */}
      <div className="text-center mb-16">
        <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-[#8b5cf6] to-[#00d9ff] bg-clip-text text-transparent">
          Love Debugging Lab
        </h1>
        <p className="text-[#a0a6b0] text-xl mb-2">
          Professional Astrological Compatibility System
        </p>
        <p className="text-[#6a7080] text-sm">
          Select operational mode to begin analysis
        </p>
      </div>

      {/* Mode Selection Cards */}
      <div className="grid md:grid-cols-3 gap-8 mb-16">
        {/* Mode 1: Love Reading */}
        <Link 
          to="/mode1" 
          className="group block transform transition-all duration-300 hover:scale-105"
        >
          <div className="bg-[#1a1a24] border-2 border-[#2a2a3a] rounded-xl p-8 h-full hover:border-[#8b5cf6] hover:shadow-[0_0_30px_rgba(139,92,246,0.3)] transition-all duration-300">
            <div className="flex items-center justify-between mb-6">
              <div className="text-5xl">💜</div>
              <span className="text-xs font-mono text-[#6a7080] bg-[#0f0f14] px-3 py-1 rounded">
                MODE_01
              </span>
            </div>
            
            <h3 className="text-2xl font-bold mb-3 text-[#e0e6ed] group-hover:text-[#8b5cf6] transition-colors">
              Love Reading
            </h3>
            
            <p className="text-[#a0a6b0] text-sm leading-relaxed mb-6">
              Single-person natal chart analysis. Generate comprehensive love personality profile and relationship readiness assessment.
            </p>
            
            <div className="flex items-center text-[#8b5cf6] text-sm font-mono">
              <span>Initialize Analysis</span>
              <span className="ml-2 group-hover:translate-x-1 transition-transform">→</span>
            </div>
          </div>
        </Link>

        {/* Mode 2: Celebrity Match */}
        <Link 
          to="/mode2" 
          className="group block transform transition-all duration-300 hover:scale-105"
        >
          <div className="bg-[#1a1a24] border-2 border-[#2a2a3a] rounded-xl p-8 h-full hover:border-[#00d9ff] hover:shadow-[0_0_30px_rgba(0,217,255,0.3)] transition-all duration-300">
            <div className="flex items-center justify-between mb-6">
              <div className="text-5xl">⭐</div>
              <span className="text-xs font-mono text-[#6a7080] bg-[#0f0f14] px-3 py-1 rounded">
                MODE_02
              </span>
            </div>
            
            <h3 className="text-2xl font-bold mb-3 text-[#e0e6ed] group-hover:text-[#00d9ff] transition-colors">
              Celebrity Match
            </h3>
            
            <p className="text-[#a0a6b0] text-sm leading-relaxed mb-6">
              Compare your chart against public figure database. Discover top compatibility matches with celebrities and influencers.
            </p>
            
            <div className="flex items-center text-[#00d9ff] text-sm font-mono">
              <span>Initialize Analysis</span>
              <span className="ml-2 group-hover:translate-x-1 transition-transform">→</span>
            </div>
          </div>
        </Link>

        {/* Mode 3: Couple Compatibility */}
        <Link 
          to="/mode3" 
          className="group block transform transition-all duration-300 hover:scale-105"
        >
          <div className="bg-[#1a1a24] border-2 border-[#2a2a3a] rounded-xl p-8 h-full hover:border-[#8b5cf6] hover:shadow-[0_0_30px_rgba(139,92,246,0.3)] transition-all duration-300">
            <div className="flex items-center justify-between mb-6">
              <div className="text-5xl">💕</div>
              <span className="text-xs font-mono text-[#6a7080] bg-[#0f0f14] px-3 py-1 rounded">
                MODE_03
              </span>
            </div>
            
            <h3 className="text-2xl font-bold mb-3 text-[#e0e6ed] group-hover:text-[#8b5cf6] transition-colors">
              Couple Compatibility
            </h3>
            
            <p className="text-[#a0a6b0] text-sm leading-relaxed mb-6">
              Two-person compatibility analysis. Calculate relationship scores, identify strengths, and assess potential challenges.
            </p>
            
            <div className="flex items-center text-[#8b5cf6] text-sm font-mono">
              <span>Initialize Analysis</span>
              <span className="ml-2 group-hover:translate-x-1 transition-transform">→</span>
            </div>
          </div>
        </Link>
      </div>

      {/* Info Section */}
      <div className="bg-[#1a1a24] border border-[#2a2a3a] rounded-xl p-6">
        <div className="flex items-start space-x-4">
          <div className="text-3xl flex-shrink-0">ℹ️</div>
          <div>
            <h4 className="text-lg font-bold mb-2 text-[#e0e6ed]">System Information</h4>
            <p className="text-[#a0a6b0] text-sm leading-relaxed">
              This system uses Swiss Ephemeris for planetary calculations and cosine similarity 
              for compatibility matching. All analyses are based on natal chart feature vectors 
              and rule-based astrological principles.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
