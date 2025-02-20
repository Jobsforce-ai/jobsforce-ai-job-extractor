const axios = require('axios');
const cheerio = require('cheerio');

exports.scrapeJobDescription = async (req, res) => {
  try {
    const { url } = req.query;
    if (!url) {
      return res.status(400).json({ error: "URL is required" });
    }

    // Extract job ID from URL
    const jobIdMatch = url.match(/currentJobId=(\d+)/);
    if (!jobIdMatch) {
      return res.status(400).json({
        error: "Invalid URL format",
        message: "Could not extract job ID from URL"
      });
    }

    const jobId = jobIdMatch[1];
    const directJobUrl = `https://www.linkedin.com/jobs/view/${jobId}`;

    console.log('Fetching job page:', directJobUrl);
    const { data: html } = await axios.get(directJobUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      }
    });

    const $ = cheerio.load(html);
    
    const possibleSelectors = [
      '.show-more-less-html__markup',
      '.jobs-description-content__text',
      '.jobs-box__html-content',
      '[data-job-detail-text]',
      '.jobs-description__content'
    ];

    let content = '';

    for (const selector of possibleSelectors) {
      const element = $(selector);
      if (element.length) {
        content = element.text().trim();
        console.log(`Found content using selector: ${selector}`);
        break;
      }
    }

    // If no content found from specific selectors, try paragraphs
    if (!content) {
      content = $('p[dir="ltr"]').map((_, el) => $(el).text().trim()).get().join('\n\n');
    }

    if (!content) {
      throw new Error('No job description content found');
    }

    // Clean up content
    content = content.replace(/\s+/g, ' ').trim();

    return res.json({
      success: true,
      job_description: content,
      length: content.length,
      original_url: url,
      direct_url: directJobUrl,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Scraping error:', error);
    return res.status(500).json({
      error: "Failed to scrape data",
      details: error.message,
      suggestion: "The page might require authentication or the job posting might have expired",
      timestamp: new Date().toISOString()
    });
  }
};