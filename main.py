from domain.models.concrete_automation_metrics import ConcreteAutomationMetrics
from domain.usecases.automation_extract import AutomationExtract
from infraestructure.driven_adapters.gestor_elastic_search import ElasticSearchIntegration


def main():
    automation_metrics = ConcreteAutomationMetrics()
    automation_extract = AutomationExtract(automation_metrics)

    elastic_search = ElasticSearchIntegration(
        url_endpoint='https://emma-vault.apps.bancolombia.com/curiosity_indicadores_calidad_auto/_search',
        user='curiosity',
        password='User_elastic2020'
    )

    elastic_search.set_max_result_window(limit_index=10000)

    automation_extract.query_elasticsearch()


if __name__ == "__main__":
    main()
