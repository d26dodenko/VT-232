const ProductModel = require('../models/ProductModel');

const getProducts = async (req, res, next) => {
  try {
    const products = await ProductModel.find();
    res.json(products);
  } catch (error) {
    next(error);
  }
};

const getSingleProducts = async (req, res, next) => {
try {
  const product = await ProductModel.findById(req.params.id);
  if (!product) {
    return res.status(404).json({ message: "Product not found" });
  }
  res.json(product);
} catch (error) {
  res.status(500).json({ message: "Error" });
}
};

module.exports = { getProducts,getSingleProducts  }