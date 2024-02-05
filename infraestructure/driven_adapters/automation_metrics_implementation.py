import pandas as pd

from domain.models.automation_metrics import AutomationMetrics
from infraestructure.driven_adapters.gestor_elastic_search import ElasticSearchIntegration


class ElasticSearchAutomationMetrics(AutomationMetrics):

    def update_index_by_query(self, url_get_data, user, password, payload):
        conection = ElasticSearchIntegration(
            url_get_data,
            user,
            password,
        )

        return conection.update_index_by_query(payload)