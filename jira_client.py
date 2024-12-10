"""
Modulo de interacao com o JIRA
"""
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from jira import JIRA


class JiraClient:
    def __init__(self, api_token, server_url, user_email):
        self.client = JIRA(
            server=server_url,
            basic_auth=(user_email, api_token)
        )

    def check_connectivity(self):
        """
        Verifica a conectividade com o servidor JIRA.

        :return: True se a conexão for bem-sucedida, False caso contrário.
        """
        try:
            # Realiza uma chamada simples para verificar a conexão.
            self.client.myself()
            return True
        except Exception as e:
            print(f"Erro de conectividade com o Jira: {e}")
            return False

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

    def check_progress_status(self, epic_id, label):
        """
        Informa semanalmente o status de progresso de um epic_id, 
        ou um label para pesquisa (que identifica o marco de entrega)

        :param epic_id: The epic ID to monitor (e.g., 'BURACO-4245')
        :param label: The label identifying the delivery milestone (e.g., 'Milestone_1')

        :return: A dictionary with total and completed issues, or an error message.

        """
        if not label or not epic_id:
            return {"error": "Label and epic_id are required parameters."}

        try:
            # Query for all issues matching the epic_id and label
            jql = f'parent = "{epic_id}" AND status not in (Cancelled, Aborted) AND labels = "{label}"'
            issues = self.client.search_issues(jql, maxResults=False)
            count_total = len(issues)

            # Query for completed issues
            jql_done = f'parent = "{epic_id}" AND status = Done AND labels = "{label}"'
            issues_done = self.client.search_issues(jql_done, maxResults=False)
            count_done = len(issues_done)

            # Build progress status
            progress_status = {"total_issues": count_total,
                               "done_issues": count_done}
        except Exception as e:
            return {"error": str(e), "total_issues": 0, "done_issues": 0}

        return progress_status
