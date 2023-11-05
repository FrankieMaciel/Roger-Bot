from Project.models.chatbot import chatbot

from flask import Flask, request, jsonify
import os

app = Flask(__name__)

dataset = os.path.join('Project', 'data', 'database.txt')
roger = chatbot('Roger', dataset)

@app.route('/roger', methods=['POST'])
def callRoger():
  try:
      dados = request.get_json()

      if dados is not None:
          texto = dados.get("text", "")
      else:
          return "Requisição inválida. Certifique-se de que a requisição está no formato JSON.", 400

      response = roger.run(texto)

      return jsonify({"response": response})
  except Exception as e:
      return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)