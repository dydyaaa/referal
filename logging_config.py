import logging
from logging.config import dictConfig
import re
import requests


class WerkzeugFilter(logging.Filter):
    """Фильтр для очистки логов werkzeug."""
    def filter(self, record):
        # Убираем IP-адрес и дату в квадратных скобках
        record.msg = re.sub(r'^\d+\.\d+\.\d+\.\d+ - - \[\d+\/\w+\/\d+[:\d+ ]+\] ', '', record.msg)
        # Убираем лишний дефис в конце, если есть
        record.msg = record.msg.rstrip('- ')
        return True

class LokiHandler(logging.Handler):
    """Кастомный handler для отправки логов в Loki через HTTP."""
    def __init__(self, url, labels=None):
        super().__init__()
        # URL Loki API, например, 'http://localhost:3100/loki/api/v1/push'
        self.url = 'http://loki:3100/loki/api/v1/push'  
        self.labels = labels or {"job": "flask_app"}  # Метки по умолчанию
        self.session = requests.Session() 

    def emit(self, record):
        try:
            log_entry = self.format(record)
            
            timestamp = int(record.created * 1e9) 
            
            payload = {
                "streams": [{
                    "stream": self.labels,
                    "values": [[str(timestamp), log_entry]]
                }]
            }
            
            self.session.post(self.url, json=payload, headers={"Content-Type": "application/json"})
        except Exception as e:
            self.handleError(record)

def setup_logging(test_mode):
    """Настройка логирования через dictConfig."""
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(levelname)s | %(name)s | %(asctime)s | line %(lineno)d | %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'werkzeug': {
                'format': '%(levelname)s | %(name)s | %(asctime)s | line %(lineno)d | %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout',
            },
            'error_file': {
                'class': 'logging.FileHandler',
                'level': 'ERROR',
                'formatter': 'standard',
                'filename': 'error.log',
                'mode': 'a',
            },
            'app_file': {
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'filename': 'app.log',
                'mode': 'a',
            },
            'loki': {
                'class': 'logging_config.LokiHandler', 
                'level': 'INFO',
                'formatter': 'standard',
                'url': 'http://loki:3100/loki/api/v1/push',  # URL вашего Loki
                'labels': {'job': 'flask_app', 'env': 'production'},
            }
        },
        'loggers': {
            '': {
                'handlers': ['console'] if test_mode else ['console', 'app_file', 'error_file', 'loki'],
                'level': 'INFO',
                'propagate': True,
            },
            'werkzeug': {
                'handlers': ['console'] if test_mode else ['console', 'app_file', 'error_file', 'loki'],
                'level': 'INFO',
                'propagate': False,
                'filters': ['werkzeug_filter'],
            },
            'app': {
                'handlers': ['console'] if test_mode else ['console', 'app_file', 'error_file', 'loki'],
                'level': 'INFO',
                'propagate': False,
            },
            'app.auth': {
                'handlers': ['console'] if test_mode else ['console', 'app_file', 'error_file', 'loki'],
                'level': 'INFO',
                'propagate': False,
            },
            'app.referral': {
                'handlers': ['console'] if test_mode else ['console', 'app_file', 'error_file', 'loki'],
                'level': 'INFO',
                'propagate': False,
            },
        },
        'filters': {
            'werkzeug_filter': {
                '()': WerkzeugFilter
            }
        }
    }
    
    dictConfig(LOGGING_CONFIG)
