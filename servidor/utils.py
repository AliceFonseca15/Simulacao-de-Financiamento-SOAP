import math

class Financiamento:
    @staticmethod
    def aplicar_taxa(ano, valor_total, entrada):

        percentual_entrada = entrada / valor_total if valor_total > 0 else 0
        
        taxa = 0.015 if ano >= 2020 else 0.023        
        
        if percentual_entrada == 0:
            taxa += 0.025  
        elif percentual_entrada < 0.20:
            taxa += 0.010  
            
        return taxa

    @staticmethod
    def calcular_price(valor_total, entrada, parcelas, taxa_mensal):
        valor_financiar = valor_total - entrada
        if valor_financiar <= 0:
            return 0.0, 0.0
        
        valor_parcela = (valor_financiar * taxa_mensal) / (1 - math.pow(1 + taxa_mensal, -parcelas))
        total_pago = (valor_parcela * parcelas) + entrada
        return round(valor_parcela, 2), round(total_pago, 2)