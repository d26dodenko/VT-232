const mongoose = require("mongoose");
require("dotenv").config();

// Attempt to connect to MongoDB using the provided URL from the environment variables

const connection = mongoose.connect(process.env.MONGO_URI);

const PORT = process.env.PORT;

module.exports = { connection, PORT };