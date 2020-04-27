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
from django.apps.registry import apps
from django.db.models.signals import post_save

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.events.classes import ModelEventType
from mayan.apps.common.classes import ModelFieldRelated, ModelProperty
from mayan.apps.acls.classes import ModelPermission
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.documents.search import document_search, document_page_search
from mayan.apps.common.menus import menu_facet, menu_list_facet, menu_tools
from mayan.apps.documents.signals import post_version_upload

from .events import event_barcode_document_version_finish
from .permissions import permission_barcodes_setup,\
    permission_barcodes_view
from .links import link_document_barcodes, link_document_type_submit, \
    link_document_page_barcodes, link_document_type_barcode_settings
from .utils import get_document_barcodes, get_document_version_barcodes
from .methods import method_document_scan
from mayan_barcodes.handlers import handler_initialize_new_barcode_settings,\
    handler_document_version


class MayanBarcodesConfig(MayanAppConfig):
    app_namespace = 'mayan_barcodes'
    app_url = 'mayan_barcodes'
    has_rest_api = False
    has_tests = False
    name = 'mayan_barcodes'
    verbose_name = _('Barcodes')

    def ready(self):
        super(MayanBarcodesConfig, self).ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentPage = apps.get_model(
            app_label='documents', model_name='DocumentPage'
        )
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        DocumentTypeSettings = self.get_model(
            model_name='DocumentTypeSettings'
        )
        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )

        Barcode = self.get_model(
            model_name='Barcode'
        )

        Document.add_to_class(
            name='barcodes', value=get_document_barcodes
        )
        Document.add_to_class(
            name='submit_for_scan', value=method_document_scan
        )
        DocumentVersion.add_to_class(
            name='ocr_content', value=get_document_version_barcodes
        )
        
        ModelEventType.register(
            model=Document, event_types=(
                event_barcode_document_version_finish,
            )
        )
        
#         ModelFieldRelated(
#             model=Document,
#             name='versions__version_pages__barcodes'
#         )
        ModelProperty(
            description=_(
                'A generator returning the document\'s barcodes.'
            ), label=_('Barcodes'), model=Document,
            name='barcodes'
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_barcodes_setup, permission_barcodes_view,
            )
        )
        ModelPermission.register(
            model=DocumentType, permissions=(
                permission_barcodes_setup,
            )
        )
        ModelPermission.register_inheritance(
            model=DocumentTypeSettings, related='document_type',
        )

        SourceColumn(
            attribute='document_page__page_number', is_sortable=True,
            source=Barcode,
        )
        SourceColumn(
            attribute='data', is_sortable=False,
            source=Barcode,
        )
        SourceColumn(
            attribute='type', is_sortable=True,
            source=Barcode,
        )

        document_search.add_model_field(
            field='versions__version_pages__barcodes', label=_('Barcodes')
        )

        document_page_search.add_model_field(
            field='barcodes', label=_('Barcodes')
        )

        menu_facet.bind_links(
            links=(link_document_barcodes,), sources=(Document,)
        )
        menu_list_facet.bind_links(
            links=(link_document_page_barcodes,), sources=(DocumentPage,)
        )
        menu_list_facet.bind_links(
            links=(link_document_type_barcode_settings,), sources=(DocumentType,)
        )
        
        menu_tools.bind_links(
            links=(
                link_document_type_submit,
            )
        )

        post_save.connect(
            dispatch_uid='handler_initialize_new_barcode_settings',
            receiver=handler_initialize_new_barcode_settings,
            sender=DocumentType
        )
        post_version_upload.connect(
            dispatch_uid='barcodes_handler_document_version',
            receiver=handler_document_version,
            sender=DocumentVersion
        )
