
const express = require("express");
const {
  getCart,
  addCart,
  updateCart,
  removeCart,
} = require("../controller/CartController");
const { protect } = require("../middleware/authentication");

const cartRouter = express.Router();
cartRouter.post("/add", protect, addCart);
cartRouter.get("/", protect, getCart);
cartRouter.put("/update/:id", protect, updateCart);
cartRouter.delete("/remove/:id", protect, removeCart);

module.exports = {cartRouter};
