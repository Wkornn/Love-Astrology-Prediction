import { Link } from 'react-router-dom';

const Header = () => {
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
        </div>
      </div>
    </header>
  );
};

export default Header;
