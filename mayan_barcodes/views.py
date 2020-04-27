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
from django.contrib import messages

from mayan.apps.common.generics import SingleObjectListView,\
    SingleObjectEditView, FormView
from mayan_barcodes.permissions import permission_barcodes_view,\
    permission_barcodes_setup
from mayan_barcodes.icons import icon_document_barcodes
from mayan_barcodes.models import Barcode, DocumentTypeSettings
from mayan.apps.common.mixins import ExternalObjectMixin
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.models.document_type_models import DocumentType
from django.urls.base import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect
from mayan.apps.documents.forms.document_type_forms import DocumentTypeFilteredSelectForm


class BarcodeListView(SingleObjectListView):
    object_permission = permission_barcodes_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_document_barcodes,
            'no_results_text': _(
                'The document contains no barcodes or hasn\'t been scaned yet'
            ),
            'no_results_title': _('No barcodes available'),
            'title': _('Barcodes'),
        }

    def get_source_queryset(self):
        return self.get_tag_queryset()

    def get_barcode_queryset(self):
        return Barcode.objects.all()

class DocumentBarcodeListView(ExternalObjectMixin, BarcodeListView):
    external_object_class = Document
    external_object_permission = permission_barcodes_view
    external_object_pk_url_kwarg = 'document_id'

    def get_extra_context(self):
        context = super(DocumentBarcodeListView, self).get_extra_context()
        context.update(
            {
                'hide_link': True,
                'object': self.external_object,
                'title': _(
                    'Barcodes for document: %s'
                ) % self.external_object,
            }
        )
        return context
    
    def get_source_queryset(self):
        return self.external_object.barcodes().all()


class DocumentTypeSettingsEditView(ExternalObjectMixin, SingleObjectEditView):
    external_object_class = DocumentType
    external_object_permission = permission_barcodes_setup
    external_object_pk_url_kwarg = 'document_type_id'
    fields = ('auto_scan',)
    post_action_redirect = reverse_lazy(
        viewname='documents:document_type_list'
    )

    def get_document_type(self):
        return self.external_object

    def get_extra_context(self):
        return {
            'object': self.get_document_type(),
            'title': _(
                'Edit Barcode settings for document type: %s.'
            ) % self.get_document_type()
        }

    def get_object(self, queryset=None):
        try:
            return self.get_document_type().barcode_settings
        except:
            return DocumentTypeSettings.objects.create(document_type=self.get_document_type())

class DocumentTypeSubmitView(FormView):
    extra_context = {
        'title': _('Submit all documents of a type for barcode scanning')
    }
    form_class = DocumentTypeFilteredSelectForm
    post_action_redirect = reverse_lazy(viewname='common:tools_list')

    def form_valid(self, form):
        count = 0
        for document_type in form.cleaned_data['document_type']:
            for document in document_type.documents.all():
                document.submit_for_scan()
                count += 1

        messages.success(
            message=_(
                '%(count)d documents added to the OCR queue.'
            ) % {
                'count': count,
            }, request=self.request
        )

        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def get_form_extra_kwargs(self):
        return {
            'allow_multiple': True,
            'permission': permission_barcodes_setup,
            'user': self.request.user
        }

    def get_post_action_redirect(self):
        return reverse(viewname='common:tools_list')
