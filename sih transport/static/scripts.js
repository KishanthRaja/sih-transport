document.getElementById('allocation-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const crewId = document.getElementById('crew_id').value;
    console.log(crewId);
    fetch('/allocate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'crew_id': crewId
        })
    })
    .then(response => response.text())  // Change to response.text() to handle HTML errors
    .then(text => {
        try {
            const data = JSON.parse(text);  // Try parsing the text as JSON
            const resultDiv = document.getElementById('result');
            if (data.error) {
                resultDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
            } else {
                resultDiv.innerHTML = `
                    <p><strong>Driver Name:</strong> ${data.driver_name}</p>
                    <p><strong>Conductor Name:</strong> ${data.conductor_name}</p>
                    <p><strong>Allocated Route:</strong> ${data.allocated_route}</p>
                    <p><strong>Route Stops:</strong> ${data.route_stops}</p>
                    <p><strong>Route Timings:</strong> ${data.route_timings}</p>
                    <p><strong>Bus Number:</strong> ${data.bus_number}</p>
                `;
            }
        } catch (e) {
            // Handle cases where text is not valid JSON
            console.error('Invalid JSON response:', e);
            document.getElementById('result').innerHTML = '<p style="color: red;">An error occurred. Please try again.</p>';
        }
    })
    .catch(error => console.error('Error:', error));
});

