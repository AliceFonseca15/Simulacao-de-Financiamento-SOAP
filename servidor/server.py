import xml.etree.ElementTree as ET
import math
from flask import Flask, request, Response
from ConexaoDB import ConexaoDB 
from utils import Financiamento

app = Flask(__name__)
db = ConexaoDB()

db.inicializar_banco()

#http://localhost:8000/?wsdl
NS_SOAP = "http://schemas.xmlsoap.org/soap/envelope/"
NS_TNS = "concessionaria.soap"


@app.route('/', methods=['GET', 'POST'])
def prover_wsdl():
    if request.method == 'GET' and 'wsdl' in request.args:
        with open('servico.wsdl', 'r', encoding='utf-8') as f:
            return Response(f.read(), mimetype='text/xml')

    if request.method == 'POST':
        return processar_soap(request.data)

    return "Serviço SOAP está ativo. Use o parâmetro ?wsdl para ver o contrato ou envie um POST SOAP.", 200

def buscar_veiculo_formatado(db, veiculo_id):
    veiculo_raw = db.get_veiculo_por_id(veiculo_id) 
    
    if not veiculo_raw:
        return None
        
    return {
        "id": veiculo_raw[0],
        "tipo": veiculo_raw[1],
        "marca": veiculo_raw[2],
        "modelo": veiculo_raw[3],
        "ano": veiculo_raw[4],
        "preco": veiculo_raw[5]
    }

def processar_soap(xml_data):
    xml_string = xml_data.decode("utf-8")
    
    print("Recebido XML:", xml_string)
    try:
        root = ET.fromstring(xml_string)
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
                    <inserir_veiculoResponse xmlns="{NS_TNS}">
                        <inserir_veiculoResult>Veículo {marca} {modelo} cadastrado com sucesso!</inserir_veiculoResult>
                    </inserir_veiculoResponse>
                </soapenv:Body>
            </soapenv:Envelope>"""
            
            return Response(resposta_xml, mimetype="text/xml")
        
        elif nome_metodo == "excluir_veiculo":
            veiculo_id = int(metodo_nodo.find("id").text)
            
            db = ConexaoDB()
            sucesso = db.excluir_veiculo(veiculo_id)
            
            resposta_xml = f"""<soapenv:Envelope xmlns:soapenv="{NS_SOAP}">
                <soapenv:Body>
                    <excluir_veiculoResponse xmlns="{NS_TNS}">
                        <result>{str(sucesso).lower()}</result>
                    </excluir_veiculoResponse>
                </soapenv:Body>
            </soapenv:Envelope>"""
            return Response(resposta_xml, mimetype="text/xml")
        
        elif nome_metodo == "listar_veiculos":
            db = ConexaoDB()
            veiculos = db.listar_veiculos()
            elementos = ""
            for v in veiculos:
                elementos += f"<item><id>{v['id']}</id><tipo>{v['tipo']}</tipo><marca>{v['marca']}</marca><modelo>{v['modelo']}</modelo><ano>{v['ano']}</ano><preco>{v['preco']}</preco></item>"
            
            resposta = f"""<soapenv:Envelope xmlns:soapenv="{NS_SOAP}">
                <soapenv:Body>
                    <listar_veiculosResponse>
                        <result>{elementos}</result>
                    </listar_veiculosResponse>
                </soapenv:Body>
            </soapenv:Envelope>"""
            
            return Response(resposta, mimetype="text/xml")

        elif nome_metodo == "simular_financiamento":
            veiculo_id = int(metodo_nodo.find("veiculo_id").text)
            valor_entrada = float(metodo_nodo.find("valor_entrada").text)
            parcelas = int(metodo_nodo.find("parcelas").text)
            
            db = ConexaoDB()
            carro = db.buscar_veiculo_por_id(veiculo_id) 
            
            if not carro:
                return "Veículo não encontrado", 404
            
            preco_veiculo = carro[5]
            ano_veiculo = carro[4]
            
            taxa = Financiamento.aplicar_taxa(ano_veiculo, preco_veiculo, valor_entrada)
            
            v_parcela, total_parcelas = Financiamento.calcular_price(preco_veiculo, valor_entrada, parcelas, taxa)
            
            total_final = round(total_parcelas + valor_entrada, 2)
            
            resposta = f"""<soapenv:Envelope xmlns:soapenv="{NS_SOAP}">
                <soapenv:Body>
                    <tns:simular_financiamentoResponse xmlns:tns="{NS_TNS}">
                        <valor_parcela>{v_parcela}</valor_parcela>
                        <total_apenas_parcelas>{round(total_parcelas, 2)}</total_apenas_parcelas>
                        <total_final>{total_final}</total_final>
                        <num_parcelas>{parcelas}</num_parcelas>
                    </tns:simular_financiamentoResponse>
                </soapenv:Body>
            </soapenv:Envelope>"""
            return Response(resposta, mimetype="text/xml")

    except Exception as e:
        return f"Erro no processamento: {str(e)}", 500

if __name__ == "__main__":
    app.run(port=8000, debug=True)
    
