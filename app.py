import pandas as pd
from io import BytesIO
from flask import Flask, render_template_string, send_file

app = Flask(__name__)

def obter_dados_alunos():
    return [
        {"nome": "ALLAN ARAÚJO MARQUES DA CONCEIÇÃO", "faltas": 0, "media": 0.0, "d10": "P", "d11": "P"},
        {"nome": "ALLYCYA SANNY GONÇALVES MENESES", "faltas": 0, "media": 0.0, "d10": "P", "d11": "P"},
        {"nome": "ANA BEATRIZ DIAS SILVA", "faltas": 0, "media": 0.0, "d10": "P", "d11": "P"},
        {"nome": "ANA BEATRIZ SANTOS DA PENHA", "faltas": 0, "media": 0.0, "d10": "-", "d11": "-"},
        {"nome": "ANA CLARA SANTOS", "faltas": 0, "media": 0.0, "d10": "P", "d11": "P"}
    ]

HTML_PAGINA = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Diário Eletrônico de Classe</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body { background-color: #f8f9fa; }
        .navbar-custom { background-color: #1a365d; color: white; }
        .table-thead { background-color: #f7fafc; }
        .text-p { color: #2f855a; font-weight: bold; }
    </style>
</head>
<body>

<nav class="navbar navbar-custom p-3 mb-4">
    <div class="container-fluid">
        <span class="navbar-brand mb-0 h1 text-white">🍎 Diário Eletrônico de Classe</span>
    </div>
</nav>

<div class="container bg-white p-4 rounded shadow-sm">
    
    <div class="alert alert-success d-flex justify-content-between align-items-center mb-4 p-3" role="alert">
        <h5 class="m-0 text-success fw-bold">📊 PLANILHA CONSOLIDADA PRONTA</h5>
        <a href="/exportar-excel" class="btn btn-success btn-lg fw-bold px-4 shadow">
            📥 Baixar Planilha Excel
        </a>
    </div>

    <div class="table-responsive">
        <table class="table table-bordered align-middle">
            <thead class="table-thead">
                <tr>
                    <th>Turma / Nome do Aluno</th>
                    <th class="text-center">Faltas</th>
                    <th class="text-center">Média</th>
                    <th class="text-center">10/06</th>
                    <th class="text-center">11/06</th>
                </tr>
            </thead>
            <tbody>
                {% for aluno in alunos %}
                <tr>
                    <td>
                        <span class="badge bg-secondary" style="font-size: 10px;">turma</span><br>
                        <strong>{{ aluno.nome }}</strong>
                    </td>
                    <td class="text-center">{{ aluno.faltas }}</td>
                    <td class="text-center text-danger fw-bold">{{ aluno.media }}</td>
                    <td class="text-center text-p">{{ aluno.d10 }}</td>
                    <td class="text-center text-p">{{ aluno.d11 }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>

</body>
</html>
'''

@app.route('/')
def index():
    alunos = obter_dados_alunos()
    return render_template_string(HTML_PAGINA, alunos=alunos)

@app.route('/exportar-excel')
def exportar_excel():
    alunos = obter_dados_alunos()
    dados_planilha = []
    for aluno in alunos:
        dados_planilha.append({
            "Nome do Aluno": aluno["nome"],
            "Faltas": aluno["faltas"],
            "Média": aluno["media"],
            "10/06": aluno["d10"],
            "11/06": aluno["d11"]
        })
    
    df = pd.DataFrame(dados_planilha)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='CIEP_205')
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='Consolidado_Bimestre_CIEP_205.xlsx'
    )

if __name__ == '__main__':
    app.run(debug=True)
