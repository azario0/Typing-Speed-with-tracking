from flask import Flask, render_template, request, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__)
PROGRESS_FILE = "typing_progress.csv"

def init_progress_file():
    """Creates the CSV file with a header if it doesn't exist."""
    if not os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "WPM", "Accuracy"])
        print(f"Created new progress file: {PROGRESS_FILE}")

def validate_and_fix_csv():
    """Validates and fixes the CSV file structure if needed."""
    if not os.path.exists(PROGRESS_FILE):
        init_progress_file()
        return
    
    try:
        # Read the file to check its structure
        with open(PROGRESS_FILE, 'r', newline='') as f:
            content = f.read().strip()
        
        # Check if file is empty
        if not content:
            print("CSV file is empty, reinitializing...")
            init_progress_file()
            return
        
        # Check if header is correct
        with open(PROGRESS_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            
        expected_header = ["Timestamp", "WPM", "Accuracy"]
        if header != expected_header:
            print(f"Invalid header found: {header}")
            print(f"Expected: {expected_header}")
            
            # Backup the corrupted file
            backup_file = f"{PROGRESS_FILE}.backup"
            if os.path.exists(backup_file):
                os.remove(backup_file)
            os.rename(PROGRESS_FILE, backup_file)
            print(f"Corrupted file backed up as: {backup_file}")
            
            # Recreate the file
            init_progress_file()
            print("CSV file has been reset with correct headers")
            
    except Exception as e:
        print(f"Error validating CSV file: {e}")
        # Create backup and reinitialize
        backup_file = f"{PROGRESS_FILE}.error_backup"
        if os.path.exists(backup_file):
            os.remove(backup_file)
        if os.path.exists(PROGRESS_FILE):
            os.rename(PROGRESS_FILE, backup_file)
        init_progress_file()

@app.route('/')
def dashboard():
    """Renders the main dashboard page."""
    # Validate CSV file first
    validate_and_fix_csv()
    
    history = []
    summary_stats = {
        "total_tests": 0,
        "avg_wpm": 0,
        "avg_accuracy": 0,
        "best_wpm": 0
    }
    
    try:
        with open(PROGRESS_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            
            # Check if reader has the expected fieldnames
            expected_fields = {"Timestamp", "WPM", "Accuracy"}
            if not expected_fields.issubset(set(reader.fieldnames or [])):
                raise ValueError(f"CSV missing required columns. Found: {reader.fieldnames}")
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 because header is row 1
                try:
                    # Validate that required fields exist and are not empty
                    if not row.get('Timestamp') or not row.get('WPM') or not row.get('Accuracy'):
                        print(f"Skipping incomplete row {row_num}: {row}")
                        continue
                    
                    # Convert strings to appropriate types
                    row['WPM'] = float(row['WPM'])
                    row['Accuracy'] = float(row['Accuracy'])
                    
                    # Parse and format timestamp
                    try:
                        parsed_time = datetime.strptime(row['Timestamp'], "%Y-%m-%d %H:%M:%S")
                        row['Timestamp'] = parsed_time.strftime("%b %d, %Y %I:%M %p")
                    except ValueError:
                        # If timestamp parsing fails, keep original
                        print(f"Could not parse timestamp in row {row_num}: {row['Timestamp']}")
                    
                    history.append(row)
                    
                except (ValueError, TypeError) as e:
                    print(f"Error processing row {row_num}: {e} - Row: {row}")
                    continue
        
        # Calculate summary statistics
        if history:
            summary_stats["total_tests"] = len(history)
            total_wpm = sum(item['WPM'] for item in history)
            total_acc = sum(item['Accuracy'] for item in history)
            summary_stats["avg_wpm"] = round(total_wpm / len(history), 2)
            summary_stats["avg_accuracy"] = round(total_acc / len(history), 2)
            summary_stats["best_wpm"] = max(item['WPM'] for item in history)
            
        # Reverse history to show most recent first
        history.reverse()
        
    except FileNotFoundError:
        print("Progress file not found, creating new one...")
        init_progress_file()
    except Exception as e:
        print(f"Error reading progress file: {e}")
        # Try to fix the file
        validate_and_fix_csv()
    
    return render_template('index.html', history=history, summary_stats=summary_stats)

@app.route('/api/save_result', methods=['POST'])
def save_result():
    """API endpoint to receive and save a new typing test result."""
    data = request.get_json()
    if not data or 'wpm' not in data or 'accuracy' not in data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400
    
    try:
        wpm = float(data['wpm'])
        accuracy = float(data['accuracy'])
        
        # Validate the data ranges
        if wpm < 0 or wpm > 500:  # Reasonable WPM limits
            return jsonify({"status": "error", "message": "Invalid WPM value"}), 400
        if accuracy < 0 or accuracy > 100:
            return jsonify({"status": "error", "message": "Invalid accuracy value"}), 400
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Ensure CSV file exists and has correct structure
        validate_and_fix_csv()
        
        # Append the new result
        with open(PROGRESS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, wpm, accuracy])
        
        print(f"Saved result: WPM={wpm}, Accuracy={accuracy}%")
        return jsonify({"status": "success", "message": "Result saved"})
        
    except (ValueError, TypeError) as e:
        print(f"Data format error: {e}")
        return jsonify({"status": "error", "message": f"Invalid data format: {e}"}), 400
    except IOError as e:
        print(f"File I/O error: {e}")
        return jsonify({"status": "error", "message": f"Could not write to file: {e}"}), 500

@app.route('/debug/csv')
def debug_csv():
    """Debug endpoint to check CSV file contents."""
    try:
        with open(PROGRESS_FILE, 'r') as f:
            content = f.read()
        return f"<pre>CSV Content:\n{content}</pre>"
    except FileNotFoundError:
        return "CSV file not found"
    except Exception as e:
        return f"Error reading CSV: {e}"

if __name__ == '__main__':
    print("Starting Typing Speed Dashboard...")
    validate_and_fix_csv()
    app.run(debug=False)