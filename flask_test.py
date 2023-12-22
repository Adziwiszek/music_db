import json
from flask import Flask, request, jsonify
import db_operations
app = Flask(__name__)
db = None

@app.route("/")
def main():
    return "<p>Your favourite music library xd</p>"

#TODO 

@app.route("/<string:table_name>", methods=['POST'])
def add_entry(table_name):
    try:
        data = request.form.to_dict()
        db.add_entry(table_name,data)
        return jsonify(f'added: {data}')
    except Exception as e:
        return jsonify({'error': e})

@app.route('/<string:table_name>/<int:id>', methods=['DELETE'])
def delete_entry_by_id(table_name, id):
    try:
        res_message = db.delete_by_id(table_name=table_name, del_id=id)
        return jsonify({'message': res_message})
    except:
        return f"Error while deleting an entry with id: {id} in table: {table_name}"

@app.route('/<string:table_name>/<int:id>', methods=['GET'])
def get_entry_by_id(table_name, id):
    json_res = db.get_entry(table_name=table_name,id=id)
    return json_res
    
@app.route('/<string:table_name>', methods=['GET'])
def get_table(table_name):
    json_res = db.display_table(table_name=table_name)
    return json_res

if __name__ == "__main__":
    db = db_operations.Database()
    app.run(debug=True)
    db.session.close()
    
#Set-ExecutionPolicy Unrestricted -Scope Process
#.\env\Scripts\activate