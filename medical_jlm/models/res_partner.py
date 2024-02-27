from odoo import models, fields, api, _

class Partner(models.Model):
    _inherit = 'res.partner'
    
    is_patient = fields.Boolean(compute='_compute_patient')
    authorized_users_crm = fields.Many2many(comodel_name='res.users', relation='auth_crm_users')
    authorized_users_therapists = fields.Many2many(comodel_name='res.users', relation='auth_therapist_users')
    
    @api.depends('name')
    def _compute_patient(self):
        for record in self:
            search = self.env['medical.patient'].search(['|',
                                    ('partner','=',record.id),
                                    '|',
                                    ('couple_member_1.partner','=',record.id),
                                    ('couple_member_2.partner','=',record.id),
                            ])
            if search:
                record.is_patient = True
            else:
                record.is_patient = False
                
    def action_show_patient(self):
        self.ensure_one()
        patients = self.env['medical.patient'].search(['|',
                                    ('partner','=',self.id),
                                    '|',
                                    ('couple_member_1.partner','=',self.id),
                                    ('couple_member_2.partner','=',self.id),
                            ])
        result = {
            "type": "ir.actions.act_window",
            "res_model": "medical.patient",
            "domain": [('id', 'in', patients.ids)],
            "context": {"create": False},# 'default_move_type': 'in_invoice'},
            "name": _("Patients"),
            'view_mode': 'tree,form',
        }
        return result
    
    def action_create_patient(self):
        self.ensure_one()
        res = self.env['medical.patient'].create(
            {'partner': self.id,
             'state': 'initial'
                })
        return {
                'name':_("Patient"),
                'view_mode': 'form',
                'res_model': 'medical.patient',
                'res_id': res.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'domain': '[]',
            }