JAY - O Bot de Slack para Agile Teams
=====================================

Sobre o JAY
-----------

JAY (antigo AgileBOT) é um bot de Slack inteligente e interativo, projetado para auxiliar equipes ágeis em suas rotinas diárias. Com uma série de funcionalidades focadas em eficiência e produtividade, JAY se integra perfeitamente ao seu ambiente de trabalho, oferecendo suporte na gestão de tarefas e na comunicação da equipe.

Funcionalidades
---------------

-   Monitoramento de WIP (Work In Progress): JAY monitora automaticamente os limites de WIP em quadros do JIRA, enviando alertas personalizados e bem-humorados no Slack quando estes limites são excedidos.
-   Configuração Flexível: Cada equipe pode configurar seus próprios limites de WIP e canais de Slack correspondentes.
-   Integração com JIRA: JAY se conecta ao JIRA para obter informações em tempo real sobre o status das tarefas e projetos.
-   Respostas Divertidas e Engajadoras: Quando um limite de WIP é excedido, JAY envia mensagens variadas, mantendo o ambiente leve e motivador.
-   *(NEW)* Método para notificação no slack sobre atualizações de arquivos

Como Configurar
---------------

1.  Clone o Repositório:

    bashCopy code

    `git clone https://github.com/felipefernandes/agilebot.git`

2.  Configuração de Tokens:

    -   Configure os tokens de acesso do Slack e JIRA no arquivo `config.py`.

3.  Configuração das Equipes:

    -   Edite o arquivo `teams_config.json` para definir os limites de WIP, canais do Slack e outras configurações específicas de cada equipe.

4.  Instale dependencias:

    -   Execute o comando `pip install -r requirements.txt`

4.  Execução:

    -   Execute o bot com `python main.py`.

Publique seu BOT
----------------

Você vai precisar publicá-lo para ter acesso a URL que irá ser usada para a conexão com o JIRA via Webhook.

Algumas opções:
* [Vercel](https://vercel.com)
* [Squarecloud](squarecloud.app)
* [Heroku](https://www.heroku.com)
* [Amazon AWS](https://aws.amazon.com/pt/free)


Interação com o JIRA
--------------------

A interação com o JIRA é feita a partir do recurso de AUTOMATION (automatização de tarefas). Depois de publicado, crie uma automação dessa forma: 

1. When: `Quando uma issue for movida para {SELECIONE AS ETAPAS DE FLUXO QUE ESTÃO DEPOIS DO PONTO DE COMPROMISSO E ANTES DO DONE}`
2. Then: `Enviar um WEB REQUEST {web request URL é onde você publicou seu BOT, e o HTTP Method é POST}`


Contribuindo para o JAY
-----------------------

Contribuições são sempre bem-vindas! Se você tem ideias para melhorar o JAY ou quer adicionar novas funcionalidades, sinta-se à vontade para criar um fork do repositório e enviar suas Pull Requests. Antes de contribuir, por favor, leia o guia de contribuição.

Licença
-------

JAY é distribuído sob a licença [Apache License](http://www.apache.org/licenses/), permitindo que seja livremente utilizado e modificado.

Contato
-------

Para dúvidas, sugestões ou suporte, entre em contato através de [felipfernandesweb@gmail.com](felipfernandesweb@gmail.com).

Gostou do projeto? 
-----------------
Me pague um café. PIX: `felipfernandesweb@gmail.com`