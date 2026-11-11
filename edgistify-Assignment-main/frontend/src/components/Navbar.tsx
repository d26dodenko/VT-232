import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
// import logo from "../assets/shoes.png";

const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const token: string | null = localStorage.getItem("token");
  const navigate = useNavigate();

  const logout = (): void => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav className="bg-white shadow-md sticky top-0 z-10">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex justify-between">
          <div className="flex items-center">
            <Link to="/">
              <img className="w-28 h-12" src="https://clothisa.netlify.app/images/logo.png" alt="logo" />
            </Link>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-4">
            <Link to="/" className="text-teal-700 font-bold cursor-pointer">Home</Link>
            <Link to="/products" className="text-teal-700 font-bold cursor-pointer">Products</Link>
            <Link to="/cart" className="text-teal-700 font-bold cursor-pointer">Cart</Link>
            {token ? (
              <button
                onClick={logout}
                className="text-red-600 cursor-pointer bg-white rounded font-bold"
              >
                Logout
              </button>
            ) : (
              <Link to="/login">Login</Link>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="focus:outline-none"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                {isOpen ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <div className="md:hidden">
            <div className="pt-5 pb-3 space-y-1">
              <Link to="/" className="block px-3 py-2">
                Home
              </Link>
              <Link to="/products" className="block px-3 py-2">
                Products
              </Link>
              <Link to="/cart" className="block px-3 py-2">
                Cart
              </Link>
              {!token && (
                <Link to="/login" className="block px-3 py-2">
                  Login
                </Link>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
