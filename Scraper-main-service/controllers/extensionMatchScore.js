const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();
const {generatePrompt} = require('../lib/extension/prompt')

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
const model = genAI.getGenerativeModel({ model: 'gemini-pro' });

exports.matchScore = async (req, res) => {
    try {
        const { jobDescription, resume } = req.body;

        if (!jobDescription || !resume) {
            return res.status(400).json({
                success: false,
                error: 'Both jobDescription and resume are required'
            });
        };

        const prompt = generatePrompt(jobDescription, resume);
        const result = await model.generateContent(prompt);
        const response = await result.response;
        const rawScore = response.text().trim();

        let score = parseFloat(rawScore);

        if (isNaN(score)) {
            return res.status(500).json({
                success: false,
                error: 'Failed to generate valid match score'
            });
        }

        score = Math.max(0, Math.min(100, score));
        score = Number(score.toFixed(1));

        return res.json({
            success: true,
            matchScore: score
        });
    } catch (error) {
        console.error('Error in match-score endpoint:', error);
        return res.status(500).json({
            success: false,
            error: 'An error occurred while processing your request'
        });
    }
}