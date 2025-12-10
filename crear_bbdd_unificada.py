import pandas as pd
import os
import concurrent.futures
from deep_translator import GoogleTranslator
from tqdm import tqdm  # Importamos la librería de la barra de progreso

# Configuración
ARCHIVO_BEDCA = 'BASE_DATOS_BEDCA_COMPLETA.csv'
ARCHIVO_USDA = 'BASE_DATOS_USDA_COMPLETA.csv'
ARCHIVO_SALIDA = 'Listado_Alimentos_Unificado.xlsx'

# Ajustes de velocidad
WORKERS = 8       # Hilos simultáneos
TAMANO_LOTE = 50  # Palabras por envío

def traducir_sub_lote(lote):
    """ Función auxiliar que ejecuta un solo hilo """
    try:
        traductor = GoogleTranslator(source='en', target='es')
        return traductor.translate_batch(lote)
    except Exception as e:
        # Si falla un lote, devolvemos el original
        return lote

def traduccion_rapida_con_barra(lista_textos):
    """
    Divide la lista y muestra una barra de progreso visual (tqdm).
    """
    total_items = len(lista_textos)
    
    # Dividir la lista en lotes
    lotes = [lista_textos[i:i + TAMANO_LOTE] for i in range(0, total_items, TAMANO_LOTE)]
    total_lotes = len(lotes)
    
    print(f"   > Preparando traducción paralela de {total_items} alimentos en {total_lotes} lotes...")
    
    resultados_ordenados = []
    
    # Ejecutamos en paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
        # executor.map mantiene el orden de los resultados automáticamente
        resultados_iterador = executor.map(traducir_sub_lote, lotes)
        
        # Envolvemos el iterador con tqdm para ver la barra
        # total=total_lotes: le dice a la barra cuál es el 100%
        # unit="lote": para que diga "5 lotes/segundo"
        for resultado_lote in tqdm(resultados_iterador, total=total_lotes, unit="lote", desc="Traduciendo", ncols=100):
            resultados_ordenados.extend(resultado_lote)

    print("   > ¡Traducción completada!")
    return resultados_ordenados

def unificar_ficheros_csv():
    print("--- Iniciando proceso de unificación PROFESIONAL ---")
    
    if not os.path.exists(ARCHIVO_BEDCA) or not os.path.exists(ARCHIVO_USDA):
        print(f"Error: Faltan archivos .csv en la carpeta.")
        return

    print("1. Cargando archivos CSV...")
    df_bedca = pd.read_csv(ARCHIVO_BEDCA)
    df_usda = pd.read_csv(ARCHIVO_USDA)

    print("2. Iniciando motor de traducción (USDA -> Español)...")
    
    # Limpiamos y preparamos la lista
    nombres_ingles = df_usda['f_ori_name'].fillna('').astype(str).tolist()
    
    # Llamamos a la nueva función con barra visual
    nombres_espanol = traduccion_rapida_con_barra(nombres_ingles)
    
    # Asignamos
    df_usda['f_ori_name'] = nombres_espanol

    print("3. Normalizando y unificando tablas...")
    df_bedca['Fuente'] = 'BEDCA'
    df_usda['Fuente'] = 'USDA'

    def limpiar_nombre(nombre):
        return " ".join(nombre.split())

    df_bedca.columns = [limpiar_nombre(c) for c in df_bedca.columns]
    df_usda.columns = [limpiar_nombre(c) for c in df_usda.columns]

    df_total = pd.concat([df_bedca, df_usda], ignore_index=True, sort=False)

    cols = [c for c in df_total.columns if c != 'Fuente']
    df_total = df_total[cols + ['Fuente']]

    df_total = df_total.fillna("NA")

    print(f"4. Guardando archivo final: {ARCHIVO_SALIDA}...")
    df_total.to_excel(ARCHIVO_SALIDA, index=False)

    print(f"\n¡Todo listo! Se han unificado {len(df_total)} alimentos.")

if __name__ == "__main__":
    unificar_ficheros_csv()