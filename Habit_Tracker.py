from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime, timedelta

app = Flask(__name__)

file_name = 'habit_tracker.csv'

# Initialize CSV file if it does not exist
def initialize_csv(file_name):
    try:
        with open(file_name, mode='r') as file:
            pass
    except FileNotFoundError:
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Reading (mins)', 'Workout (mins)', 'Meditation (mins)', 'Studying (mins)'])

initialize_csv(file_name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log', methods=['GET', 'POST'])
def log_activities():
    if request.method == 'POST':
        date = datetime.now().strftime('%Y-%m-%d')
        reading = request.form['reading']
        workout = request.form['workout']
        meditation = request.form['meditation']
        studying = request.form['studying']

        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, reading, workout, meditation, studying])
        
        return redirect(url_for('index'))
    return render_template('log.html')

@app.route('/progress', methods=['GET', 'POST'])
def view_progress():
    progress_data = {}
    if request.method == 'POST':
        days = int(request.form['days'])
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            total_reading, total_workout, total_meditation, total_studying = 0, 0, 0, 0
            count = 0

            for row in reader:
                date = datetime.strptime(row[0], '%Y-%m-%d')
                if start_date <= date <= end_date:
                    total_reading += int(row[1])
                    total_workout += int(row[2])
                    total_meditation += int(row[3])
                    total_studying += int(row[4])
                    count += 1

            if count > 0:
                progress_data = {
                    'reading': total_reading // count,
                    'workout': total_workout // count,
                    'meditation': total_meditation // count,
                    'studying': total_studying // count,
                    'days': days
                }

    return render_template('progress.html', progress_data=progress_data)