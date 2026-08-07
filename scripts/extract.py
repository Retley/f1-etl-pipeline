import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_race_results(year: int = 2023) -> list:
    """
    Extrae información de carreras desde OpenF1 API.
    """
    url = f"https://api.openf1.org/v1/sessions?year={year}&session_name=Race"

    try:
        logging.info(f"Iniciando la extracción de datos de la temporada {year} desde OpenF1...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        sessions = response.json()
        logging.info(f"Extracción completada con éxito. Se obtuvieron {len(sessions)} carreras.")
        return sessions

    except requests.exceptions.RequestException as e:
        logging.error(f"Error al conectar con la API de F1: {e}")
        raise


if __name__ == "__main__":
    data = extract_race_results(2023)
    if data:
        print(f"\n✅ Primera carrera extraída: {data[0].get('location')} - Fecha: {data[0].get('date_start')}")