const mongoose = require("mongoose");

const productSchema = new mongoose.Schema(
  {
    title: { type: String, required: true },
    category: { type: String, required: true },
    description: {type: String,required: true},
    brand: { type: String, required: true },
    price: { type: Number, required: true },
    rating: { type: Number, default: 0 },
    images: { type: [String], required: true },
    quantity: { type: Number, required: true },
    size: { type: String, required: true },
  },
  {
    timestamps: true,
  }
);

const ProductModel = mongoose.model("Product", productSchema);

// Export the model directly
module.exports = ProductModel;
