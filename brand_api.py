import pymysql
from app import app
from config import mysql
from flask import jsonify, request
from global_functions import validate_schema


conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)

brands_schema = {
    "type":"object",
    "properties":{
        "brand_name": {"type":"string"},
        "brand_id": {"type":"integer"},
    },
    'required':['brand_name']
}

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
    _json = request.json
    validation_repsonse = validate_schema(_json,brands_schema)
    if validation_repsonse == None:
        try:
            _brand_name = _json['brand_name']
            if request.method == 'POST':
                sqlQuery = "INSERT INTO brands(brand_name) VALUES(%s)"
                bindData = (_brand_name)
                cursor.execute("USE production")		
                cursor.execute(sqlQuery, bindData)
                id = cursor.lastrowid
                conn.commit()
                response = str(f'Brand added successfully! \nNew generated ID: {id}')
                return response,200
            else:
                return "Error due to wrong HTTP method selection"
        except Exception as e:
            return e
    elif validation_repsonse != None:
        return validation_repsonse
              

@app.route('/brands/update', methods=['PUT'])
def update_brand():
        _json = request.json
        validation_response = validate_schema(_json,brands_schema)
        _brand_id = _json['brand_id']
        if validation_response == None and _brand_id:
            try:
                _brand_name = _json['brand_name']
                if request.method == 'PUT':			
                    sqlQuery = "UPDATE brands SET brand_name=%s WHERE brand_id=%s"
                    bindData = (_brand_name, _brand_id)
                    cursor.execute("USE production")
                    cursor.execute(sqlQuery, bindData)
                    conn.commit()
                    response = jsonify('Brand updated successfully!')
                    response.status_code = 200
                    return response
                else:
                    return "Error due to wrong HTTP method selection"
            except Exception as e:
                return e
        elif validation_response != None:
            return validation_response
     

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


@app.errorhandler(400)
def handle_400(e):
    message = {
        'status': 400,
        'message': 'Error in JSON body format'
    }
    response = jsonify(message)
    response.status_code = 400
    return response