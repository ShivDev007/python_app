from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'sql_db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb'

# Connect to MySQL
mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

# Create a MySQL table if it doesn't exist
with mysql.cursor() as cursor:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    mysql.commit()

@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        with mysql.cursor() as cursor:
            cursor.execute('''
                INSERT INTO data (name, email, message)
                VALUES (%s, %s, %s)
            ''', (name, email, message))
            mysql.commit()

        return jsonify({"message": "Data stored successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
