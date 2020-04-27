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
from mayan.apps.navigation.classes import Link

from .permissions import permission_barcodes_view, permission_barcodes_setup


def is_document_page_disabled(context):
    return not context['resolved_object'].enabled

link_document_page_barcodes = Link(
    args='resolved_object.id', conditional_disable=is_document_page_disabled,
    icon_class_path='mayan_barcodes.icons.icon_document_barcodes',
    permissions=(permission_barcodes_view,), 
    text=_('Barcodes'),
    view='mayan_barcodes:document_page_barcodes',
)
link_document_barcodes = Link(
    args='resolved_object.id', 
    icon_class_path='mayan_barcodes.icons.icon_document_barcodes',
    permissions=(permission_barcodes_view,), 
    text=_('Barcodes'),
    view='mayan_barcodes:document_barcodes',
)
link_document_type_barcode_settings = Link(
    args='resolved_object.id',
    icon_class_path='mayan_barcodes.icons.icon_document_barcodes',
    permissions=(permission_barcodes_setup,), 
    text=_('Setup barcodes'),
    view='mayan_barcodes:document_type_barcodes',
)

link_document_type_submit = Link(
    icon_class_path='mayan_barcodes.icons.icon_document_barcodes',
    permissions=(permission_barcodes_setup,), 
    text=_('Scan barcodes per document type'),
    view='mayan_barcodes:document_type_submit'
)

