import { useEffect, useState, ChangeEvent, FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { createOrder, getCartItems } from "../api/api";
import { toast } from "react-toastify";

interface CartItem {
  _id: string;
  title: string;
  price: number;
  quantity: number;
  img1: string;
}

interface FormData {
  firstName: string;
  lastName: string;
  email: string;
  address: string;
  city: string;
  pinCode: string;
}

function Checkout() {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    firstName: "",
    lastName: "",
    email: "",
    address: "",
    city: "",
    pinCode: "",
  });

  const navigate = useNavigate();

  useEffect(() => {
    const fetchCartItems = async () => {
      try {
        const response = await getCartItems();
        setCartItems(response.data);
      } catch {
        toast.error("Failed to load cart items");
      }
    };

    fetchCartItems();
  }, []);

  const calculateTotal = (): number =>
    cartItems.reduce((total, item) => total + item.price * item.quantity, 0);

  const handleChange = (e: ChangeEvent<HTMLInputElement>): void => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    if (cartItems.length === 0) {
      toast.error("Your cart is empty!");
      return;
    }

    setLoading(true);
    const orderData = {
      userId: localStorage.getItem("userId"),
      products: cartItems.map((item) => ({
        img1: item.img1,
        title: item.title,
        productId: item._id,
        quantity: item.quantity,
        price: item.price,
      })),
      totalPrice: Math.round(calculateTotal()),
      shippingAddress: `${formData.address}, ${formData.city}, ${formData.pinCode}`,
      paymentStatus: "Pending",
      orderStatus: "Pending",
    };

    try {
      await createOrder(orderData);
      toast.success("Order placed successfully!");
      navigate("/placed");
    } catch {
      toast.error("Failed to place order");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-6 py-10 bg-gray-50 shadow-md rounded-lg">
      <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">Checkout</h1>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <h2 className="text-xl font-semibold mb-3 text-gray-700">Shipping Address</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {["firstName", "lastName", "email", "address", "city", "pinCode"].map(
              (field, index) => (
                <div key={index} className={field === "email" || field === "address" ? "md:col-span-2" : ""}>
                  <label className="block text-sm font-medium text-gray-600 capitalize">
                    {field.replace(/([A-Z])/g, " $1")} <span className="text-red-500">*</span>
                  </label>
                  <input
                    type={field === "email" ? "email" : field === "pinCode" ? "number" : "text"}
                    name={field}
                    required
                    className="block w-full rounded-md px-4 py-3 border border-gray-300 outline-none mt-1 focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400"
                    value={formData[field as keyof FormData]}
                    onChange={handleChange}
                  />
                </div>
              )
            )}
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-2 text-gray-700">Payment Method</h2>
          <p className="text-gray-600">Cash On Delivery</p>
        </div>

        <div className="flex justify-between items-center mt-6 bg-white p-4 rounded-lg shadow-md">
          <p className="text-lg font-semibold text-gray-700">
            Total: <span className="text-teal-600 font-bold"> ${Math.round(calculateTotal())}</span>
          </p>
          <button
            type="submit"
            disabled={loading}
            className={`py-2 px-6 rounded-lg text-white transition-all cursor-pointer ${
              loading ? "bg-gray-400 cursor-not-allowed" : "bg-[#319795]"
            }`}
          >
            {loading ? "Processing..." : "Place Order"}
          </button>
        </div>
      </form>
    </div>
  );
}

export default Checkout;
