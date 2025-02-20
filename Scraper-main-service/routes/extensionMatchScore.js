const express = require("express");
const extensionMatchScore = express.Router();
const { matchScore } = require("../controllers/extensionMatchScore");

extensionMatchScore.post('/matchScore', matchScore)

module.exports = extensionMatchScore;