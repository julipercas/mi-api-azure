from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify(ok=True, description="Probando el CI de Github y Azure :D", status_code=200)

if __name__ == '__main__':
    app.run()