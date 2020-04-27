# -*- encoding: utf-8 -*-
'''
Created on 24 abr. 2020
@author: julio

Copyright (C) 2020  Julio Santa Cruz <bartacruz@gmail.com>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

'''
import logging

from django.apps import apps
from pyzbar.pyzbar import decode
import PIL
from mayan_barcodes.events import event_barcode_document_version_finish
from django.db import transaction
from mayan_barcodes.signals import post_document_version_barcode_scan

logger = logging.getLogger(name=__name__)



def handler_initialize_new_barcode_settings(sender, instance, **kwargs):
    DocumentTypeSettings = apps.get_model(
        app_label='mayan_barcodes', model_name='DocumentTypeSettings'
    )

    if kwargs['created']:
        DocumentTypeSettings.objects.create(
            document_type=instance, auto_scan=False # TODO: use settings
        )


def handler_document_version(sender, instance, **kwargs):
    logger.debug('received post_version_upload')
    logger.debug('instance pk: %s', instance.pk)
    Barcode = apps.get_model(
        app_label='mayan_barcodes', model_name='Barcode'
    )

    if instance.document.document_type.barcode_settings.auto_scan:
        logger.debug("Searching for barcodes on %s" % instance)
        for page in instance.pages:
            image = PIL.Image.open(page.get_image())
            detected_barcodes = decode(image)
            for decoded in detected_barcodes:
                try:
                    # Avoid duplicated entries on already scanned pages
                    barcode=Barcode.objects.get(document_page=page,data=decoded.data.decode("utf-8"),type=decoded.type)
                    logger.debug("Barcode already exists on page. Ignoring")
                except Barcode.DoesNotExist:
                    barcode = Barcode(document_page=page,data=decoded.data.decode("utf-8"),type=decoded.type)
                    barcode.save()
                    logger.debug("Barcode obtained %s" % barcode)
                except:
                    logger.exception("Decoding barcode %s" % str(decoded))
                
        
        with transaction.atomic():
            logger.debug("Sending barcode scan signals for %s" % instance)
            event_barcode_document_version_finish.commit(
                action_object=instance.document,
                target=instance
            )

            transaction.on_commit(
                lambda: post_document_version_barcode_scan.send(
                    sender=instance.__class__,
                    instance=instance
                )
            )
            logger.debug("Finished barcode scan signals for %s" % instance)
