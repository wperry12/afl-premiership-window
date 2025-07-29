import React, { useState, useRef, useLayoutEffect } from 'react';
import './TeamLogo.css';

const TeamLogo = ({ team, x, y, isPremier }) => {
  const [imageError, setImageError] = useState(false);
  const [showTooltip, setShowTooltip] = useState(false);
  
  // Team name mapping for logo files
  const getLogoPath = (teamName) => {
    const teamMappings = {
      'Adelaide': 'Adelaide.avif',
      'Brisbane Bears': 'Brisbane Bears.avif',
      'Brisbane Lions': 'Brisbane Lions.avif',
      'Carlton': 'Carlton.avif',
      'Collingwood': 'Collingwood.avif',
      'Essendon': 'Essendon.avif',
      'Fitzroy': 'Fitzroy.png',
      'Footscray': 'Footscray.png',
      'Fremantle': 'Fremantle.avif',
      'Geelong': 'Geelong.avif',
      'Gold Coast': 'Gold Coast.jpeg',
      'Greater Western Sydney': 'Greater Western Sydney.avif',
      'Hawthorn': 'Hawthorn.avif',
      'Kangaroos': 'Kangaroos.avif',
      'Melbourne': 'Melbourne.avif',
      'North Melbourne': 'North Melbourne.avif',
      'Port Adelaide': 'Port Adelaide.avif',
      'Richmond': 'Richmond.webp',
      'South Melbourne': 'South Melbourne.avif',
      'St Kilda': 'St Kilda.avif',
      'Sydney': 'Sydney.avif',
      'West Coast': 'West Coast.avif',
      'Western Bulldogs': 'Western Bulldogs.png'
    };
    
    return teamMappings[teamName] || null;
  };

  const logoPath = getLogoPath(team);
  
  if (!logoPath) {
    // Fallback to text if no logo found
    return (
      <g className="team-logo-fallback">
        <circle 
          cx={x} 
          cy={y} 
          r="15" 
          fill="#e5e7eb" 
          stroke={isPremier ? "#10b981" : "#d1d5db"} 
          strokeWidth="2"
        />
        <text 
          x={x} 
          y={y + 4} 
          textAnchor="middle" 
          className="fallback-text"
        >
          {team.charAt(0)}
        </text>
      </g>
    );
  }

  const handleImageError = () => {
    setImageError(true);
  };

  if (imageError) {
    // Fallback to text if image fails to load
    return (
      <g className="team-logo-fallback">
        <circle 
          cx={x} 
          cy={y} 
          r="15" 
          fill="#e5e7eb" 
          stroke={isPremier ? "#10b981" : "#d1d5db"} 
          strokeWidth="2"
        />
        <text 
          x={x} 
          y={y + 4} 
          textAnchor="middle" 
          className="fallback-text"
        >
          {team.charAt(0)}
        </text>
      </g>
    );
  }

  const bringToFront = (evt) => {
    const g = evt.currentTarget;
    if (g && g.parentNode) {
      g.parentNode.appendChild(g);     // move node to end of <svg>
    }
  };

  return (
    <g className="team-logo">
      <defs>
        <clipPath id={`clip-${team.replace(/\s+/g, '-')}`}>
          <circle cx={x} cy={y} r="15" />
        </clipPath>
      </defs>

      {showTooltip && (
            <Tooltip x={x} y={y - 20} text={team} />
        )}
      
      {/* Border circle */}
      <circle 
        cx={x} 
        cy={y} 
        r="17" 
        fill="none" 
        stroke={isPremier ? "#10b981" : "#d1d5db"} 
        strokeWidth="2"
      />

      {/* Tooltip
      {showTooltip && (
        <g className="tooltip">
          <rect
            x={x - 40}
            y={y - 35}
            width="80"
            height="20"
            fill="rgba(0, 0, 0, 0.8)"
            rx="4"
          />
          <text
            x={x}
            y={y - 20}
            textAnchor="middle"
            className="tooltip-text"
          >
            {team}
          </text>
        </g>
      )} */}

        
      
      {/* Logo image - scaled to fit height, crop width if needed */}
      <image
        href={`/data/logos/${logoPath}`}
        x={x - 15}
        y={y - 15}
        width="30"
        height="30"
        preserveAspectRatio="xMidYMid slice"
        clipPath={`url(#clip-${team.replace(/\s+/g, '-')})`}
        onError={handleImageError}
      />
      
      {/* Invisible circle for hover area */}
      <circle 
        cx={x} 
        cy={y} 
        r="20" 
        fill="transparent"
        className="hover-area"
        onMouseEnter={(e) => {
            bringToFront(e);
            setShowTooltip(true);
          }}
        onMouseLeave={() => setShowTooltip(false)}
      />
      
      
    </g>
  );
};

const Tooltip = ({ x, y, text }) => {
    const textRef = useRef(null);
    const [box, setBox] = useState({ w: 0, h: 0 });
  
    // Measure the <text> after it’s rendered
    useLayoutEffect(() => {
      if (textRef.current) {
        const { width, height } = textRef.current.getBBox();
        // + padding so letters don’t touch the edge
        setBox({ w: width + 16, h: height + 10 });
      }
    }, [text]);
  
    return (
      <g className="tooltip" pointerEvents="none">
        <rect
          x={x - box.w / 2}
          y={y - box.h}
          width={box.w}
          height={box.h}
          rx="4"
          fill="rgba(0,0,0,0.85)"
        />
        <text
          ref={textRef}
          x={x}
          y={y - box.h / 2 + 3}   /* vertically centres text */
          textAnchor="middle"
          fill="#fff"
          fontSize="11"
          style={{ userSelect: 'none' }}
        >
          {text}
        </text>
      </g>
    );
  };

export default TeamLogo; 