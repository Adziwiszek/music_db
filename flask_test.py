import json
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/")
def main():
    return "<p>Kurs programowania w Pythonie</p>"

@app.route("/wyklad12")
def wyklad():
    return "<p>Usługi sieciowe</p>"

@app.route('/osoba/<int:ide>', methods=['GET'])
def get_osoba(ide):
    print(ide)
    return jsonify({'imie': 'Maksymilian', 'nazwisko': 'Debeściak'})

@app.route('/osoba/', methods=['PUT'])
def new_osoba(ide):
    print(f"nowa osoba {ide}")
    return jsonify({'msg': ide})

if __name__ == "__main__":
    app.run(debug=True)