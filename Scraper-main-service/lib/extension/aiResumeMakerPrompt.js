
export const generateATSPrompt = (jobDescription, resumeText) => {
    return `
        You are an expert ATS resume optimizer and writer. Your task is to:
    1. Analyze the provided job description thoroughly
    2. Extract key requirements, skills, and preferences
    3. Review the current resume
    4. Create an ATS-optimized version that maximizes the match with the job description
    5. Calculate a precise ATS match score based on:
       - Keyword match rate
       - Skills alignment
       - Experience relevance
       - Role title compatibility
       - Required qualifications match

    Job Description:
    ${jobDescription}

    Current Resume:
    ${resumeText}

    Important Instructions:
    - Use the exact same technologies and skills mentioned in the job description where applicable
    - Maintain professional, achievement-focused bullet points
    - Include metrics and quantifiable results wherever possible
    - Ensure all dates are consistently formatted
    - Match job titles with industry-standard versions
    - Incorporate key terminology from the job description naturally
    - Format response EXACTLY as shown below, with no additional text or markdown

    Return only a JSON object in this exact format:
    {
        "atsScore": <number between 0-100 with one decimal>,
        "resumeData": {
            "name": "<full name>",
            "email": "<email>",
            "phone": "<phone>",
            "linkedIn": "<profile url>",
            "github": "<profile url>",
            "portfolio": "<website url>",
            "skills": ["<skill1>", "<skill2>", ...],
            "experience": [
                {
                    "role": "<job title>",
                    "company": "<company name>",
                    "technologies": ["<tech1>", "<tech2>", ...],
                    "points": ["<achievement1>", "<achievement2>", ...],
                    "date": "<duration>"
                }
            ],
            "projects": [
                {
                    "name": "<project name>",
                    "technologies": ["<tech1>", "<tech2>", ...],
                    "points": ["<achievement1>", "<achievement2>", ...],
                    "date": "<completion date>",
                    "projectLink": "<project url>"
                }
            ],
            "education": [
                {
                    "institution": "<school name>",
                    "degree": "<degree name>",
                    "startYear": "<start>",
                    "endYear": "<end>",
                    "marks": "<grade>"
                }
            ],
            "extra": ["<activity1>", "<activity2>", ...]
        }
    }`;
};