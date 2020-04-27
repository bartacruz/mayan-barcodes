# -*- encoding: utf-8 -*-
'''
Created on 26 abr. 2020
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
from django.conf.urls import url
from .views import DocumentTypeSettingsEditView, DocumentBarcodeListView
from mayan_barcodes.views import DocumentTypeSubmitView

urlpatterns = [
url(
        regex=r'^document_types/(?P<document_type_id>\d+)/barcodes/settings/$',
        name='document_type_barcodes',
        view=DocumentTypeSettingsEditView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/barcodes/$',
        name='document_barcodes', view=DocumentBarcodeListView.as_view()
    ),
    url(
        regex=r'^document_types/submit/$', name='document_type_submit',
        view=DocumentTypeSubmitView.as_view()
    ),
    
    
]    