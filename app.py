import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Extrai a mensagem SNS
        sns_message = event['Records'][0]['Sns']['Message']
        logger.info(f"Mensagem SNS recebida: {sns_message}")

        # Converte string JSON em dicionário
        alerta = json.loads(sns_message)
        
        # Extrai dados principais
        nome_orcamento = alerta.get("budgetName", "Desconhecido")
        tipo_alerta = alerta.get("alertType")
        threshold = alerta.get("alertThreshold")
        estado = alerta.get("alertState")
        periodo_inicio = alerta.get("timePeriodStart")
        periodo_fim = alerta.get("timePeriodEnd")

        logger.info(f"🧾 Alerta do orçamento: {nome_orcamento}")
        logger.info(f"Tipo: {tipo_alerta} | Threshold: {threshold}% | Estado: {estado}")
        logger.info(f"Período: {periodo_inicio} até {periodo_fim}")
        
        # Trata alertas reais ou previstos
        if tipo_alerta == "ACTUAL":
            gasto_real = alerta.get("actualSpend", {}).get("amount", "0")
            logger.warning(f"⚠️ Gasto REAL atingiu: U${gasto_real}")
            # Aqui você pode automatizar ações como desligar recursos, se necessário

        elif tipo_alerta == "FORECASTED":
            gasto_previsto = alerta.get("forecastedSpend", {}).get("amount", "0")
            logger.warning(f"🔮 Gasto PREVISTO excederá: U${gasto_previsto}")
            # Aqui também dá para antecipar ações preventivas

        else:
            logger.error("Tipo de alerta desconhecido. Nenhuma ação tomada.")

        return {
            'statusCode': 200,
            'body': json.dumps('Processamento concluído com sucesso!')
        }

    except Exception as e:
        logger.exception("Erro durante o processamento do alerta.")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro: {str(e)}')
        }
