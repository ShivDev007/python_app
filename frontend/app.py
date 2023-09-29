from flask import Flask, render_template, request, jsonify
import requests  # Add this import to make HTTP requests

app = Flask(__name__)

# Define the URL of the backend API
backend_api_url = 'http://api:5000/api/data'  # 'api' is the service name in Docker Compose

# Define a route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Create a JSON payload with the data
        data = {
            'name': name,
            'email': email,
            'message': message
        }

        try:
            # Send a POST request to the backend API
            response = requests.post(backend_api_url, json=data)

            # Check if the request was successful (status code 201)
            if response.status_code == 201:
                print("Data sent successfully to the backend API.")
            else:
                print("Failed to send data to the backend API.")
        except Exception as e:
            print(f"Error sending data to the backend API: {str(e)}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
