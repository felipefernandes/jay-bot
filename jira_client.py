"""
Modulo de interacao com o JIRA
"""
from jira import JIRA


def get_jira_client(jira_token, jira_server, jira_user_email):
    """
    Configura e retorna um cliente JIRA.

    :param jira_token: Token de acesso para a API do JIRA.
    :param jira_server: URL do servidor JIRA.
    :return: Instância do cliente JIRA.
    """
    options = {'server': jira_server}
    jira_client = JIRA(options, basic_auth=(jira_user_email, jira_token))
    return jira_client


def check_wip_limit(jira_client, board_id, wip_limit, states):
    """
    Verifica se o limite de WIP foi excedido em um quadro do JIRA.

    :param jira_client: Cliente JIRA configurado.
    :param board_id: ID do quadro no JIRA.
    :param wip_limit: Limite de WIP para itens normais.
    :param expedite_limit: Limite de WIP para itens expedidos.
    :return: True se o limite de WIP foi excedido, False caso contrário.
    """

    states_query = "', '".join(states)
    jql_query = f"project = {board_id} AND status IN ('{states_query}')"
    issues = jira_client.search_issues(jql_query)

    # Verificar se o limite de WIP foi excedido
    return len(issues) > wip_limit
