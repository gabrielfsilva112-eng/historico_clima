from dotenv import load_dotenv
from flask import Flask, request, render_template
from datetime import datetime

from weather_service import buscar_clima_por_cidade
from database import criar_tabela, ja_existe_registro, insert_clima

load_dotenv()

app = Flask(__name__)

# Cria a tabela ao iniciar
criar_tabela()

def salvar_historico(cidade, weather):
    hoje = datetime.now().strftime('%Y-%m-%d')
    cidade_lower = cidade.strip().lower()

    if ja_existe_registro(cidade_lower, hoje):
        return  # Já existe, não salva

    previsao_hoje = weather.get('previsao', [{}])[0]

    insert_clima(
        cidade       = cidade_lower,
        data         = hoje,
        umidade      = weather.get('umidade'),
        vento        = weather.get('vento'),
        precipitacao = weather.get('precipitacao'),
        temp_min     = previsao_hoje.get('temperatura_min'),
        temp_max     = previsao_hoje.get('temperatura_max')
    )

@app.route('/', methods=['GET'])
def home():
    cidade = request.args.get('cidade')
    weather = None
    error = None

    if cidade:
        result = buscar_clima_por_cidade(cidade)
        if result['error']:
            error = result['message']
        else:
            weather = result['data']
            salvar_historico(cidade, weather)

    return render_template('index.html', weather=weather, error=error, cidade=cidade)

if __name__ == '__main__':
    app.run(debug=True)