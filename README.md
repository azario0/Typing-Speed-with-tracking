# 🚀 Typing Speed Test Application

A comprehensive typing speed testing application with real-time progress tracking and web dashboard visualization.

## 📋 Table of Contents
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [Usage](#-usage)
- [File Structure](#-file-structure)
- [API Documentation](#-api-documentation)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## ✨ Features

### Typing Speed Test Application
- 🎯 Real-time WPM (Words Per Minute) calculation
- 📊 Live accuracy tracking with visual feedback
- ⏱️ Precise timer functionality
- 🎨 Color-coded text highlighting (correct/incorrect)
- 📱 Clean, responsive GUI built with Tkinter
- 💾 Automatic progress saving to CSV
- 🌐 Web dashboard integration

### Web Dashboard
- 📈 Interactive progress charts with Chart.js
- 📊 Summary statistics (total tests, best WPM, averages)
- 📋 Complete test history table
- 🎨 Modern Bootstrap UI with gradients and animations
- 📱 Fully responsive design
- 🔄 Real-time data updates

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7+**
- **pip** (Python package installer)

### Required Python Packages
```bash
pip install flask requests
```

**Note**: `tkinter` comes pre-installed with most Python installations.

## 🛠️ Installation

1. **Clone or Download** this repository to your local machine

2. **Navigate** to the project directory:
   ```bash
   cd typing-speed-test
   ```

3. **Install dependencies**:
   ```bash
   pip install flask requests
   ```

4. **Verify installation** by checking Python version:
   ```bash
   python --version
   ```

## 🎮 Running the Application

### Step 1: Start the Web Server
First, start the Flask web server that handles the dashboard and data storage:

```bash
python app.py
```

You should see output like:
```
Starting Typing Speed Dashboard...
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 2: Launch the Typing Test
In a **separate terminal/command prompt**, run the typing test application:

```bash
python typing_speed_test.py
```

This will open the GUI typing test window.

### Step 3: View Your Dashboard
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## 📖 Usage

### Taking a Typing Test
1. **Start Typing**: Begin typing the displayed text in the input box
2. **Real-time Feedback**: Watch your WPM and accuracy update live
3. **Visual Cues**: Correctly typed characters appear in green, errors in red
4. **Auto-Complete**: Test automatically ends when you finish the sentence
5. **Progress Saved**: Results are automatically saved locally and sent to the web dashboard

### Viewing Progress
1. **Web Dashboard**: Visit `http://127.0.0.1:5000` for comprehensive stats
2. **Local File**: Check `typing_progress.csv` for raw data
3. **Charts**: View your progress trends over time
4. **History**: See all your previous test results

### Starting a New Test
- Click the **"New Test"** button to get a fresh sentence
- The app randomly selects from a pool of practice sentences

## 📁 File Structure

```
typing-speed-test/
├── typing_speed_test.py      # Main Tkinter GUI application
├── app.py                    # Flask web server
├── templates/
│   └── index.html           # Web dashboard template
├── typing_progress.csv      # Data storage (auto-created)
├── README.md               # This file
└── requirements.txt        # Python dependencies (optional)
```

## 🔌 API Documentation

### Save Test Result
**Endpoint**: `POST /api/save_result`

**Request Body**:
```json
{
  "wpm": 65.5,
  "accuracy": 98.2
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Result saved"
}
```

### Debug CSV Contents
**Endpoint**: `GET /debug/csv`

Returns the raw contents of the CSV file for troubleshooting.

## 🚨 Troubleshooting

### Common Issues

#### 1. "Error reading progress file: 'WPM'"
**Solution**: This indicates a corrupted CSV file. The app will automatically fix this by:
- Creating a backup of the corrupted file
- Generating a new CSV with correct headers
- Restarting with clean data

#### 2. "Could not connect to the server"
**Solution**: 
- Ensure the Flask server is running (`python app.py`)
- Check that the server is accessible at `http://127.0.0.1:5000`
- Verify no firewall is blocking the connection

#### 3. Chart Not Displaying
**Solution**:
- Complete at least one typing test to generate data
- Check browser console for JavaScript errors
- Ensure you have an internet connection (for Chart.js CDN)

#### 4. GUI Window Not Appearing
**Solution**:
- Ensure `tkinter` is installed: `python -c "import tkinter"`
- On Linux: `sudo apt-get install python3-tk`
- On macOS: Tkinter should be included with Python

### Manual CSV Reset
If you encounter persistent CSV issues:

```bash
# Backup your current data
mv typing_progress.csv typing_progress_backup.csv

# Restart the Flask app - it will create a new CSV file
python app.py
```

### Debug Mode
To see detailed error messages:

1. Check Flask console output for server errors
2. Visit `http://127.0.0.1:5000/debug/csv` to inspect CSV contents
3. Enable Python debugging in `typing_speed_test.py` by adding print statements

## 🎯 Performance Tips

### For Better Typing Scores
- 🏠 Use proper finger positioning (home row)
- 👀 Look at the screen, not your keyboard
- ⚡ Focus on accuracy first, speed will follow
- 🔄 Practice regularly for consistent improvement
- 🧘 Stay relaxed and maintain steady rhythm

### For Better App Performance
- 🔄 Restart the Flask server periodically for optimal performance
- 📁 Keep CSV files under 1000 entries for faster loading
- 💾 Consider archiving old data if the file gets very large

## 🔮 Future Enhancements

Potential improvements for future versions:
- 📊 Advanced statistics (typing patterns, error analysis)
- 🏆 Achievement system and goals
- 📈 Export data to different formats
- 🌐 Multi-user support
- 📝 Custom text import functionality
- ⌨️ Different typing test modes (numbers, symbols, code)

## 🤝 Contributing

Created by **azario0**

Feel free to submit issues and enhancement requests!

### Development Setup
1. Fork the repository
2. Make your changes
3. Test thoroughly with both GUI and web components
4. Submit a pull request with a clear description

## 📜 License

This project is open source and available for personal and educational use.

## 🙏 Acknowledgments

- Built with Python's Tkinter for the GUI
- Flask for the web server
- Bootstrap for responsive web design
- Chart.js for beautiful data visualizations

---

**Happy Typing! 🎉**

*Improve your typing skills one keystroke at a time.*