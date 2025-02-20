const express = require("express");
const extensionAiResume = express.Router();

const extensionAi = require('../controllers/extensionAIResumeGenerator');

extensionAiResume.post('/optimize-resume', extensionAi.aiResumeMaker);

module.exports = extensionAiResume;