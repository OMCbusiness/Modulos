{
    'name': 'Medical application',
    'version': '15.0.1.0.0',
    'summary': 'Management of patients and therapists.',
    'category': 'Contacts',
    'author': 'Javier L. de los Mozos',
    'maintainer': 'Javier L. de los Mozos',
    'depends': ['contacts', 'resource', 'survey_crm_generation', 'sales_team'],
    'data': [
        'views/medical_views.xml',
        'views/partner_views.xml',
        'views/therapist_calendar_views.xml',
        'views/survey_survey_patient_views.xml',
        'views/survey_survey_partner_views.xml',
        'views/crm_menu_views.xml',
        'views/crm_stage_views.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
    ],
    'images': [],
    'license': 'Other proprietary',
    'installable': True,
    'application': True
}
