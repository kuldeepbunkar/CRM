from .settings import *

DEBUG = False

DATABASE_CONFIG.update({
    'name': 'crm_prod.db',
    'backup_path': '/var/backups/crm/',
    'backup_frequency': 'daily'
})

EMAIL_CONFIG.update({
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'use_tls': True
})

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/error.log',
        },
    },
    'loggers': {
        'crm': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
} 