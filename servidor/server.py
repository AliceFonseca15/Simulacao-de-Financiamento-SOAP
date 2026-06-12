import xml.etree.ElementTree as ET
import math
from flask import Flask, request, Response
from ConexaoDB import ConexaoDB 

app = Flask(__name__)
db = ConexaoDB()

db.inicializar_banco()

#http://localhost:8000/?wsdl
NS_SOAP = "http://schemas.xmlsoap.org/soap/envelope/"
NS_TNS = "concessionaria.soap"

def aplicar_taxa(ano):
    return 0.015 if ano >= 2020 else 0.023

def calcular_price(valor_total, entrada, parcelas, taxa_mensal):
    valor_financiar = valor_total - entrada
    if valor_financiar <= 0:
        return 0.0, 0.0
    
    valor_parcela = (valor_financiar * taxa_mensal) / (1 - math.pow(1 + taxa_mensal, -parcelas))
    total_pago = (valor_parcela * parcelas) + entrada
    return round(valor_parcela, 2), round(total_pago, 2)

def ler_wsdl():
    with open("servico.wsdl", "r", encoding="utf-8") as f:
        return f.read()
    
@app.route('/', methods=['GET', 'POST'])
def prover_wsdl():
    # 1. Tratamento do WSDL (GET com ?wsdl)
    if request.method == 'GET' and 'wsdl' in request.args:
        with open('servico.wsdl', 'r', encoding='utf-8') as f:
            return Response(f.read(), mimetype='text/xml')

    if request.method == 'POST':
        return processar_soap(request.data)

    return "Serviço SOAP está ativo. Use o parâmetro ?wsdl para ver o contrato ou envie um POST SOAP.", 200

@app.route("/debug_db", methods=["GET"])
def debug_db():
    db = ConexaoDB()
    veiculos = db.listar_veiculos() # Reutiliza sua função de listar
    return str(veiculos)

@app.route("/", methods=["POST"])
def processar_soap():
    xml_dados = request.data
    try:
        root = ET.fromstring(xml_dados)
        body = root.find(f".//{{{NS_SOAP}}}Body")
        metodo_nodo = body[0]
        nome_metodo = metodo_nodo.tag.split("}")[-1]

        if nome_metodo == "inserir_veiculo":
            tipo = metodo_nodo.find("tipo").text
            marca = metodo_nodo.find("marca").text
            modelo = metodo_nodo.find("modelo").text
            ano = int(metodo_nodo.find("ano").text)
            preco = float(metodo_nodo.find("preco").text)

            db = ConexaoDB()
            novo_id = db.inserir_veiculo(tipo, marca, modelo, ano, preco)
            print(f"DEBUG: Veículo inserido com ID: {novo_id}")

            resposta_xml = f"""<soapenv:Envelope xmlns:soapenv="{NS_SOAP}">
                <soapenv:Body>
                    <tns:inserir_veiculoResponse xmlns:tns="{NS_TNS}">
                        <inserir_veiculoResult>Veículo {marca} {modelo} cadastrado com sucesso!</inserir_veiculoResult>
                    </tns:inserir_veiculoResponse>
                </soapenv:Body>
            </soapenv:Envelope>"""
            
            return Response(resposta_xml, mimetype="text/xml")
        
        elif nome_metodo == "excluir_veiculo":
            veiculo_id = int(metodo_nodo.find("id").text)
            
            db = ConexaoDB()
            sucesso = db.excluir_veiculo(veiculo_id)
            
            resposta_xml = f"""<soapenv:Envelope xmlns:soapenv="{NS_SOAP}">
                <soapenv:Body>
                    <tns:excluir_veiculoResponse xmlns:tns="{NS_TNS}">
                        <result>{str(sucesso).lower()}</result>
                    </tns:excluir_veiculoResponse>
                </soapenv:Body>
            </soapenv:Envelope>"""
            return Response(resposta_xml, mimetype="text/xml")
        
        elif nome_metodo == "listar_veiculos":
            db = ConexaoDB()
            veiculos = db.listar_veiculos()
            elementos = ""
            for v in veiculos:
                elementos += f"<item><id>{v[0]}</id><tipo>{v[1]}</tipo><marca>{v[2]}</marca><modelo>{v[3]}</modelo><ano>{v[4]}</ano><preco>{v[5]}</preco></item>"
            
            resposta = f"""<soapenv:Envelope xmlns:soapenv="{NS_SOAP}">
                <soapenv:Body>
                    <tns:listar_veiculosResponse xmlns:tns="{NS_TNS}">
                        {elementos}
                    </tns:listar_veiculosResponse>
                </soapenv:Body>
            </soapenv:Envelope>"""
            return Response(resposta, mimetype="text/xml")

        elif nome_metodo == "simular_financiamento":
            veiculo_id = int(metodo_nodo.find("veiculo_id").text)
            valor_entrada = float(metodo_nodo.find("valor_entrada").text)
            parcelas = int(metodo_nodo.find("parcelas").text)
            
            db = ConexaoDB()
            carro = db.buscar_veiculo_por_id(veiculo_id) # Esperado: (id, tipo, marca, modelo, ano, preco)
            
            if not carro:
                return "Veículo não encontrado", 404
            
            modelo_veiculo = carro[3] 
            preco_veiculo = carro[5]
            
            taxa = aplicar_taxa(carro[4]) 
            v_parcela, total = calcular_price(preco_veiculo, valor_entrada, parcelas, taxa)
            
            resposta_xml = f"""<soapenv:Envelope xmlns:soapenv="{NS_SOAP}">
                <soapenv:Body>
                    <tns:simular_financiamentoResponse xmlns:tns="{NS_TNS}">
                        <modelo>{modelo_veiculo}</modelo>
                        <valor_parcela>{v_parcela:.2f}</valor_parcela>
                        <total_pago>{total:.2f}</total_pago>
                    </tns:simular_financiamentoResponse>
                </soapenv:Body>
            </soapenv:Envelope>"""
            return Response(resposta_xml, mimetype="text/xml")

        else:
            return "Método não implementado", 404

    except Exception as e:
        return f"Erro no processamento: {str(e)}", 500

if __name__ == "__main__":
    app.run(port=8000, debug=True)
    
