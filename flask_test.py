import json
from flask import Flask, request, jsonify
import db_operations
app = Flask(__name__)
db = None
@app.route("/")
def main():
    return "<p>Kurs programowania w Pythonie</p>"

#TODO 
#1) add "Create" function to server,
#   

@app.route("/<string:table_name>", methods=['POST'])
def add_band(table_name):
    try:
        data = request.form.to_dict()
        db.add_entry(table_name,data)
        return jsonify(f'added: {data}')
    except Exception as e:
        return jsonify({'error': e})

@app.route("/wyklad12")
def wyklad():
    return "<p>Usługi sieciowe</p>"

@app.route('/bands/<int:id>', methods=['GET'])
def get_band(id):
    json_res = db.get_entry(table_name='bands',id=id)
    return json_res
    
@app.route('/<string:table_name>', methods=['GET'])
def get_table(table_name):
    #print(f"given table name: {table_name}")
    json_res = db.display_table(table_name=table_name)
    return json_res

if __name__ == "__main__":
    db = db_operations.Database()
    app.run(debug=True)
    db.session.close()
    
#Set-ExecutionPolicy Unrestricted -Scope Process
#.\env\Scripts\activate