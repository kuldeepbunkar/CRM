from .settings import *

DEBUG = True

DATABASE_CONFIG.update({
    'name': 'crm_dev.db',
    'backup_path': 'data/backups/dev/'
})

EMAIL_CONFIG.update({
    'smtp_server': 'localhost',
    'smtp_port': 1025  # For development mail server
}) 