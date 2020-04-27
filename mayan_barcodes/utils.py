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
from django.apps.registry import apps

logger = logging.getLogger(__name__)

def get_document_barcodes(instance):
    Barcode = apps.get_model(
        app_label="mayan_barcodes", model_name='Barcode'
    )
    return Barcode.objects.filter(document_page__document_version__document=instance)
    
def get_document_version_barcodes(instance):
    Barcode = apps.get_model(
        app_label="mayan_barcodes", model_name='Barcode'
    )
    return Barcode.objects.filter(document_page__document_version=instance)

def get_instance_barcodes(instance):
    logger.info("Getting barcodes for %s" % instance)
    
    for page in instance.pages.all():
        for barcode in page.barcodes.all():
            yield barcode

