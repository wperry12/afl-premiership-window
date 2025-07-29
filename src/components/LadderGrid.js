import React, { useMemo } from 'react';
import TeamLogo from './TeamLogo';
import YearSelector from './YearSelector';
import './LadderGrid.css';

const LadderGrid = ({ yearData, year, selectedYear, availableYears, onYearChange }) => {
  const processedData = useMemo(() => {
    if (!yearData || yearData.length === 0) return [];

    const teamsWithData = yearData.map(team => {
      const played = parseInt(team.Played) || 1;
      const forPoints = parseInt(team.For) || 0;
      const againstPoints = parseInt(team.Against) || 0;
      
      // Normalize points by games played
      const normalizedFor = forPoints / played;
      const normalizedAgainst = againstPoints / played;
      
      return {
        ...team,
        normalizedFor,
        normalizedAgainst,
        position: parseInt(team.Position) || 0,
        isPremier: team.Premiers === 'True'
      };
    });

    

    // Calculate ranks for Points For (higher is better = rank 1)
    const sortedByFor = [...teamsWithData].sort((a, b) => b.normalizedFor - a.normalizedFor);
    const forRanks = {};
    sortedByFor.forEach((team, index) => {
      forRanks[team.Team] = index + 1;
    });

    // Calculate ranks for Points Against (lower is better = rank 1)
    const sortedByAgainst = [...teamsWithData].sort((a, b) => a.normalizedAgainst - b.normalizedAgainst);
    const againstRanks = {};
    sortedByAgainst.forEach((team, index) => {
      againstRanks[team.Team] = index + 1;
    });

    // Add ranks to each team
    return teamsWithData.map(team => ({
      ...team,
      forRank: forRanks[team.Team],
      againstRank: againstRanks[team.Team]
    })).sort((a, b) => a.position - b.position);
  }, [yearData]);

  if (!processedData || processedData.length === 0) {
    return (
      <div className="ladder-grid">
        <div className="no-data">
          <h3>No data available for {year}</h3>
        </div>
      </div>
    );
  }

  // Calculate grid dimensions for ranks
  const maxRank = processedData.length;
  const minRank = 1;

  // Create a proper n x n grid where each cell represents a rank intersection
  const gridSize = Math.max(400, maxRank * 30); // 30px per rank cell
  const cellSize = gridSize / maxRank; // Size of each grid cell
  const gridWidth = gridSize;
  const gridHeight = gridSize;
  const padding = 120; // Padding for axis labels

  const getPosition = (team) => {
    // X-axis: Rank by Points Against (lower is better, so invert)
    // Position at the center of the grid cell for that rank
    const x = 120 + (maxRank - team.againstRank) * cellSize + (cellSize / 2);
    // Y-axis: Rank by Points For (higher is better, so invert)
    // Position at the center of the grid cell for that rank
    const y = 120 + (team.forRank - 1) * cellSize + (cellSize / 2);
    return { x, y };
  };

    return (
    <div className="ladder-grid">
      <div className="grid-header">
        <h2 className="grid-title">AFL Premiership Window - {year}</h2>
        <div className="year-selector-container">
          <YearSelector 
            selectedYear={selectedYear}
            availableYears={availableYears}
            onYearChange={onYearChange}
          />
        </div>
      </div>
      
      <div className="grid-container">
          <svg width={gridWidth + 240} height={gridHeight + 240} className="grid-svg" viewBox={`0 0 ${gridWidth + 240} ${gridHeight + 240}`}>
            {/* Grid lines - create proper rank grid */}
            <defs>
              <pattern id="rankGrid" width={cellSize} height={cellSize} patternUnits="userSpaceOnUse">
                <path d={`M ${cellSize} 0 L 0 0 0 ${cellSize}`} fill="none" stroke="#e5e7eb" strokeWidth="1"/>
              </pattern>
            </defs>
                        {/* Premiership window highlight (ranks 1-6 on both axes) */}
            <rect 
              x={120 + (maxRank - 6) * cellSize} 
              y={120} 
              width={6 * cellSize} 
              height={6 * cellSize} 
              fill="#dcfce7" 
              opacity="0.3"
            />
            
            <rect x={120} y={120} width={gridSize} height={gridSize} fill="url(#rankGrid)" />
            
            {/* Axis labels - positioned outside the grid */}
            <text x={120 + (gridSize / 2)} y={120 + gridSize + 60} textAnchor="middle" className="axis-label">
              Rank by Points Against (per game)
            </text>
            <text x={60} y={120 + (gridSize / 2)} textAnchor="middle" className="axis-label" transform={`rotate(-90, 60, ${120 + (gridSize / 2)})`}>
              Rank by Points For (per game)
            </text>
          
          {/* Scale markers */}
          <text x={120} y={120 + gridSize + 35} textAnchor="middle" className="scale-marker">
            Rank {maxRank}
          </text>
          <text x={120 + gridSize} y={120 + gridSize + 35} textAnchor="middle" className="scale-marker">
            Rank 1
          </text>
          <text x={85} y={120} textAnchor="middle" className="scale-marker" transform={`rotate(-90, 85, 120)`}>
            Rank 1
          </text>
          <text x={85} y={120 + gridSize} textAnchor="middle" className="scale-marker" transform={`rotate(-90, 85, ${120 + gridSize})`}>
            Rank {maxRank}
          </text>
          
          {/* Team logos */}
          {processedData.map((team, index) => {
            const position = getPosition(team);
            return (
              <g key={team.Team} className="team-group">
                <TeamLogo 
                  team={team.Team}
                  x={position.x}
                  y={position.y}
                  isPremier={team.isPremier}
                />
              </g>
            );
          })}
        </svg>
      </div>
      
      <div className="grid-legend">
        <div className="legend-item">
          <div className="legend-logo premier"></div>
          <span>Premiership Winner</span>
        </div>
      </div>
    </div>
  );
};

export default LadderGrid; 