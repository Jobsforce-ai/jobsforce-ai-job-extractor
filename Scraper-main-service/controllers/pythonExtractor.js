const axios = require('axios');

exports.getJobs = async (req, res) => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/api/jobs');        
        res.status(200).json(response.data);
    } catch (error) {
        console.error("Error fetching jobs:", error.message);
        res.status(500).json({ error: "Failed to fetch jobs" });
    }
};
