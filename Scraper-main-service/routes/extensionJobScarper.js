const express = require("express");
const extensionRouter = express.Router();
const extensionScraper = require('../controllers/extensionJobScraper');

extensionRouter.get('/scrape', extensionScraper.scrapeJobDescription);

module.exports = extensionRouter;