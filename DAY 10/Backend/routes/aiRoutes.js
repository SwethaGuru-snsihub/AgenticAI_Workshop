const express = require('express');
const router = express.Router();
const { generateJourney } = require('../controllers/aiController');

router.post('/generate-journey', generateJourney);

module.exports = router;
