import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { addToCart, getProductById } from "../api/api";
import { toast } from "react-toastify";

interface Product {
  _id: string;
  images:string
  title: string;
  img1:string;
  title2: string;
  price: number;
  description: string;
  reviews: string;
  brand: string;
  originalPrice: number;
  discount: number;
}

const ProductDetails: React.FC = () => {
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [quantity, setQuantity] = useState<number>(1);
  const [selectedSize, setSelectedSize] = useState<string>("S");

  const { id } = useParams<{ id: string }>();
  const userId = localStorage.getItem("userId");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await getProductById(id as string);
        setProduct(response.data);
      } catch {
        toast.error("Failed to fetch product details");
        navigate("/products");
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id, navigate]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-600"></div>
      </div>
    );
  }

  if (!product) {
    return <p className="text-center text-gray-500">Product not found</p>;
  }

  const handleAddToCart = async () => {
    if (!selectedSize) {
      toast.error("Please select a size before adding to cart.");
      return;
    }

    const payload = {
      userId,
      productId: product._id,
      img1: product.img1,
      title: product.title,
      price: product.price,
      quantity,
      size: selectedSize,
    };

    try {
      const res = await addToCart(payload);
      toast.success(res.data.message);
    } catch {
      toast.error("Error adding to cart");
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col lg:flex-row gap-8">
        {/* Left Side - Product Image */}
        <div className="w-full lg:w-6/12">
          <img
           src={product.images[0]}
            alt={product.title}
            className="w-80 rounded-lg shadow-md"
          />
        </div>

        {/* Right Side - Product Details */}
        <div className="w-full lg:w-6/12">
          <h1 className="text-3xl font-semibold text-teal-700 mb-3 italic">
            {product.title}
          </h1>
          <p className="text-gray-600 mb-4">{product.description}</p>

          <p className="font-medium text-teal-600">Brand: {product.brand}</p>

          {/* Price Section */}
          <div className="flex items-center gap-2 mt-2 mb-4">
            <p className="text-3xl font-bold text-teal-700">${product.price}</p>
            <p className="text-gray-400 line-through">${product.originalPrice}</p>
            <p className="text-green-600 font-medium">Save ${product.discount}</p>
          </div>

          {/* Size Selection */}
          <p className="font-medium mb-1">Sizes:</p>
          <div className="flex items-center gap-2 mb-6">
            {["S", "M", "L", "XL"].map((size) => (
              <button
                key={size}
                onClick={() => setSelectedSize(size)}
                className={`px-4 py-1 border rounded-full cursor-pointer ${
                  selectedSize === size
                    ? "bg-teal-600 text-white border-teal-600 cursor-pointer"
                    : "border-gray-500"
                }`}
              >
                {size}
              </button>
            ))}
          </div>

          {/* Quantity Selection */}
          <div className="flex items-center gap-4 mb-6">
            <p className="font-medium">Quantity:</p>
            <button
              onClick={() => setQuantity((prev) => Math.max(1, prev - 1))}
              className="px-4 py-2 hover:text-white font-bold border rounded-md border-neutral-300 hover:bg-teal-600 cursor-pointer"
            >
              -
            </button>
            <span className="px-4 text-teal-600 font-bold">{quantity}</span>
            <button
              onClick={() => setQuantity((prev) => prev + 1)}
              className="px-4 py-2 border hover:text-white font-bold border-neutral-300 rounded-md hover:bg-teal-600 cursor-pointer"
            >
              +
            </button>
          </div>

          {/* Add to Cart Button */}
          <button
            onClick={handleAddToCart}
            className="w-full bg-teal-600 cursor-pointer text-white py-3 px-6 rounded-md hover:bg-teal-700 transition duration-200"
          >
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductDetails;
