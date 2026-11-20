const OrderModel = require("../models/OrderModel");

const createOrder = async (req, res) => {
  try {
    const { products, totalPrice, shippingAddress } = req.body;
    const userId = req.userId;

    if (!products || products.length === 0) {
      return res.status(400).json({ message: "must contain products" });
    }

    const order = new OrderModel({
      userId,
      products,
      totalPrice,
      shippingAddress,
      paymentStatus: "Pending",
      orderStatus: "Pending",
    });

    await order.save();
    res.status(201).json({ message: "Order added successfully", order });
  } catch (error) {
    res.status(500).json({ message: "Error", error });
  }
};

 // Fetch all orders 
const getOrders = async (req, res) => {
  try {
    const orders = await OrderModel.find({ userId: req.userId });
    res.json(orders);
  } catch (error) {
    res.status(500).json({ message: "Error", error });
  }
};

module.exports = {createOrder, getOrders}