import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import LadderGrid from './components/LadderGrid';
import YearSelector from './components/YearSelector';

function App() {
  const [data, setData] = useState([]);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [availableYears, setAvailableYears] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Run scraper on page load
  useEffect(() => {
    const runScraper = async () => {
      try {
        setLoading(true);
        console.log('Running AFL ladder scraper...');
        
        // Call the Python scraper
        const response = await axios.post('/api/run-scraper');
        console.log('Scraper completed:', response.data);
        
        // Load the data
        await loadData();
      } catch (err) {
        console.error('Error running scraper:', err);
        // If scraper fails, try to load existing data
        console.log('Scraper failed, trying to load existing data...');
        await loadData();
      }
    };

    runScraper();
  }, []);

  const loadData = async () => {
    try {
      const response = await axios.get('/data/afl_ladder_with_premiers.csv');
      const csvData = response.data;
      
      // Parse CSV data
      const lines = csvData.split('\n');
      const headers = lines[0].split(',');
      const parsedData = lines.slice(1).map(line => {
        const values = line.split(',');
        const row = {};
        headers.forEach((header, index) => {
          row[header.trim()] = values[index]?.trim() || '';
        });
        return row;
      }).filter(row => row.Year && row.Team);

      setData(parsedData);
      
      // Extract available years
      const years = [...new Set(parsedData.map(row => parseInt(row.Year)))].sort((a, b) => b - a);
      setAvailableYears(years);
      
      // Set default year to current year or most recent available year
      const currentYear = new Date().getFullYear();
      const defaultYear = years.includes(currentYear) ? currentYear : years[0];
      setSelectedYear(defaultYear);
      
      setLoading(false);
    } catch (err) {
      console.error('Error loading data:', err);
      setError('Failed to load AFL data.');
      setLoading(false);
    }
  };

  const getYearData = () => {
    return data.filter(row => parseInt(row.Year) === selectedYear);
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <h2>Loading AFL Data...</h2>
          {/* <p>Running scraper and loading data...</p> */}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <div className="error">
          <h2>Error</h2>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <main className="app-main">
        <LadderGrid 
          yearData={getYearData()}
          year={selectedYear}
          selectedYear={selectedYear}
          availableYears={availableYears}
          onYearChange={setSelectedYear}
        />
      </main>
    </div>
  );
}

export default App; 