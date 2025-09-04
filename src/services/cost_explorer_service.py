import boto3
import datetime


class CostExplorerService:
    """Serviço para consultar dados de custo da AWS usando o Cost Explorer."""
    """US$ 0,01 por solicitação de API do Cost Explorer."""
    
    def __init__(self, client=None):
        self.client = client or boto3.client("ce")

    def consultar_gasto_total_mensal(self):
        """Consulta o custo total mensal até a data atual."""
        hoje = datetime.date.today()
        inicio_mes = hoje.replace(day=1)

        resposta = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': inicio_mes.strftime('%Y-%m-%d'),
                'End': hoje.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost']
        )

        valor = resposta['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
        return float(valor)

    def consultar_por_servico(self):
        """Consulta gastos detalhados por serviço AWS."""
        hoje = datetime.date.today()
        inicio_mes = hoje.replace(day=1)

        resposta = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': inicio_mes.strftime('%Y-%m-%d'),
                'End': hoje.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
        )

        servicos = resposta['ResultsByTime'][0].get('Groups', [])
        return [
            {
                "servico": grupo['Keys'][0],
                "valor": float(grupo['Metrics']['UnblendedCost']['Amount'])
            }
            for grupo in servicos
        ]

    def consultar_por_tag(self, tag_key: str):
        """
        Consulta os custos agrupados pela tag informada (ex: 'Project', 'CostCenter').
        A tag precisa estar habilitada como tag de alocação de custo na conta AWS.
        """
        hoje = datetime.date.today()
        inicio_mes = hoje.replace(day=1)

        resposta = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': inicio_mes.strftime('%Y-%m-%d'),
                'End': hoje.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {
                    'Type': 'TAG',
                    'Key': tag_key
                }
            ]
        )

        grupos = resposta['ResultsByTime'][0].get('Groups', [])
        return [
            {
                "tag": grupo['Keys'][0] if grupo['Keys'] else "Sem valor",
                "valor": float(grupo['Metrics']['UnblendedCost']['Amount'])
            }
            for grupo in grupos
        ]

    def listar_dimensoes_servicos(self):
        """
        Retorna a lista de todos os serviços AWS reconhecidos pela dimensão 'SERVICE'.
        Ideal para uso como sugestão de filtros ou construção dinâmica de relatórios.
        """
        resposta = self.client.get_dimension_values(
            TimePeriod={
                'Start': '2025-01-01',  # início genérico; não influencia os resultados
                'End': datetime.date.today().strftime('%Y-%m-%d')
            },
            Dimension='SERVICE',
            Context='COST_AND_USAGE'
        )

        valores = resposta.get('DimensionValues', [])
        return [item['Value'] for item in valores]