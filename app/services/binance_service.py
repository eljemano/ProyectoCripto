# Interaccion con API de Binance
import os
from binance import client

def get_binance_client():
    """Crea y retorna un cliente de Binance usando las variables de entorno."""
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        raise ValueError("Faltan las variables de entorno BINANCE_API_KEY o BINANCE_API_SECRET")
    return client.Client(api_key, api_secret)

def get_market_data(symbol: str, interval: str = '10m', limit: int = 500):
    """Obtiene datos de mercado para un símbolo específico."""
    binance_client = get_binance_client()
    try:
        ticker = binance_client.get_ticker(symbol=symbol)
        return ticker
    except Exception as e:
        print(f"Error al obtener datos de mercado para {symbol}: {str(e)}")
        return None