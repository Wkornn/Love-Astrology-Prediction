import { Link } from 'react-router-dom';
import { useState } from 'react';

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="border-b border-[#4E5564]/30 bg-[#2a2d38]/20 backdrop-blur-md sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-[#B5A593]/80 backdrop-blur-sm rounded-lg flex items-center justify-center">
              <span className="text-2xl">♥️</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-[#e0e6ed] drop-shadow-md">
                Love Debugging Lab
              </h1>
              <p className="text-xs text-[#a0a6b0] drop-shadow-sm">v2.0.0</p>
            </div>
          </Link>
          
          {/* Desktop Nav */}
          <nav className="hidden xl:flex space-x-6">
            <Link to="/mode1" className="text-[#e0e6ed] hover:text-[#E07A5F] transition-colors drop-shadow-md">
              Mode 1
            </Link>
            <Link to="/mode2" className="text-[#e0e6ed] hover:text-[#E07A5F] transition-colors drop-shadow-md">
              Mode 2
            </Link>
            <Link to="/mode3" className="text-[#e0e6ed] hover:text-[#E07A5F] transition-colors drop-shadow-md">
              Mode 3
            </Link>
          </nav>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="xl:hidden text-[#e0e6ed] p-2"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {mobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Nav */}
        {mobileMenuOpen && (
          <nav className="xl:hidden mt-4 pb-4 space-y-2">
            <Link
              to="/mode1"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-[#e0e6ed] hover:text-[#E07A5F] transition-colors py-2 px-4 rounded bg-[#2a2d38]/40"
            >
              Mode 1: Love Reading
            </Link>
            <Link
              to="/mode2"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-[#e0e6ed] hover:text-[#E07A5F] transition-colors py-2 px-4 rounded bg-[#2a2d38]/40"
            >
              Mode 2: Celebrity Match
            </Link>
            <Link
              to="/mode3"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-[#e0e6ed] hover:text-[#E07A5F] transition-colors py-2 px-4 rounded bg-[#2a2d38]/40"
            >
              Mode 3: Couple Compatibility
            </Link>
          </nav>
        )}
      </div>
    </header>
  );
};

export default Header;
