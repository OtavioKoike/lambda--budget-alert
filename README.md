# lambda--budget-alert

Afim de não ter problemas de cobranças elevadas na AWS, esse projeto contém todo um ecossistema responsavel por monitorar o Budget da conta AWS e intervir nos serviços com gastos elevados, podendo desligar, diminuir, migrar ou tomar alguma outra ação que busque diminuir o valor previsto.

<div align="center">
  <img src="docs\images\fluxograma.png" alt="Fluxograma"/>
</div>

Com esse projeto, 90% da estrutura será criado diretamente na conta e funcional desde o primeiro deploy atraves do SAM. Os passos manuais serão descritos no tópico de <b>Ações Manuais</b>.

## Arquitetura

Este projeto contém código-fonte e arquivos de suporte para uma aplicação sem servidor que você pode implantar com a CLI do SAM. Inclui os seguintes arquivos e pastas.

- docs - Documentos do Projeto
- src - Implementação do código responsavel pelo monitoramento e desligamento de serviços.
- testes - Testes unitários para o código da aplicação. 
- app.py - Classe inicial do projeto
- requirements.txt - Dependencias de bibliotecas
- template.yaml – Um modelo que define os recursos AWS da aplicação.

A aplicação usa vários recursos da AWS, incluindo funções Lambda e SNS. Esses recursos são definidos no arquivo `template.yaml` deste projeto. Você pode atualizar o modelo para adicionar recursos da AWS por meio do mesmo processo de implantação que atualiza o código do seu aplicativo.

## Pré Requisito

Antes de iniciarmos o Deploy, é necessario ter configurado as credenciais da AWS, elas serão utilizadas no permissionamento do SAM. Para isso, o ideal é ter um diretorio .aws com as chaves de credenciais.

Para usar a CLI da SAM, você precisa das seguintes ferramentas.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)

## Deploy

Para fazer o deploy do seu pacote, na raiz do projeto, execute o seguinte no shell:

```bash
Remove-Item 'lambda_budget_alert.zip'
Compress-Archive -Path app.py, src/, requirements.txt, __init__.py -DestinationPath lambda_budget_alert.zip

aws s3 cp lambda_budget_alert.zip s3://<SUA_CONTA>--serverless-deployments/lambda_budget_alert.zip --profile deployment
aws lambda update-function-code --function-name lambda--budget-alert --s3-bucket <SUA_CONTA>--serverless-deployments --s3-key lambda_budget_alert.zip --profile deployment
```

Com os comandos acima, voce criará o pacote zip dos componentes da sua aplicação e copiará para o bucket <SUA_CONTA>--serverless-deployments, o qual será apontado durante o deploy.

Obs.: O profile deve ser de acordo com suas credenciais, caso seja default, não é necessario informar

Para compilar e implantar sua aplicação pela primeira vez, execute o seguinte no shell:

```bash
sam init
sam build
sam deploy --guided --capabilities CAPABILITY_NAMED_IAM
```

O primeiro comando iniciará o SAM local com algumas configurações iniciais. <br>O segundo comando criará o código-fonte do seu aplicativo. <br>O terceiro comando empacotará e implantará sua aplicação na AWS, com uma série de prompts:

* **Nome da Pilha**: O nome da pilha a ser implantada no CloudFormation. Ele deve ser exclusivo para sua conta e região, e um bom ponto de partida seria algo que corresponda ao nome do seu projeto.
* **Região da AWS**: A região da AWS na qual você deseja implantar seu aplicativo.
* **Confirmar alterações antes da implantação**: Se definido como sim, quaisquer conjuntos de alterações serão exibidos antes da execução para revisão manual. Se definido como não, a CLI do AWS SAM implantará automaticamente as alterações no aplicativo.
* **Permitir criação de função IAM da CLI do SAM**: Muitos modelos do AWS SAM, incluindo este exemplo, criam funções IAM da AWS necessárias para que as funções do AWS Lambda incluídas acessem os serviços da AWS. Por padrão, elas são limitadas às permissões mínimas necessárias. Para implantar uma pilha do AWS CloudFormation que cria ou modifica funções IAM, o valor `CAPABILITY_IAM` para `capabilities` deve ser fornecido. Se a permissão não for fornecida por meio deste prompt, para implantar este exemplo, você deverá passar explicitamente `--capabilities CAPABILITY_IAM` para o comando `sam deploy`.
* **Salvar argumentos em samconfig.toml**: Se definido como sim, suas escolhas serão salvas em um arquivo de configuração dentro do projeto, para que, no futuro, você possa executar `sam deploy` novamente sem parâmetros para implantar as alterações em seu aplicativo.

<div align="center">
  <img src="docs\images\success.png" alt="Sucesso"/>
</div>

## Ações Manuais

Após a criação do ecossistema, vá até o serviço do AWS Budget. Nele é preciso configurar os alertas necessários de acordo com suas prioridades e configurar para enviar uma notificação ao SNS 'topic-bugdet-alert' já criado pelo deploy.

## Delete

Para excluir a aplicação e as dependencias, use a CLI da AWS. Supondo que você tenha usado o nome do seu projeto como nome da pilha, você pode executar o seguinte:

```bash
sam delete --stack-name "lambda--budget-alert"
```

## Documentações
Segue documentações da AWS que podem agregar junto do projeto:
* [Gerenciando seus custos com AWS orçamentos](https://docs.aws.amazon.com/pt_br/cost-management/latest/userguide/budgets-managing-costs.html)
