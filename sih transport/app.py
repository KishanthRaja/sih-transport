from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load the CSV files
table1 = pd.read_csv('sih_delhi.csv')
table2 = pd.read_csv('sih_dtc.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/allocate', methods=['POST'])
def allocate_route():
    crew_id = request.form.get('Crew_Id')  # Ensure this matches your form input name
    if crew_id is None:
        return jsonify({'error': 'Crew ID not provided'}), 400
    
    crew_id = crew_id.strip().upper()  # Strip spaces and convert to uppercase  # Strip spaces and convert to uppercase
    crew_row = table2[table2['Crew_Id'].str.strip().str.upper() == crew_id]
    if crew_row.empty:
        return jsonify({'error': 'Crew ID not found'}), 404
    
    familiar_routes = crew_row['Familiar Route Number'].values[3].split(', ')
    
    # Choose a route from the familiar routes
    allocated_route = familiar_routes[0]  # You can apply a more complex scheduling algorithm here
    
    # Get details from table1
    route_details = table1[table1['Route Number'] == allocated_route]
    
    if route_details.empty:
        return jsonify({'error': 'Route details not found'}), 404
    
    route_info = route_details.to_dict(orient='records')[0]
    
    response = {
        'driver_name': crew_row['Driver Name'].values[0],
        'conductor_name': crew_row['Conductor Name'].values[1],
        'allocated_route': allocated_route,
        'route_stops': route_info['Route Stops'],
        'route_timings': route_info['Route Timings'],
        'bus_number': route_info['Bus Number']
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
