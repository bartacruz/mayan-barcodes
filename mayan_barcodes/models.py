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

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils.encoding import force_text
from mayan.apps.documents.models.document_page_models import DocumentPage
from mayan.apps.documents.models.document_type_models import DocumentType
from .managers import BarcodesManager

class DocumentTypeSettings(models.Model):
    """
    Model to store the barcode settings for a document type.
    """
    document_type = models.OneToOneField(on_delete=(models.CASCADE),
      related_name='barcode_settings',
      to=DocumentType,
      unique=True,
      verbose_name='Document type')
    auto_scan = models.BooleanField(default=True,
      verbose_name=(_('Automatically queue newly created documents for barcode scan.')))

    class Meta:
        verbose_name = _('Document type settings')
        verbose_name_plural = _('Document types settings')

    def natural_key(self):
        return self.document_type.natural_key()

    natural_key.dependencies = ['documents.DocumentType']


class Barcode(models.Model):
    
    document_page = models.ForeignKey(on_delete=(models.CASCADE),
      related_name='barcodes',
      to=DocumentPage,
      verbose_name=(_('Document page')))
    data = models.CharField(max_length=255, verbose_name=(_('Barcode data')))
    type = models.CharField(max_length=255, verbose_name=(_('Barcode type')))
    
    objects = BarcodesManager()

    class Meta:
        verbose_name = _('Document page barcodes')
        verbose_name_plural = _('Document pages barcodes')

    def __str__(self):
        return force_text('%s: %s,%s)' % (self.document_page, self.data, self.type))

