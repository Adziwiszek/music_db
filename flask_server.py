import json
from flask import Flask, request, jsonify
import db_operations

app = Flask(__name__)
db = None


@app.route("/")
def main():
    '''Main page of the website'''
    return "<p>Your favourite music library xd</p>"

# CREATE


@app.route("/<string:table_name>", methods=['POST'])
def add_entry(table_name):
    '''Adds entry to the data base
        Parameters:
        table_name (string): name of a table
        data (dictionary): given through requests data of new entry'''
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            res_message = db.add_entry(table_name, data)
            return jsonify(res_message)
        except Exception as e:
            return jsonify({'error': e})

# DELETE


@app.route('/<string:table_name>/<int:id>', methods=['DELETE'])
def delete_entry_by_id(table_name, id):
    '''Deletes an entry from the data base
        Parameters:
        table_name (string): name of a table
        id (int): id of an entry 
        '''
    if request.method == 'DELETE':
        try:
            res_message = db.delete_by_id(table_name=table_name, del_id=id)
            return jsonify({'message': res_message})
        except:
            return f"Error while deleting an entry with id: {id} in table: {table_name}"

# READ


@app.route('/<string:table_name>/<int:id>', methods=['GET'])
def get_entry_by_id(table_name, id):
    '''Returns an entry with a given id from a table, in json format'''
    if request.method == 'GET':
        json_res = db.get_entry(table_name=table_name, id=id)
        return json_res

# READ


@app.route('/<string:table_name>', methods=['GET'])
def get_table(table_name):
    '''Returns content of a table, in json format
        Parameters:
        table_name (string): name of a table'''
    if request.method == 'GET':
        json_res = db.display_table(table_name=table_name)
        return json_res

# UPDATE


@app.route('/<string:table_name>', methods=['PUT'])
def update_entry(table_name):
    '''Updates an entry in the data base
        Parameters:
        table_name (string): name of a table
        data (dictionary): given through requests data of new entry'''
    if request.method == 'PUT':
        try:
            data = request.form.to_dict()
            res_message = db.update_entry(table_name, data)
            return jsonify(res_message)
        except Exception as e:
            return jsonify({'error': e})


if __name__ == "__main__":
    '''Main function of the file'''
    db = db_operations.Database()
    app.run(debug=True)
    db.session.close()

# Set-ExecutionPolicy Unrestricted -Scope Process
# .\env\Scripts\activate
