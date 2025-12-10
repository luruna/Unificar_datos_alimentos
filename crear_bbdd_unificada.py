import pandas as pd
import os

def unificar_ficheros_csv():
    print("--- Iniciando proceso de unificación ---")
    
    archivo_bedca = 'BASE_DATOS_BEDCA_COMPLETA.csv'
    archivo_usda = 'BASE_DATOS_USDA_COMPLETA.csv'

    # Verificación de existencia de archivos
    if not os.path.exists(archivo_bedca) or not os.path.exists(archivo_usda):
        print(f"Error: Asegúrate de tener '{archivo_bedca}' y '{archivo_usda}' en la carpeta.")
        return

    print("Cargando archivos CSV...")
    df_bedca = pd.read_csv(archivo_bedca)
    df_usda = pd.read_csv(archivo_usda)

    # Crear columna Fuente
    df_bedca['Fuente'] = 'BEDCA'
    df_usda['Fuente'] = 'USDA'

    # Función para normalizar nombres de columnas (quita espacios extra)
    def limpiar_nombre(nombre):
        return " ".join(nombre.split())

    df_bedca.columns = [limpiar_nombre(c) for c in df_bedca.columns]
    df_usda.columns = [limpiar_nombre(c) for c in df_usda.columns]

    # Concatenar
    print("Unificando bases de datos...")
    df_total = pd.concat([df_bedca, df_usda], ignore_index=True, sort=False)

    # Reordenar para que 'Fuente' sea la última columna
    cols = [c for c in df_total.columns if c != 'Fuente']
    df_total = df_total[cols + ['Fuente']]

    # RELLENAR VACÍOS CON "NA"
    # Esto busca cualquier valor nulo o NaN y lo reemplaza por el texto "NA"
    df_total = df_total.fillna("NA")

    # Guardar
    nombre_salida = 'Listado_Alimentos_Unificado.xlsx'
    print(f"Guardando archivo: {nombre_salida}...")
    df_total.to_excel(nombre_salida, index=False)

    print(f"\n¡Proceso terminado con éxito!")
    print(f"Total de alimentos: {len(df_total)}")

if __name__ == "__main__":
    unificar_ficheros_csv()