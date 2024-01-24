# -*- coding: utf-8 -*-
{
    'name': 'Attendance Maps',
    'version': '15.0.1.0.0',
    'author': 'Javier L. de los Mozos',
    'license': 'AGPL-3',
    'support': 'jdelosmozos@coit.es',
    'category': 'Human Resources',
    'description': """
Contacts Maps
=============

Added Google Map view on Attendances
""",
    'depends': [
        'hr_attendance_geolocation',
        'base_geolocalize',
        'web_google_maps',
        'google_marker_icon_picker'
    ],
    'website': '',
    'data': [
#        'views/attendance_map_views.xml',
        'views/check_in_out_views.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [],
    'images': [],
    'installable': True
}
