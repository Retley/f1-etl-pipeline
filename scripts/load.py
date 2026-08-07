import sys
import os
import pandas as pd
import logging

# Añadimos la raíz del proyecto al sys.path para poder importar config.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import get_db_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_data_to_postgres(df: pd.DataFrame, table_name: str = "f1_races") -> None:
    """
    Carga un DataFrame de Pandas a la base de datos PostgreSQL.
    Si la tabla no existe, la crea automáticamente con el esquema inferido.
    """
    if df.empty:
        logging.warning("El DataFrame está vacío. No hay datos para cargar.")
        return

    try:
        engine = get_db_engine()
        logging.info(f"Cargando {len(df)} registros en la tabla '{table_name}' de PostgreSQL...")

        # if_exists='replace' recrea la tabla en cada corrida limpia.
        # En producción se usa 'append' con control de claves primarias.
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False
        )

        logging.info(f"✅ ¡Datos cargados exitosamente en la tabla '{table_name}'!")

    except Exception as e:
        logging.error(f"❌ Error al cargar los datos en PostgreSQL: {e}")
        raise


if __name__ == "__main__":
    # Prueba individual del módulo de carga
    from extract import extract_race_results
    from transform import transform_race_data

    raw_data = extract_race_results(2023)
    clean_df = transform_race_data(raw_data)
    load_data_to_postgres(clean_df)