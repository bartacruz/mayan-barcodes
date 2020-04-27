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
from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Barcodes'), name='mayan_barcodes')

permission_barcodes_view = namespace.add_permission(
    label=_('View the barcodes found in documents'),
    name='barcodes_view'
)
permission_barcodes_setup = namespace.add_permission(
    label=_('Setup barcode scan'),
    name='barcodes_setup'
)

