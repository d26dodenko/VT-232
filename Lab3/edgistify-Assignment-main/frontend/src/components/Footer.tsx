import { FaTwitter, FaInstagram, FaFacebook, FaWhatsapp, FaUser } from "react-icons/fa";
import { MdVerified } from "react-icons/md";

export default function Footer() {
  return (
    <footer className="bg-teal-600 text-white text-center py-6">
      <div className="max-w-4xl mx-auto">
        <h2 className="font-bold text-lg">Clothify <span className="font-normal"> | Fashion Redefined</span></h2>
        
        {/* Social Media Icons */}
        <div className="flex justify-center space-x-4 my-4 text-xl">
          <FaTwitter />
          <FaInstagram />
          <FaFacebook />
          <FaWhatsapp />
        </div>

        {/* Links */}
        <div className="flex justify-center space-x-6 text-sm">
          <a href="/" className="hover:underline">Product</a>
          <a href="/cart" className="hover:underline">Cart</a>
          <a href="/login" className="hover:underline">Login</a>
        </div>

        {/* Divider */}
        <div className="border-t border-white my-4 w-4/5 mx-auto"></div>

        {/* Owner Info */}
        <div className="flex justify-center items-center space-x-4 text-sm">
          <div className="flex items-center space-x-1">
            <FaUser />
            <span>Owned Md Sajid Ansari</span>
          </div>
          <div className="flex items-center space-x-1">
            <MdVerified />
            <span>Secure Online Shopping</span>
          </div>
        </div>

        {/* Copyright */}
        <p className="text-sm mt-2">© 2025 Clothify. All rights reserved.</p>
      </div>
    </footer>
  );
}
