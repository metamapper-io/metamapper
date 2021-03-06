# -*- coding: utf-8 -*-
from utils import logging

from metamapper.celery import app

from app.inspector import service as inspector
from app.definitions.models import Datastore


__all__ = [
    'check_for_version_update',
]


@app.task(bind=True)
@logging.task_logger(__name__)
def check_for_version_update(self, datastore_id):
    """Check if the version of the datastore needs to be updated.
    """
    datastore = Datastore.objects.get(pk=datastore_id)
    dbversion = inspector.version(datastore)

    if dbversion != datastore.version:
        datastore.version = dbversion
        datastore.save()
