import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import request


# @app.route("/")
# def main_page():
#     return "<center><h1>*** API making in progress ***</h1></center>"

conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)

@app.route('/brands', methods=['GET'])
def view_brand():
    try:
        cursor.execute("USE production")
        cursor.execute("SELECT brand_id, brand_name FROM brands")
        empRows = cursor.fetchall()
        response = jsonify(empRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
      

@app.route('/brands/<int:id>', methods=['GET'])
def view_brand_details(id):
    try:
        cursor.execute("USE production")
        cursor.execute(f"SELECT brand_id, brand_name FROM brands WHERE brand_id ={id}")
        empRow = cursor.fetchone()
        response = jsonify(empRow)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
     

@app.route('/brands/create', methods=['POST'])
def create_brand():
    try:        
        _json = request.json
        _brand_name = _json['brand_name']
        if _brand_name and request.method == 'POST':
            sqlQuery = "INSERT INTO brands(brand_name) VALUES(%s)"
            bindData = (_brand_name)
            cursor.execute("USE production")		
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Brand added successfully!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
              

@app.route('/brands/update', methods=['PUT'])
def update_brand():
    try:
        _json = request.json
        _brand_id = _json['brand_id']
        _brand_name = _json['brand_name']
        if _brand_id and _brand_name and _brand_id and request.method == 'PUT':			
            sqlQuery = "UPDATE brands SET brand_name=%s WHERE brand_id=%s"
            bindData = (_brand_name, _brand_id)
            cursor.execute("USE production")
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Brand updated successfully!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
     

@app.route('/brands/delete/<int:id>', methods=['DELETE'])
def delete_brand(id):
    try:
        cursor.execute("USE production")
        cursor.execute("DELETE FROM brands WHERE brand_id =%s", (id))
        conn.commit()
        response = jsonify('Brand deleted successfully!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    
        
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response
