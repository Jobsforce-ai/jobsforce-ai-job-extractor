export const generatePrompt = (jobDescription, resume) => {
    return `
    Task: Analyze the job description and resume below to generate a match score between 0.0 and 100.0.
    
    Job Description:
    ${jobDescription}
    
    Resume:
    ${resume}
    
    Instructions:
    1. Carefully compare the skills, experience, and qualifications in both documents
    2. Consider both technical and soft skills matches
    3. Evaluate education requirements and work experience alignment
    4. Account for specific industry knowledge and certifications
    5. Generate a single decimal number between 0.0 and 100.0 representing the match percentage
    
    Response format: Return ONLY the numeric score with exactly one decimal place. 
    Example response: 87.4
    `;
};