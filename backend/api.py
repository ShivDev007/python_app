from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'mysql'  # Docker Compose service name
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb'
mysql = MySQL(app)

# Create a MySQL table if it doesn't exist
with app.app_context():
    cursor = mysql.connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    mysql.connection.commit()
    cursor.close()

@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO data (name, email, message)
            VALUES (%s, %s, %s)
        ''', (name, email, message))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": "Data stored successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
