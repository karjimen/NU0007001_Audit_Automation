import requests
import pandas as pd
from openpyxl.packaging import workbook
from openpyxl.styles import PatternFill
from openpyxl.workbook import Workbook
import openpyxl.utils

from domain.utils.constants import Constants
from infraestructure.driven_adapters.automation_metrics_implementation import ElasticSearchAutomationMetrics
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def extract_data():
    payload = {
        "size": 10000,
        "query": {
            "term": {
                "Sprint.keyword": "Sprint 184"
            }
        }
    }

    es_automation_metrics = ElasticSearchAutomationMetrics(
        Constants.url_elasticsearch_automation_metrics,
        Constants.Username,
        Constants.Password
    )

    try:
        session = requests.Session()
        session.auth = (Constants.Username, Constants.Password)
        session.verify = False

        response = session.get(Constants.url_elasticsearch_automation_metrics, json=payload)
        print(f"Código de estado de la respuesta: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            df = pd.json_normalize(data['hits']['hits'])
            df.rename(columns={'_source.Sprint': 'Sprint',
                               '_source.state': 'Estado',
                               '_source.dod': 'DOD',
                               '_source.name_pipeline_pdn': 'Pipeline PDN',
                               '_source.herramienta_despliegue': 'Herramienta Despliegue',
                               '_source.evidence_item': 'Id Evidencias VSTS',
                               '_source.name_pipeline_release_QA': 'Pipeline_Release',
                               '_source.id_test_plan': 'Testplan',
                               '_source.stage_E2E': 'Stage E2E',
                               '_source.stage_manual': 'Stage Manual Test',
                               '_source.stage_exploratory': 'Stage Exploratory Test',
                               '_source.existe_matriz': 'Herramienta matriz de riesgos',
                               '_source.existe_evidence': 'Evidencias',
                               '_source.check_list_perf': 'Checklist Performance',
                               '_source.check_list_sec': 'Checklist Seguridad',
                               '_source.analista': 'Responsable',
                               '_source.titulo_test_plan': 'Titulo Testplan',
                               '_source.exite_tag': 'TAG',
                               '_source.alcance_estrategia': 'Alcance/Estrategia',
                               '_source.fabrica': 'Fabrica',
                               '_source.componente_menor': 'Componente Menor',
                               '_source.lider_componente': 'Lider Inmediato'
                               }, inplace=True)
            df = df[['Sprint','Herramienta Despliegue','Estado','DOD','Pipeline PDN','Pipeline_Release','Id Evidencias VSTS',
                     'Testplan','Checklist Performance','Checklist Seguridad','Titulo Testplan','TAG','Alcance/Estrategia',
                     'Herramienta matriz de riesgos','Evidencias','Stage E2E','Stage Manual Test','Stage Exploratory Test',
                     'Responsable','Lider Inmediato','Fabrica','Componente Menor']]

            ruta_data = Constants.ruta_data
            df.to_excel(ruta_data, index=False)
            # Aqui abrimos el excel y trabajamos con el.
            workbook = Workbook()
            sheet = workbook.active
            workbook = pd.ExcelWriter(ruta_data, engine='openpyxl')
            workbook.book = workbook.book
            df.to_excel(workbook, index=False, sheet_name='Sheet1')
            sheet = workbook.sheets['Sheet1']

            columns_to_color = []

            for index, row in df.iterrows():
                checklist_performance_value = row['Checklist Performance']
                checklist_segue_value = row['Checklist Seguridad']
                archivo_evidence_value = row['Evidencias']
                title_testplan_value = row['Titulo Testplan']
                tag_value = row['TAG']
                strategy_value = row['Alcance/Estrategia']
                risk_matrix_value = row['Herramienta matriz de riesgos']

                columns_to_color.extend(
                    [(index + 1, 'I','A')] if checklist_performance_value == 'Error resultado checklist performance' else [])
                columns_to_color.extend(
                    [(index + 1, 'J', 'A')] if checklist_segue_value == 'Error resultado checklist seguridad' else [])
                columns_to_color.extend(
                    [(index + 1, 'K', 'A')] if title_testplan_value == 'Titulo no valido' else [])
                columns_to_color.extend(
                    [(index + 1, 'L', 'A')] if tag_value == 'Tag no Valido o Estandar Invalido' else [])
                columns_to_color.extend(
                    [(index + 1, 'M', 'A')] if strategy_value == 'No hay estrategia' else [])
                columns_to_color.extend(
                    [(index + 1, 'N', 'A')] if risk_matrix_value == 'No existe archivo Matriz de riesgos' else [])
                columns_to_color.extend(
                    [(index + 1, 'O', 'A')] if archivo_evidence_value == 'No existe archivo Evidencias' else [])

            error_count = 1

            # Pintar las celdas
            for row_index, column, column_a in columns_to_color:
                cell = sheet[column][row_index]
                cell_a = sheet[column_a][row_index]

                if sheet[column][row_index].value:
                    sheet['A'][row_index].value = 'ERROR ' + str(error_count)
                    error_count += 1

                cell.fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
                cell_a.fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            workbook.save()
            print(f"Datos exportados a {ruta_data} exitosamente.")
        else:
            print(f"Fallo al obtener datos. Código de estado: {response.status_code}")
            print(f"Respuesta de la API: {response.text}")

    except Exception as e:
        print(f"Error al obtener datos: {e}")

if __name__ == "__main__":
    extract_data()



