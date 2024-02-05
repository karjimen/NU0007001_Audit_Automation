import hashlib
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from domain.models.automation_metrics import AutomationMetrics
from domain.utils.constants import Constants



def calculator_hash(cadena):
    hasher = hashlib.sha256()
    cadena_bytes = cadena.encode('utf-8')
    hasher.update(cadena_bytes)
    hash_resultant = hasher.hexdigest()
    return hash_resultant


class AutomationExtract:
    def __init__(self, data_source_automation_metrics: AutomationMetrics):
        self.data_source_automation_metrics = data_source_automation_metrics
        self.executions_count = 0

    def query_elasticsearch(self):
        es = Elasticsearch("https://emma-vault.apps.bancolombia.com/curiosity_indicadores_calidad_auto/_search")

        query = {
            {
                "size": 10000,
                "query": {
                    "match": {
                        "Sprint": "Sprint 183"
                    }
                }
            }
        }

        result = es.search(index="_search", body=query)
        print(result)

