const express = require("express");
const { createOrder, getOrders } = require("../controller/OrderController");
const { protect } = require("../middleware/authentication"); 

const orderRouter = express.Router();

orderRouter.post("/create", protect, createOrder);
orderRouter.get("/get", protect, getOrders)

module.exports = {orderRouter};