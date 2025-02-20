const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const pythonExtractor = require("./routes/pythonExtractor");
const extenstionScraper = require("./routes/extensionJobScarper");
const extenstionMatchScore = require("./routes/extensionMatchScore");
const extensionAIResumeGenerator = require("./routes/extensionAIResumeGenerator")

const nodeapp = express();
nodeapp.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  next();
});

nodeapp.use(cors());
nodeapp.use(bodyParser.json());
nodeapp.use("/api/getJobs", pythonExtractor);
nodeapp.use("/api/ext", extenstionScraper);
nodeapp.use("/api/ext", extenstionMatchScore);
nodeapp.use("/api/ext", extensionAIResumeGenerator);
module.exports = nodeapp;
