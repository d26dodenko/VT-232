import { useState, FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { signup } from "../api/api";

const Signup = () => {
  const [fullName, setFullName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const navigate = useNavigate();

  const handleSignup = async (e: FormEvent) => {
    e.preventDefault();

    try {
      const response = await signup({ fullName, email, password });
      toast.success(response.data.message);
      setTimeout(() => navigate("/login"), 2000);
    } catch (error: any) {
      toast.error(error?.response?.data?.message || "An unexpected error occurred");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-xl shadow-lg w-[400px]">
        <h2 className="text-2xl font-bold text-center text-[#227f7f]">Sign Up</h2>
        <p className="text-gray-500 text-center mb-4">
          Discover the latest trends, express your style, and redefine fashion.
        </p>
        <form onSubmit={handleSignup} className="space-y-4">
          <div>
            <input
              type="text"
              placeholder="Name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
              className="w-full p-3 border border-gray-300 rounded-md outline-none"
            />
          </div>
          <div>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full p-3 border border-gray-300 rounded-md outline-none"
            />
          </div>
          <div className="relative">
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full p-3 border border-gray-300 rounded-md outline-none tracking-wider"
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-3 text-gray-600"
            >
            </button>
          </div>
          <button
            type="submit"
            className="w-full p-3 bg-[#227f7f]  text-white font-medium rounded-md flex items-center justify-center space-x-2"
          >
            
            <span>Sign Up</span>
          </button>
        </form>
        <p className="text-sm text-center mt-4">
          Already have an account?{" "}
          <span
            className="text-[#227f7f] cursor-pointer font-medium"
            onClick={() => navigate("/login")}
          >
            Login
          </span>
        </p>
      </div>
    </div>
  );
};

export default Signup;
