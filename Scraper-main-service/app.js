const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const pythonExtractor = require("./routes/pythonExtractor");
const nodeapp = express();
nodeapp.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  next();
});

nodeapp.use(cors());
nodeapp.use(bodyParser.json());
nodeapp.use("/api/getJobs", pythonExtractor);
module.exports = nodeapp;
