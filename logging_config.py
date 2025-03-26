import logging
from logging.config import dictConfig
import re

class WerkzeugFilter(logging.Filter):
    """Фильтр для очистки логов werkzeug."""
    def filter(self, record):
        # Убираем IP-адрес и дату в квадратных скобках
        record.msg = re.sub(r'^\d+\.\d+\.\d+\.\d+ - - \[\d+\/\w+\/\d+[:\d+ ]+\] ', '', record.msg)
        # Убираем лишний дефис в конце, если есть
        record.msg = record.msg.rstrip('- ')
        return True


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
            }
        },
        'loggers': {
            '': {
                'handlers': ['console'] if test_mode else ['console', 'app_file', 'error_file'],
                'level': 'INFO',
                'propagate': True,
            },
            'werkzeug': {
                'handlers': ['console'] if test_mode else ['console', 'app_file', 'error_file'],
                'level': 'INFO',
                'propagate': False,
                'filters': ['werkzeug_filter'],
            },
            'app': {
                'handlers': ['console'] if test_mode else ['console', 'app_file', 'error_file'],
                'level': 'INFO',
                'propagate': False,
            },
            'app.auth': {
                'handlers': ['console'] if test_mode else ['console', 'app_file', 'error_file'],
                'level': 'INFO',
                'propagate': False,
            },
            'app.referral': {
                'handlers': ['console'] if test_mode else ['console', 'app_file', 'error_file'],
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
