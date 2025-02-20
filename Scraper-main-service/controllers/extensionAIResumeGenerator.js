const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();
const {generateATSPrompt} = require('../lib/extension/aiResumeMakerPrompt')

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
const model = genAI.getGenerativeModel({ model: 'gemini-pro' });


exports.aiResumeMaker = async (req, res) => {
    try {
        const { jobDescription, resume } = req.body;

        if (!jobDescription || !resume) {
            return res.status(400).json({
                success: false,
                error: 'Both jobDescription and resume are required'
            });
        }

        const prompt = generateATSPrompt(jobDescription, resume);
        const result = await model.generateContent(prompt);
        const response = await result.response;
        
        try {
            // Extract just the JSON part from the response
            const responseText = response.text();
            const jsonMatch = responseText.match(/\{[\s\S]*\}/);
            if (!jsonMatch) {
                throw new Error('No valid JSON found in response');
            }

            const parsedResponse = JSON.parse(jsonMatch[0]);
            
            // Validate the response structure
            if (!parsedResponse.atsScore || !parsedResponse.resumeData) {
                throw new Error('Invalid response structure');
            }

            return res.json({
                success: true,
                atsScore: parsedResponse.atsScore,
                resumeData: parsedResponse.resumeData
            });

        } catch (parseError) {
            console.error('Error parsing AI response:', parseError);
            return res.status(500).json({
                success: false,
                error: 'Failed to generate valid resume data'
            });
        }

       
    } catch (error) {
        console.error('Error in optimize-resume endpoint:', error);
        return res.status(500).json({
            success: false,
            error: 'An error occurred while optimizing the resume'
        });
    }
}