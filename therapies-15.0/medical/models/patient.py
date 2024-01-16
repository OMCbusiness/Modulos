from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Patient(models.Model):
    _name = 'medical.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Model to manage patient information.'
    
    partner = fields.Many2one(comodel_name='res.partner', ondelete='cascade')
    name = fields.Char()
    therapist = fields.Many2one(comodel_name='medical.therapist', ondelete='set null')
    clinical_information = fields.Html()
    
    is_couple = fields.Boolean(default=False)
    couple_member_1 = fields.Many2one(comodel_name='medical.patient', domain=[('couple','=',False)], ondelete='restrict')
    couple_member_2 = fields.Many2one(comodel_name='medical.patient', domain=[('couple','=',False)], ondelete='restrict')
    
    couple = fields.Many2one(comodel_name='medical.patient', compute='_compute_couple')
    couple_counterpart = fields.Many2one(comodel_name='medical.patient', compute='_compute_couple')
    patient_provided_info = fields.One2many(comodel_name='medical.patient.data', inverse_name='patient', readonly=True)
    tags = fields.Many2many(comodel_name='medical.patient.tag')
    therapy = fields.Many2one(comodel_name='medical.therapist.therapy', ondelete='restrict', domain="[('therapist','=',therapist)]")
    state = fields.Selection(selection=[('initial','Initial'),('active','Active'),('stand_by','Stand by'),('finished','Finished')], default='initial', )
    
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id,record.name if record.is_couple else record.partner.name))
        return result
            
    @api.constrains('is_couple','couple_members','partner')
    def _couple_constraint(self):
        for record in self:
            if record.is_couple and (not record.couple_member_1 or not record.couple_member_2):
                raise UserError(_('One couple should have two members'))
            if record.is_couple and record.partner:
                raise UserError(_('A couple cannot be related to a partner, instead it should have two members.'))
            if not record.is_couple and not record.partner:
                raise UserError(_('A patient must be a person or a couple'))
    
    @api.constrains('partner')
    def _partner_constraint(self):
        for record in self:
            if record.partner.is_company:
                raise UserError(_('A company cannot be a patient.'))
            
    _sql_constraints = [
        ('patient_partner_unique', 'UNIQUE(partner)',
         _('Only one patient for every partner is allowed.')),
    ]
            
    @api.depends('couple')
    def _compute_couple(self):
        for record in self:
            couple = self.env['medical.patient'].search(['|',('couple_member_1','=',record.id),('couple_member_2','=',record.id)])
            if couple:
                record.couple = couple[0]
            else:
                record.couple = False
            if couple:
                if record.couple.couple_member_1 == record:
                    record.couple_counterpart = record.couple.couple_member_2
                else:
                    record.couple_counterpart = record.couple.couple_member_1
            else:
                record.couple_counterpart = False
                
    def _add_therapist_user(self, therapist_id):
        user_ids = self.env['medical.therapist'].browse(therapist_id).partner.user_ids.ids
        for user_id in user_ids:
            if user_id not in self.partner.authorized_users_therapists.ids:
                self.partner.write({'authorized_users_therapists': [(4,user_id,0)]})
            
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'therapist' in vals and 'partner' in vals:
                if vals.get('is_couple',False):
                    self.browse(vals['couple_member_1'])._add_therapist_user(vals['therapist'])
                    self.browse(vals['couple_member_2'])._add_therapist_user(vals['therapist'])
                else:
                    self._add_therapist_user(vals['therapist'])
        return super(Patient, self).create(vals_list)
    
    def write(self, vals):
        for record in self:
            if not record.therapist or not record.partner:
                therapist_id = record.therapist.id or vals.get('therapist',False)
                partner_id = record.partner.id or vals.get('partner',False)
                is_couple = record.is_couple or vals.get('is_couple',False)
                if therapist_id and partner_id:
                    if is_couple:
                        record.browse(vals['couple_member_1'])._add_therapist_user(vals['therapist'])
                        record.browse(vals['couple_member_1'])._add_therapist_user(vals['therapist'])
                    else:
                        record._add_therapist_user(vals['therapist'])
            else:
                record._reset_partner_auth_users(vals=vals)
        return super(Patient, self).write(vals)

    def unlink(self):
        for record in self:
            record._reset_partner_auth_users()
        return super(Patient, self).unlink()
                 
    def _reset_partner_auth_users(self, vals=False):
        ''' Compute authorized users for partner excluding self and reset them '''
        if self.is_couple:
            if not self.therapist == self.browse(self.couple_member_1).therapist:
                self.couple_member_1.partner.write({'authorized_users_therapists': [(3,user_id,0) for user_id in self.therapist.partner.user_ids.ids]})
            if not self.therapist == self.browse(self.couple_member_2).therapist:
                self.couple_member_2.partner.write({'authorized_users_therapists': [(3,user_id,0) for user_id in self.therapist.partner.user_ids.ids]})
        else:
            self.partner.write({'authorized_users_therapists': False})
        if vals and vals.get('therapist',False):
            is_couple = self.is_couple or vals.get('is_couple',False)
            if is_couple:
                self.browse(vals['couple_member_1'])._add_therapist_user(vals['therapist'])
                self.browse(vals['couple_member_1'])._add_therapist_user(vals['therapist'])
            else:
                self._add_therapist_user(vals['therapist'])
        
class PatientProvidedDataself(models.Model):
    _name = 'medical.patient.data'
    _description = 'Data provided by the patient directly'
    
    patient = fields.Many2one(comodel_name='medical.patient')
    date = fields.Date()
    data = fields.Html(string='Information from patient')