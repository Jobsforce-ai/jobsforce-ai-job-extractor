const express = require("express");
const router = express.Router();
const pythonExtractor = require("../controllers/pythonExtractor");


router.get("/", pythonExtractor.getCachedJobs);


module.exports = router;
