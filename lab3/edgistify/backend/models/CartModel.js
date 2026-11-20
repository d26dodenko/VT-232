const mongoose = require("mongoose");

const cartSchema = new mongoose.Schema(
  {
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
    productId: { type: mongoose.Schema.Types.ObjectId, ref: "Product", required: true },
    images: { type: [String], required: true },
    title: { type: String, required: true },
    price: { type: Number, required: true },
    quantity: { type: Number, required: true, default: 1 },
    size: { type: String, required: true }
  },
  {
    timestamps: true,
  }
);

const CartModel = mongoose.model("Cart", cartSchema);

// Export the model directly
module.exports = CartModel;