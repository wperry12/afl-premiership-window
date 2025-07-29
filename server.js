const express = require('express');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the webpack build
app.use(express.static(path.join(__dirname, 'build')));

// Serve data files
app.use('/data', express.static(path.join(__dirname, 'data')));

// API endpoint to run the Python scraper
app.post('/api/run-scraper', async (req, res) => {
  try {
    console.log('Running AFL ladder scraper...');
    
    const pythonProcess = spawn('python3', ['afl_ladder_scraper.py'], {
      cwd: __dirname
    });

    let output = '';
    let errorOutput = '';

    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
      console.log('Scraper output:', data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
      console.error('Scraper error:', data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        console.log('Scraper completed successfully');
        res.json({ 
          success: true, 
          message: 'Scraper completed successfully',
          output: output 
        });
      } else {
        console.error(`Scraper failed with code ${code}`);
        res.status(500).json({ 
          success: false, 
          message: 'Scraper failed',
          error: errorOutput 
        });
      }
    });

    pythonProcess.on('error', (error) => {
      console.error('Failed to start scraper:', error);
      res.status(500).json({ 
        success: false, 
        message: 'Failed to start scraper',
        error: error.message 
      });
    });

  } catch (error) {
    console.error('Error running scraper:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Internal server error',
      error: error.message 
    });
  }
});

// Serve the React app for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Open http://localhost:${PORT} to view the application`);
}); 