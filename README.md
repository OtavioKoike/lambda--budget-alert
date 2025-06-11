# lambda--budget-alert

Afim de não ter problemas de cobranças elevadas na AWS, esse projeto contém todo um ecossistema responsavel por monitorar o Budget da conta AWS e intervir nos serviços com gastos elevados, podendo desligar, diminuir, migrar ou tomar alguma outra ação que busque diminuir o valor previsto.

<div align="center">
  <img src="docs\fluxograma.png" alt="Fluxograma"/>
</div>

Com esse projeto, 90% da estrutura será criado diretamente na conta e funcional desde o primeiro deploy. Os passos manuais serão descritos no tópico de <b>Açoes Manuais</b>.

## Arquitetura

Este projeto contém código-fonte e arquivos de suporte para um aplicativo sem servidor que você pode implantar com a CLI do SAM. Inclui os seguintes arquivos e pastas.

- docs - Documentos do Projeto
- src - Implementação do código responsavel pelo monitoramento e desligamento de serviços.
- testes - Testes unitários para o código da aplicação. 
- app.py - Classe inicial do projeto
- requirements.txt - Dependencias de bibliotecas
- template.yaml – Um modelo que define os recursos AWS do aplicativo.

O aplicativo usa vários recursos da AWS, incluindo funções Lambda e SNS. Esses recursos são definidos no arquivo `template.yaml` deste projeto. Você pode atualizar o modelo para adicionar recursos da AWS por meio do mesmo processo de implantação que atualiza o código do seu aplicativo.

## Pré Requisito

Antes de iniciarmos o Deploy, é necessario ter configurado as credenciais da AWS, elas serão utilizadas no permissionamento do SAM. Para isso, o ideal é ter um diretorio .aws com as chaves de credenciais.

## Deploy

Para usar a CLI da SAM, você precisa das seguintes ferramentas.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)

Para compilar e implantar seu aplicativo pela primeira vez, execute o seguinte no shell:

```bash
sam init
sam build
sam deploy --guided --capabilities CAPABILITY_NAMED_IAM --profile deployment
```

O primeiro comando iniciará o SAM local com algumas configurações iniciais. <br>O segundo comando criará o código-fonte do seu aplicativo. <br>O terceiro comando empacotará e implantará seu aplicativo na AWS, com uma série de prompts:

* **Nome da Pilha**: O nome da pilha a ser implantada no CloudFormation. Ele deve ser exclusivo para sua conta e região, e um bom ponto de partida seria algo que corresponda ao nome do seu projeto.
* **Região da AWS**: A região da AWS na qual você deseja implantar seu aplicativo.
* **Confirmar alterações antes da implantação**: Se definido como sim, quaisquer conjuntos de alterações serão exibidos antes da execução para revisão manual. Se definido como não, a CLI do AWS SAM implantará automaticamente as alterações no aplicativo.
* **Permitir criação de função IAM da CLI do SAM**: Muitos modelos do AWS SAM, incluindo este exemplo, criam funções IAM da AWS necessárias para que as funções do AWS Lambda incluídas acessem os serviços da AWS. Por padrão, elas são limitadas às permissões mínimas necessárias. Para implantar uma pilha do AWS CloudFormation que cria ou modifica funções IAM, o valor `CAPABILITY_IAM` para `capabilities` deve ser fornecido. Se a permissão não for fornecida por meio deste prompt, para implantar este exemplo, você deverá passar explicitamente `--capabilities CAPABILITY_IAM` para o comando `sam deploy`.
* **Salvar argumentos em samconfig.toml**: Se definido como sim, suas escolhas serão salvas em um arquivo de configuração dentro do projeto, para que, no futuro, você possa executar `sam deploy` novamente sem parâmetros para implantar as alterações em seu aplicativo.

Para fazer o deploy do seu pacote, execute o seguinte no shell:

```bash
Compress-Archive -Path app.py, requirements.txt, __init__.py -DestinationPath lambda_budget_alert.zip
aws s3 cp lambda_budget_alert.zip s3://<SEU_BUCKET>/lambda_budget_alert.zip
```

## Delete

Para excluir o aplicativo de exemplo que você criou, use a CLI da AWS. Supondo que você tenha usado o nome do seu projeto como nome da pilha, você pode executar o seguinte:

```bash
sam delete --stack-name "lambda--budget-alert"
```
