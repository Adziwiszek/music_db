import json
from flask import Flask, request, jsonify
import db_operations
app = Flask(__name__)
db = None

@app.route("/")
def main():
    return "<p>Your favourite music library xd</p>"

# CREATE
@app.route("/<string:table_name>", methods=['POST'])
def add_entry(table_name):
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            res_message = db.add_entry(table_name,data)
            return jsonify(res_message)
        except Exception as e:
            return jsonify({'error': e})

# DELETE
@app.route('/<string:table_name>/<int:id>', methods=['DELETE'])
def delete_entry_by_id(table_name, id):
    if request.method == 'DELETE':
        try:
            res_message = db.delete_by_id(table_name=table_name, del_id=id)
            return jsonify({'message': res_message})
        except:
            return f"Error while deleting an entry with id: {id} in table: {table_name}"

# READ
@app.route('/<string:table_name>/<int:id>', methods=['GET'])
def get_entry_by_id(table_name, id):
    if request.method == 'GET':
        json_res = db.get_entry(table_name=table_name,id=id)
        return json_res

# READ
@app.route('/<string:table_name>', methods=['GET'])
def get_table(table_name):
    if request.method == 'GET':
        json_res = db.display_table(table_name=table_name)
        return json_res

# UPDATE
@app.route('/<string:table_name>', methods=['PUT'])
def update_entry(table_name):
    if request.method == 'PUT':
        try:
            data = request.form.to_dict()
            res_message = db.update_entry(table_name,data)
            return jsonify(res_message)
        except Exception as e:
            return jsonify({'error': e})


if __name__ == "__main__":
    db = db_operations.Database()
    app.run(debug=True)
    db.session.close()
    
#Set-ExecutionPolicy Unrestricted -Scope Process
#.\env\Scripts\activate
