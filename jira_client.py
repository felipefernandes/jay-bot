"""
Modulo de interacao com o JIRA
"""
from jira import JIRA


class JiraClient:
    def __init__(self, api_token, server_url, user_email):
        self.client = JIRA(
            server=server_url,
            basic_auth=(user_email, api_token)
        )

    def check_wip_limit(self, board_id, wip_limit, states):
        """
        Verifica se o limite de WIP foi atingido para o board e estados especificados.

        :param board_id: ID do board no JIRA.
        :param wip_limit: Limite de WIP.
        :param states: Lista de estados a serem verificados.
        :return: True se o limite de WIP for atingido, False caso contrário.
        """
        jql = f'board = {board_id} AND status in ({",".join(states)})'
        issues = self.client.search_issues(jql)
        return len(issues) > wip_limit