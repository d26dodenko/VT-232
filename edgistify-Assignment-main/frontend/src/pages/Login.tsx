import { useState, FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { login } from "../api/api";

const Login = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const navigate = useNavigate();

  const handleLogin = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const response = await login({ email, password });
      const { token, userId, message }: { token: string; userId: string; message: string } = response.data;

      localStorage.setItem("token", token);
      localStorage.setItem("userId", userId);

    //   console.log("Extracted userId:", userId);

      toast.success(message);
      setTimeout(() => navigate("/"), 2000);
    } catch (error: any) {
      toast.error(
        error?.response?.data?.message || "An unexpected error occurred"
      );
    }
  };

  return (
    <div className="flex bg-gray-100 items-center justify-center h-[90vh]">
      <div className="bg-white p-6 rounded-lg shadow-md w-96">
        <h2 className="text-2xl font-bold mb-4 text-center">Login</h2>
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-gray-600 text-sm font-medium">
              Email <span className="text-red-500">*</span>
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full p-2 border rounded-md outline-none"
            />
          </div>
          <div className="relative">
            <label className="block text-gray-600 text-sm font-medium">
              Password <span className="text-red-500">*</span>
            </label>
            <input
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full p-2 border rounded-md outline-none tracking-wider"
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute inset-y-0 right-3 top-5 pr-0 flex items-center text-sm leading-5"
            >
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>
          <button
            type="submit"
            className="w-full p-2 bg-[#227f7f] cursor-pointer text-white font-medium rounded-md"
          >
            Login
          </button>
        </form>
        <p className="text-sm text-center mt-4">
          Don&lsquo;t have an account?{" "}
          <span
            className="text-[#227f7f] cursor-pointer"
            onClick={() => navigate("/signup")}
          >
            Sign Up
          </span>
        </p>
      </div>
    </div>
  );
};

export default Login;
