import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def transform_race_data(raw_sessions: list) -> pd.DataFrame:
    """
    Transforma la lista de carreras extraída de la API en un DataFrame de Pandas limpio y estructurado.
    """
    if not raw_sessions:
        logging.warning("No se recibieron datos para transformar.")
        return pd.DataFrame()

    logging.info("Iniciando la transformación de datos con Pandas...")

    # 1. Convertimos la lista de diccionarios JSON a un DataFrame de Pandas
    df = pd.DataFrame(raw_sessions)

    # 2. Seleccionamos y reinsertamos únicamente las columnas relevantes para nuestro análisis
    columns_to_keep = {
        'session_key': 'session_id',
        'location': 'location',
        'country_name': 'country',
        'circuit_short_name': 'circuit_name',
        'date_start': 'start_time',
        'date_end': 'end_time',
        'year': 'year'
    }

    # Mantenemos solo las columnas existentes en los datos
    available_cols = [col for col in columns_to_keep.keys() if col in df.columns]
    df = df[available_cols].rename(columns=columns_to_keep)

    # 3. Limpieza de Tipos de Datos: Convertimos fechas a formato datetime nativo
    if 'start_time' in df.columns:
        df['start_time'] = pd.to_datetime(df['start_time'])
    if 'end_time' in df.columns:
        df['end_time'] = pd.to_datetime(df['end_time'])

    # 4. Manejo de valores nulos o faltantes
    df = df.dropna(subset=['session_id', 'location'])

    logging.info(f"Transformación completada con éxito. Se procesaron {len(df)} registros.")
    return df


if __name__ == "__main__":
    # Prueba individual combinando la extracción y la transformación
    from extract import extract_race_results

    raw_data = extract_race_results(2023)
    transformed_df = transform_race_data(raw_data)

    print("\n--- Vista previa del DataFrame Transformado ---")
    print(transformed_df.head())
    print("\nTipos de datos de las columnas:")
    print(transformed_df.dtypes)