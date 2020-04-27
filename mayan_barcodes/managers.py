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

from django.db import models
from mayan.apps.acls.models import AccessControlList
from .permissions import permission_barcodes_view

class BarcodesManager(models.Manager):
    
    def get_for_document(self, document, user):
        queryset = self.filter(
            document_page__in=document.pages
        )
        return AccessControlList.objects.restrict_queryset(
            permission=permission_barcodes_view,
            queryset=queryset, user=user
        )
    
    def get_for_page(self, page, user):        
        queryset = self.filter(
            document_page=page
        )
        return AccessControlList.objects.restrict_queryset(
            permission=permission_barcodes_view,
            queryset=queryset, user=user
        )

