import logging
from scripts.extract import extract_race_results
from scripts.transform import transform_race_data
from scripts.load import load_data_to_postgres

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_pipeline(year: int = 2023):
    """
    Orquestador principal del Pipeline ETL de F1.
    """
    logging.info(f"=== INICIANDO PIPELINE ETL DE FÓRMULA 1 (TEMPORADA {year}) ===")

    # 1. Extracción
    raw_data = extract_race_results(year)

    # 2. Transformación
    clean_df = transform_race_data(raw_data)

    # 3. Carga
    load_data_to_postgres(clean_df, table_name="f1_races")

    logging.info("=== PIPELINE EJECUTADO CON ÉXITO ===")


if __name__ == "__main__":
    # Ejecutamos el flujo completo
    run_pipeline(2023)