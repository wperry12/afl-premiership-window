# AFL Premiership Window

A React-based visualization tool for AFL ladder data that displays team performance on a scatter plot grid.

## Features

- **Automatic Data Scraping**: Runs the AFL ladder scraper on page load to get the latest data
- **Year Selection**: Choose from available years (defaults to current year)
- **Performance Grid**: Visualizes teams on a scatter plot where:
  - Y-axis: Points For (normalized per game)
  - X-axis: Points Against (normalized per game)
  - Better teams appear in the top-right quadrant
- **Team Logos**: Displays team logos from the `data/logos` directory
- **Premiership Highlighting**: Premiership winners have a green border
- **Responsive Design**: Modern, clean UI

## Prerequisites

- Node.js (v14 or higher)
- Python 3 (for the scraper)
- Python dependencies: `requests`, `beautifulsoup4`, `pandas`

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install requests beautifulsoup4 pandas
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

## Running the Application

### Quick Start (Recommended)

Use the provided start script for the easiest setup:

```bash
./start.sh
```

This will:
1. Check and install Python dependencies
2. Install Node.js dependencies if needed
3. Build the React application
4. Start the server on `http://localhost:3000`

### Manual Setup

#### Development Mode

Run both the React development server and the Express backend:

```bash
npm run dev
```

This will start:
- React development server on `http://localhost:3000`
- Express backend server on `http://localhost:3001`

#### Production Mode

Build and serve the production version:

```bash
npm run build-and-serve
```

This will:
1. Build the React application
2. Start the Express server serving the built files
3. Open `http://localhost:3000`

#### Alternative: Development with Hot Reload

If you want to run just the React development server (without the backend):

```bash
npm start
```

Note: In this mode, the scraper functionality won't work, but you can still view existing data.

## How It Works

1. **Data Scraping**: On page load, the app calls the Python scraper (`afl_ladder_scraper.py`) to fetch the latest AFL ladder data
2. **Data Processing**: The CSV data is parsed and teams are positioned on a grid based on their normalized performance metrics
3. **Visualization**: Teams are displayed as logos on a scatter plot, with premiership winners highlighted with green borders
4. **Year Selection**: Users can select different years to view historical data

## File Structure

```
afl-premiership-window/
├── src/
│   ├── components/
│   │   ├── LadderGrid.js          # Main visualization component
│   │   ├── LadderGrid.css
│   │   ├── TeamLogo.js            # Team logo display component
│   │   ├── TeamLogo.css
│   │   ├── YearSelector.js        # Year selection component
│   │   └── YearSelector.css
│   ├── App.js                     # Main app component
│   ├── App.css
│   ├── index.js                   # React entry point
│   └── index.css
├── data/
│   ├── logos/                     # Team logo images
│   ├── years/                     # Per-year CSV files
│   └── afl_ladder_with_premiers.csv
├── public/
│   └── index.html
├── server.js                      # Express backend server
├── afl_ladder_scraper.py         # Python scraper
└── package.json
```

## Data Sources

- **AFL Tables**: The scraper fetches data from `https://afltables.com/afl/seas/{year}.html`
- **Team Logos**: Stored in `data/logos/` with support for `.avif`, `.jpeg`, `.png`, and `.webp` formats

## Troubleshooting

### Python Scraper Issues

If the scraper fails to run:

1. Ensure Python 3 is installed and accessible as `python3`
2. Install required Python packages: `pip install requests beautifulsoup4 pandas`
3. Check that `afl_ladder_scraper.py` is in the root directory

### Logo Display Issues

If team logos don't display:

1. Check that logo files exist in `data/logos/`
2. Verify the team name mapping in `TeamLogo.js` matches your logo filenames
3. The app will fall back to showing team initials if logos are missing

### Port Conflicts

If you get port conflicts:

1. Change the port in `server.js` (line 6)
2. Or kill existing processes using the same port

## Browser Support

The application supports modern browsers with:
- ES6+ JavaScript support
- SVG support for the grid visualization
- Image format support (AVIF, JPEG, PNG, WebP)

## Contributing

To add new features or fix issues:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request
