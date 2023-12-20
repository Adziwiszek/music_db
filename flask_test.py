import json
from flask import Flask, request, jsonify
import db_operations
app = Flask(__name__)
db = None
@app.route("/")
def main():
    return "<p>Kurs programowania w Pythonie</p>"

@app.route("/wyklad12")
def wyklad():
    return "<p>Usługi sieciowe</p>"

@app.route('/bands/<int:id>', methods=['GET'])
def get_band(id):
    #print(f"given id: {id}")
    band_res = db.session.query(db_operations.Band).filter_by(id=id).first()
    print(band_res)
    if band_res:
        return jsonify({'id': band_res.id, 'name': band_res.name})
    else:
        return jsonify({'error_message': 'there is no such object'})
    
@app.route('/<string:table_name>', methods=['GET'])
def get_table(table_name):
    #print(f"given table name: {table_name}")
    json_res = db.display_table(table_name=table_name)
    return json_res
    

@app.route('/osoba/', methods=['PUT'])
def new_osoba(ide):
    print(f"nowa osoba {ide}")
    return jsonify({'msg': ide})

if __name__ == "__main__":
    db = db_operations.Database()
    app.run(debug=True)
    db.session.close()
    
#Set-ExecutionPolicy Unrestricted -Scope Process
#.\env\Scripts\activate