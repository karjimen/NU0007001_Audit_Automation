import requests
import pandas as pd
from domain.utils.constants import Constants
from infraestructure.driven_adapters.automation_metrics_implementation import ElasticSearchAutomationMetrics
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Desactiva las advertencias de urllib3 relacionadas con la verificación del certificado SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def main():
    # Tu carga útil para get_data_by_query
    payload = {
        "size": 10000,
        "query": {
            "term": {
                "Sprint.keyword": "Sprint 183"
            }
        }
    }

    # Crea una instancia de ElasticSearchAutomationMetrics
    es_automation_metrics = ElasticSearchAutomationMetrics(
        Constants.url_elasticsearch_automation_metrics,
        Constants.Username,
        Constants.Password
    )

    try:
        # Crea una sesión de requests y desactiva la verificación del certificado SSL
        session = requests.Session()
        session.auth = (Constants.Username, Constants.Password)
        session.verify = False  # Desactiva la verificación del certificado SSL

        # Llama a get_data_by_query
        response = session.get(Constants.url_elasticsearch_automation_metrics, json=payload)

        # Procesa la respuesta según sea necesario
        print(f"Código de estado de la respuesta: {response.status_code}")

        if response.status_code == 200:
            # Convierte el JSON a un DataFrame de pandas
            data = response.json()
            print(f"Datos de la respuesta: {data}")
            df = pd.json_normalize(data['hits']['hits'])

            # Especifica la ruta donde deseas guardar el archivo Excel
            ruta_guardado = r'C:\Users\karjimen\Documents\Curiosity\Auditorias\Repositorios\Automatizacion_Auditorias\NU007001_Audit_Automation\datos.xlsx'

            # Exporta el DataFrame a un archivo Excel
            df.to_excel(ruta_guardado, index=False)
            print(f"Datos exportados a {ruta_guardado} exitosamente.")
        else:
            print(f"Fallo al obtener datos. Código de estado: {response.status_code}")
            print(f"Respuesta de la API: {response.text}")

    except Exception as e:
        print(f"Error al obtener datos: {e}")


if __name__ == "__main__":
    main()
