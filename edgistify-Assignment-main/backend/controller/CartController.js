const CartModel = require("../models/CartModel");
const ProductModel = require("../models/ProductModel");

// get a cart
const getCart = async (req, res, next) => {
  try {
    const cartItems = await CartModel.find({ userId: req.userId });
    res.json(cartItems);
  } catch (error) {
    res.status(500).json({ message: "Error", error });
  }
};

// add a cart
const addCart = async (req, res, next) => {
  try {
    const { userId, images, title, price, quantity, size, productId } = req.body;
    const cartItem = new CartModel({
      userId,
      images,
      title,
      price,
      quantity,
      size,
      productId,
    });
    await cartItem.save();
    res.status(201).json({ message: "Added to cart Sucsessfully", cartItem });
  } catch (error) {
    res.status(500).json({ message: "Error", error });
  }
};

// uodate a cart
const updateCart = async (req, res, next) => {
  try {
    const { quantity } = req.body;
    const cartItem = await CartModel.findByIdAndUpdate(
      req.params.id,
      { quantity },
      { new: true }
    );

    if (!cartItem) {
      return res.status(404).json({ message: "Cart is not found" });
    }

    res.json({ message: "Cart updated sucessfully", cartItem });
  } catch (error) {
    res.status(500).json({ message: "Error ", error });
  }
};


// delete a cart
const removeCart = async (req, res) => {
  try {
    const cartItem = await CartModel.findByIdAndDelete(req.params.id);

    if (!cartItem) {
      return res.status(404).json({ message: "Cart is not found" });
    }

    res.json({ message: "Product removed from cart" });
  } catch (error) {
    res.status(500).json({ message: "Error ", error });
  }
};

module.exports = { getCart, addCart, updateCart, removeCart };
