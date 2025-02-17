const axios = require('axios');
const redis = require('redis');

const client = redis.createClient({
    host: "jobsforce_redis",
    port: 6379
});

exports.getJobs = async (req, res) => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/api/jobs');        
        res.status(200).json(response.data);
    } catch (error) {
        console.error("Error fetching jobs:", error.message);
        res.status(500).json({ error: "Failed to fetch jobs" });
    }
};

exports.getCachedJobs = async(req, res) => {
    client.get("jobs", async(err, data) => {
        if (err) {
            console.error("Redis GET all jobs error:", err);
            return res.status(500).json({ error: "Redis Error" });
        }
        if (data) {
            return res.json(JSON.parse(data));
        }

        try {
            const response = await axios.get('http://127.0.0.1:5000/api/jobs');
            const jobs = response.data;

            client.setEx("jobs", 600, JSON.stringify(jobs), (err, reply) => {
                if (err) console.error("Redis SET Error:", err);
            }); //cache for 10 mins

            res.json(jobs);
        } catch (error) {
            console.error("Error fetching jobs:", error.message);
            res.status(500).json({ error: "Failed to fetch jobs" });
        }
        
    })
}
