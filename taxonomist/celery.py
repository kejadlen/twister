from __future__ import absolute_import

from celery import Celery

app = Celery('taxonomist',
             broker='redis://localhost',
             backend='redis://localhost',
             include=['taxonomist'])

app.conf.update(CELERY_TASK_SERIALIZER='json',
                CELERY_RESULT_SERIALIZER='json',
                CELERY_ACCEPT_CONTENT=['json'],
                CELERY_ENABLE_UTC=True)