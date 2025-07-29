import React from 'react';
import './YearSelector.css';

const YearSelector = ({ selectedYear, availableYears, onYearChange }) => {
  return (
    <div className="year-selector">
      <select
        id="year-select"
        value={selectedYear}
        onChange={(e) => onYearChange(parseInt(e.target.value))}
        className="year-select"
      >
        {availableYears.map(year => (
          <option key={year} value={year}>
            {year}
          </option>
        ))}
      </select>
    </div>
  );
};

export default YearSelector; 