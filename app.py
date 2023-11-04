
from flask import Flask, request, jsonify
app = Flask(__name__)
import pymysql
from app import app
from app import app
from flaskext.mysql import MySQL

from flask import jsonify
from flask import flash, request

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'flask_demo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)		

		
@app.route('/add', methods=['POST'])
def add_project():
	try:
		_json = request.json
		_title = _json['title']
		_description = _json['description']
		_completed = _json['completed']
		# validate the received values
		if _title and _description and _completed and request.method == 'POST':
			conn = mysql.connect()
			cursor = conn.cursor()
			# save 
			sql = "INSERT INTO projects(title, description, completed) VALUES(%s, %s, %s)"
			data = (_title, _description, _completed,)
			
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Project added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


		
@app.route('/read')
def prjects():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM projects")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		

@app.route('/update', methods=['POST'])
def project_user():
	try:
		_json = request.json
		_id = _json['id']
		_title = _json['title']
		_description = _json['description']
		_completed = _json['completed']		
		# validate the received values
		if _title and _description and _completed and _id and request.method == 'POST':
			# save edits
			sql = "UPDATE projects SET _title=%s, _description=%s, _completed=%s WHERE id=%s"
			data = (_title, _description, _completed, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Project updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/delete/<int:id>')
def delete_project(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM projects WHERE id=%s", (id))
		conn.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
		
if __name__ == "__main__":
    app.run()