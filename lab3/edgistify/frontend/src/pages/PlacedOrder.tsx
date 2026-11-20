import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getOrder } from "../api/api";
import { toast } from "react-toastify";

interface Product {
  _id: string;
  productId: string;
  title: string;
  img1: string;
  quantity: number;
  price: number;
}

interface Order {
  _id: string;
  totalPrice: number;
  shippingAddress: string;
  paymentStatus: "Pending" | "Paid" | "Failed";
  orderStatus: "Pending" | "Processing" | "Shipped" | "Delivered";
  products: Product[];
}

const Placed: React.FC = () => {
  const [order, setOrder] = useState<Order | null>(null);

  useEffect(() => {
    const fetchOrder = async () => {
      try {
        const response = await getOrder();

        if (response.data.length > 0) {
          const latestOrder: Order = response.data[response.data.length - 1];
          setOrder(latestOrder);
        } else {
          toast.error("No orders found.");
        }
      } catch {
        toast.error("Failed to load Order");
      }
    };

    fetchOrder();
  }, []);

  return (
    <div className="bg-gray-100 flex flex-col items-center justify-center min-h-screen p-6">
      <div className="max-w-xl w-full bg-white p-8 rounded-lg shadow-lg text-center">
        {/* Success Icon */}
        <div className="flex flex-col items-center">
          <div className="rounded-full bg-green-200 p-4">
            <svg
              className="h-16 w-16 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
          <h2 className="mt-6 text-2xl font-bold text-gray-900">Order Placed Successfully!</h2>
          <p className="mt-2 text-gray-600">Thank you for your purchase. Your order has been confirmed.</p>
        </div>

        {order && (
          <div className="mt-6 text-left">
            <h3 className="text-lg font-semibold text-gray-800 border-b pb-2">Order Summary</h3>
            <div className="mt-3 text-gray-700 space-y-2 text-sm">
              <p><span className="font-medium">Order ID:</span> {order._id}</p>
              <p><span className="font-medium">Total Price:</span> <span className="text-green-600 font-bold">₹{order.totalPrice}</span></p>
              <p><span className="font-medium">Shipping Address:</span> {order.shippingAddress}</p>
              <p><span className="font-medium">Payment Status:</span> <span className={`font-semibold ${order.paymentStatus === "Paid" ? "text-blue-500" : order.paymentStatus === "Failed" ? "text-red-500" : "text-yellow-500"}`}>{order.paymentStatus}</span></p>
              <p><span className="font-medium">Order Status:</span> <span className={`font-semibold ${order.orderStatus === "Delivered" ? "text-blue-500" : order.orderStatus === "Shipped" ? "text-purple-500" : "text-yellow-500"}`}>{order.orderStatus}</span></p>
            </div>

            {/* Ordered Products */}
            <h3 className="mt-5 text-lg font-semibold text-gray-800 border-b pb-2">Products Ordered</h3>
            <div className="mt-3 space-y-4">
              {order.products.map((product) => (
                <div key={product._id} className="flex items-center bg-gray-50 p-3 rounded-lg shadow-sm">
                  <img
                    src="https://www.sendx.io/hubfs/Email-Messages-for-Order-Confirmation-Page-v3.png"
                    alt={product.title}
                    className="w-20 h-20 object-cover rounded-sm border"
                  />
                  <div className="ml-4 text-sm">
                    <p className="font-medium text-base">{product.title}</p>
                    <p className="text-gray-600">Quantity: {product.quantity}</p>
                    <p className="text-green-600 font-semibold">₹{product.price}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="mt-8">
          <Link
            to="/products"
            className="inline-block bg-teal-600 text-white font-medium py-2 px-6 rounded-lg shadow-md transition"
          >
            Continue Shopping
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Placed;
