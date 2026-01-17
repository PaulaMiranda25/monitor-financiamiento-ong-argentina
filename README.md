# Monitor de Financiamiento Internacional

![Tablero interactivo](Tablero_interactivo.gif)

Descripción del Proyecto

Este tablero interactivo de Power BI analiza el flujo de fondos de la cooperación internacional dirigidos a Organizaciones de la Sociedad Civil (OSC) en Argentina durante el periodo 2023-2024. El objetivo es visualizar quiénes financian, qué sectores son priorizados y cómo se alinean estos fondos con los Objetivos de Desarrollo Sostenible (ODS).

- Dataset: Registros de la OCDE (Creditor Reporting System - CRS).

Tecnologías Utilizadas

- Python: Para la extracción, unificación y limpieza de los datos crudos.

- Power BI: Para el modelado de datos, creación de medidas DAX y diseño de la interfaz visual.

Metodología y Proceso (ETL)

El proyecto destaca por un proceso de transformación de datos fuera de Power BI para asegurar la calidad de la información:

- Extracción: Descarga de datos crudos en formato .csv desde OECD Explorer (Fuentes Oficiales y Fundaciones Privadas).

- Procesamiento (Python): Se utilizó un script para unificar los archivos, estandarizar nombres de sectores y realizar una alineación estimada con los ODS basada en la categorización de sectores de la OCDE.

- Visualización: Diseño de un dashboard enfocado en la experiencia de usuario (UX) para facilitar la toma de decisiones.


Hallazgos Clave (Insights)

- Liderazgo de Donantes: Estados Unidos se posiciona como el principal donante en el periodo analizado.

- Foco en ODS: Existe una fuerte concentración de recursos en el ODS 2 (Hambre Cero) y sectores vinculados a la Agricultura.

- Tendencia: Se observa una retracción en el volumen de fondos recibidos en 2024 en comparación con 2023, en sintonía con el contexto económico global y local.


Estructura del Repositorio

- donantes_publicos.csv: Datos originales de fondos por parte de fuentes publicas (gobiernos) (OCDE).

- donantes_privados.csv: Datos originales de fondos por partes de fuentes privadas (fundaciones) (OCDE).

- dataset_final.csv: Archivo unificado y procesado listo para Power BI.

- procesamiento_datos.py: Script de Python utilizado para la limpieza y unificación.

- Monitor_Financiamiento_Argentina.pbix: Archivo del tablero interactivo de Power BI.

- Tablero.jpg: Captura de pantalla del dashboard para visualización rápida.


Nota Metodológica

- La asignación de ODS en este tablero es una estimación analítica propia basada en el mapeo de sectores principales reportados por la OCDE. Los datos de 2024 son preliminares y están sujetos a actualizaciones por parte de los organismos reportantes.
