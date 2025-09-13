# -*- coding: utf-8 -*-
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Enum, Index, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Crear la clase base
Base = declarative_base()

# Definicion de Enums
class IntervalType(enum.Enum):
    MIN_10 = "10m"
    HOUR_1 = "1h"
    DAY_1 = "1d"

class SignalType(enum.Enum):
    BUY = "Compra"
    SELL = "Venta"
    HOLD = "Mantener"

class SeverityLevel(enum.Enum):
    CRITICAL = "Critica"
    HIGH = "Alta"
    MEDIUM = "Media"
    LOW = "Baja"

class DataSource(enum.Enum):
    BINANCE = "Binance"
    COINGECKO = "CoinGecko"
    MANUAL = "Manual"

class TransactionType(enum.Enum):
    BUY = "Compra"
    SELL = "Venta"
    DEPOSIT = "Deposito"
    WITHDRAWAL = "Retiro"

class TransactionStatus(enum.Enum):
    PENDING = "Pendiente"
    COMPLETED = "Completada"
    FAILED = "Fallida"

class TrendType(enum.Enum):
    BULLISH = "Alcista"
    BEARISH = "Bajista"
    NEUTRAL = "Neutral"

class PortfolioType(enum.Enum):
    MAIN = "Principal"
    TRADING = "Trading"
    TEST = "Prueba"

#===========================================
# ESTRUCTURA DE LA BASE DE DATOS ACTUALIZADA
#===========================================

class Crypto(Base):
    __tablename__ = 'crypto'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False)
    name = Column(String(100), nullable=False)
    monitoring_enabled = Column(Boolean, default=True)
    
    # Nuevos campos
    weight = Column(Float, default=5.0)
    last_weight_update = Column(DateTime)
    market_cap = Column(Float)
    price_change_24h = Column(Float)
    volume_24h = Column(Float)
    last_anomaly_detected = Column(DateTime)
    anomaly_count_24h = Column(Integer, default=0)
    
    # Timestamps de auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relaciones con otras tablas
    price_data = relationship("PriceData", back_populates="crypto")
    indicators = relationship("TechnicalIndicator", back_populates="crypto")
    events = relationship("AnomalyEvent", back_populates="crypto")
    transactions = relationship("Transaction", back_populates="crypto")
    holdings = relationship("PortfolioHolding", back_populates="crypto")

class PriceData(Base):
    __tablename__ = 'price_data'
    id = Column(Integer, primary_key=True)
    crypto_id = Column(Integer, ForeignKey('crypto.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    interval = Column(Enum(IntervalType), nullable=False)

    # Datos OHLCV
    open_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    # Campos calculados localmente
    price_change_pct = Column(Float)
    num_trades = Column(Integer)
    source = Column(Enum(DataSource), default=DataSource.BINANCE)

    # Timestamps de auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    crypto = relationship("Crypto", back_populates="price_data")
    indicators = relationship("TechnicalIndicator", back_populates="price_data")

class TechnicalIndicator(Base):
    __tablename__ = 'technical_indicator'
    id = Column(Integer, primary_key=True)
    crypto_id = Column(Integer, ForeignKey('crypto.id'), nullable=False)
    price_data_id = Column(Integer, ForeignKey('price_data.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    interval = Column(Enum(IntervalType), nullable=False)

    # Indicadores de momentum
    rsi_14 = Column(Float)
    
    # MACD
    macd_line = Column(Float)
    macd_signal = Column(Float)
    macd_histogram = Column(Float)
    
    # Bollinger Bands
    bb_upper = Column(Float)
    bb_middle = Column(Float)
    bb_lower = Column(Float)
    
    # Medias moviles
    price_ma_20 = Column(Float)
    volume_ma = Column(Float)

    # Niveles de soporte y resistencia
    pivot_point = Column(Float)
    resistance_1 = Column(Float)
    resistance_2 = Column(Float)
    support_1 = Column(Float)
    support_2 = Column(Float)

    # Analisis de sentimiento y seniales
    sentiment_score = Column(Float)
    llm_used = Column(String(50))
    trend = Column(Enum(TrendType))
    signal = Column(Enum(SignalType))

    # Timestamps de auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    crypto = relationship("Crypto", back_populates="indicators")
    price_data = relationship("PriceData", back_populates="indicators")

class AnomalyEvent(Base):
    __tablename__ = 'anomaly_event'
    id = Column(Integer, primary_key=True)
    crypto_id = Column(Integer, ForeignKey('crypto.id'), nullable=False)
    detected_at = Column(DateTime, nullable=False)
    event_type = Column(String(100), nullable=False)
    severity = Column(Enum(SeverityLevel), nullable=False)
    description = Column(Text)
    source = Column(Enum(DataSource), default=DataSource.BINANCE)
    source_url = Column(String(500))
    is_notified = Column(Boolean, default=False)
    
    # Nuevos campos
    price_before = Column(Float)
    price_after = Column(Float)
    volume_before = Column(Float)
    volume_after = Column(Float)
    impact_score = Column(Float)
    
    # Timestamps de auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    crypto = relationship("Crypto", back_populates="events")
    decision = relationship("Decision", back_populates="event", uselist=False)
    notifications = relationship("Notification", back_populates="event")

class Decision(Base):
    __tablename__ = 'decision'
    id = Column(Integer, primary_key=True)
    anomaly_event_id = Column(Integer, ForeignKey('anomaly_event.id'), nullable=False)
    action = Column(Enum(SignalType), nullable=False)
    confidence = Column(Integer, nullable=False)
    reason = Column(Text, nullable=False)
    
    # Timestamps de auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    event = relationship("AnomalyEvent", back_populates="decision")
    notifications = relationship("Notification", back_populates="decision")

class Notification(Base):
    __tablename__ = 'notification'
    id = Column(Integer, primary_key=True)
    anomaly_event_id = Column(Integer, ForeignKey('anomaly_event.id'), nullable=False)
    decision_id = Column(Integer, ForeignKey('decision.id'), nullable=False)
    telegram_user_id = Column(Integer, ForeignKey('telegram_user.id'), nullable=False)
    sent_at = Column(DateTime, nullable=False)
    message = Column(Text, nullable=False)
    
    # Timestamps de auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    event = relationship("AnomalyEvent", back_populates="notifications")
    decision = relationship("Decision", back_populates="notifications")
    telegram_user = relationship("TelegramUser", back_populates="notifications")

class Portfolio(Base):
    __tablename__ = 'portfolio'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum(PortfolioType), nullable=False)
    total_invested = Column(Float, default=0.0)
    total_value_current = Column(Float, default=0.0)
    
    # Timestamps de auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    holdings = relationship("PortfolioHolding", back_populates="portfolio")
    transactions = relationship("Transaction", back_populates="portfolio")

class PortfolioHolding(Base):
    __tablename__ = 'portfolio_holding'
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolio.id'), nullable=False)
    crypto_id = Column(Integer, ForeignKey('crypto.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    average_buy_price = Column(Float, nullable=False)
    
    # Timestamps de auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    portfolio = relationship("Portfolio", back_populates="holdings")
    crypto = relationship("Crypto", back_populates="holdings")

class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolio.id'), nullable=False)
    crypto_id = Column(Integer, ForeignKey('crypto.id'), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    quantity = Column(Float, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    
    # Campos adicionales para trazabilidad
    binance_order_id = Column(String(50))
    fees_paid = Column(Float, default=0.0)
    notes = Column(Text)
    
    # Timestamps de auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    portfolio = relationship("Portfolio", back_populates="transactions")
    crypto = relationship("Crypto", back_populates="transactions")

class TelegramUser(Base):
    __tablename__ = 'telegram_user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    chat_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    language_code = Column(String(10), default='es')
    
    # Timestamps de auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    last_interaction = Column(DateTime)
    
    notifications = relationship("Notification", back_populates="telegram_user")

class SystemConfig(Base):
    __tablename__ = 'system_config'
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(String(500), nullable=False)
    data_type = Column(String(20), nullable=False)
    description = Column(Text)
    category = Column(String(50))
    is_system = Column(Boolean, default=False)
    
    # Timestamps de auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

# Indices para mejorar el rendimiento
Index('idx_price_crypto_timestamp', PriceData.crypto_id, PriceData.timestamp)
Index('idx_price_interval', PriceData.interval)
Index('idx_anomaly_crypto_detected', AnomalyEvent.crypto_id, AnomalyEvent.detected_at)
Index('idx_anomaly_severity', AnomalyEvent.severity)
Index('idx_crypto_weight', Crypto.weight)
Index('idx_crypto_monitoring', Crypto.monitoring_enabled)
Index('idx_system_config_key', SystemConfig.key)

# Constraints adicionales para validacion
CheckConstraint('weight >= 0 AND weight <= 10', name='crypto_weight_range')
CheckConstraint('confidence >= 0 AND confidence <= 100', name='decision_confidence_range')
CheckConstraint('impact_score >= 0 AND impact_score <= 100', name='anomaly_impact_range')
CheckConstraint('sentiment_score >= -1 AND sentiment_score <= 1', name='sentiment_score_range')

# ===========================================
# DATOS DE CONFIGURACION INICIAL
# ===========================================

INITIAL_SYSTEM_CONFIG = [
    {'key': 'max_monitored_cryptos', 'value': '50', 'data_type': 'integer', 
     'description': 'Numero maximo de criptomonedas a monitorear simultaneamente', 'category': 'monitoring'},
    {'key': 'monitoring_interval_minutes', 'value': '10', 'data_type': 'integer',
     'description': 'Intervalo en minutos para captura de datos', 'category': 'monitoring'},
    {'key': 'weight_recalculation_hours', 'value': '24', 'data_type': 'integer',
     'description': 'Frecuencia en horas para recalcular pesos de criptos', 'category': 'monitoring'},
    {'key': 'anomaly_detection_enabled', 'value': 'true', 'data_type': 'boolean',
     'description': 'Activar/desactivar deteccion de anomalias', 'category': 'monitoring'},
    {'key': 'telegram_notifications_enabled', 'value': 'true', 'data_type': 'boolean',
     'description': 'Activar/desactivar notificaciones por Telegram', 'category': 'notifications'},
    {'key': 'binance_api_calls_per_minute', 'value': '1200', 'data_type': 'integer',
     'description': 'Limite de llamadas a Binance API por minuto', 'category': 'api_limits'},
    {'key': 'llm_provider', 'value': 'Gemini', 'data_type': 'string',
     'description': 'Proveedor de LLM para analisis', 'category': 'ai'},
]
