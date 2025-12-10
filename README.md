# Unificador de Bases de Datos de Alimentos (BEDCA + USDA)

Este proyecto es una herramienta en Python diseñada para unificar dos bases de datos nutricionales importantes: la **BEDCA** (Base de Datos Española de Composición de Alimentos) y la **USDA** (United States Department of Agriculture).

El script procesa los archivos originales en formato CSV, normaliza las columnas para que coincidan entre español e inglés, y genera un único archivo Excel unificado donde se identifica la fuente de cada alimento.

## Características

* **Unificación:** Fusiona listados de BEDCA y USDA.
* **Normalización:** Limpia y estandariza los nombres de las columnas (ej. elimina espacios dobles y normaliza encabezados).
* **Trazabilidad:** Añade una columna `Fuente` al final para identificar si el dato viene de BEDCA o USDA.
* **Limpieza:** Rellena los valores inexistentes con "NA" para facilitar la lectura y evitar errores de procesamiento.

## Requisitos

* Python 3.x
* Librerías listadas en `requirements.txt`

## Instalación y Uso

Se recomienda utilizar un entorno virtual para ejecutar este proyecto y asegurar la consistencia de las librerías.

### 1. Clonar o descargar el repositorio
Coloca los archivos `BASE_DATOS_BEDCA_COMPLETA.csv` y `BASE_DATOS_USDA_COMPLETA.csv` en la carpeta raíz del proyecto.

### 2. Crear y activar un entorno virtual

**En Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
python crear_bbdd_unificada.py