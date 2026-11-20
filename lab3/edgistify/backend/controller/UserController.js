const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");
const UserModel = require("../models/UserModel");

//create a account
const register = async (req, res) => {
  const { fullName, email, password } = req.body;
  const result = await UserModel.findOne({ email });
  if (result) {
    res.status(400).send({ message: "Email already exists" });
  } else {
    bcrypt.hash(password, 5, async function (err, hash) {
      if (err) {
        res
          .status(500)
          .send({ message: "Something went wrong, please try again" });
      }
      const new_user = new UserModel({
        fullName: fullName,
        email: email,
        password: hash,
      });
      await new_user.save();
      res.status(200).send({ message: "Signup successful" });
    });
  }
};

//Login here
const login = async (req, res, next) => {
  const { email, password } = req.body;

  const user = await UserModel.findOne({ email });
  if (!user) {
    return res.status(404).send({ message: "User not found" });
  }

  const userId = user._id;
  const userName = user.name;
  const hash = user.password;

  bcrypt.compare(password, hash, async function (err, result) {
    if (err) {
      return res
        .status(500)
        .send({ message: "Something went wrong, please try again" });
    }
    if (result) {
      const token = jwt.sign({ userId, userName }, process.env.JWT_SECRET);
      res
        .status(200)
        .send({ message: "Login successful", token, userName, userId });
    } else {
      res.status(401).send({ message: "Login failed" });
    }
  });
};

module.exports = { register, login };
