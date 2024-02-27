from odoo import models, fields

class PatientTag(models.Model):
    _name = "medical.patient.tag"
    _description = "Tags to assign to patients."
    
    name = fields.Char()
    color = fields.Integer()
    active = fields.Boolean(default=True)