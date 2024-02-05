from domain.models.automation_metrics import AutomationMetrics
from typing import List, Dict

class ConcreteAutomationMetrics(AutomationMetrics):
    def get_data_source_domain(self, url_get_data, token, limit, sources) -> List[Dict]:
      "get data source."

    def get_info_index_with_payload(self, payload_input):
       "get info index with payload"
