const express = require("express");

const productRouter  = express.Router();
const { getProducts,getSingleProducts} = require('../controller/ProductController');

productRouter.get('/', getProducts);
productRouter.get('/:id', getSingleProducts);



module.exports = { productRouter };