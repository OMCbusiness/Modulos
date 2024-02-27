from odoo import models, fields, api

class Therapist(models.Model):
    _name = 'medical.therapist'
    _inherits = {'res.partner': 'partner'}
    _description = 'Model to manage therapist information.'
    
    partner = fields.Many2one(comodel_name='res.partner', required=True, ondelete='restrict', domain="[('user_ids','!=',False)]")
#    agenda
    therapies = fields.Many2many(comodel_name='medical.therapist.therapy', relation='therapy_therapist_rel', column1='therapy', column2='therapist')
    patients = fields.One2many(comodel_name='medical.patient', inverse_name='therapist')
    description = fields.Text()
    availability = fields.Many2one(comodel_name='medical.therapist.calendar', readonly=True)
    
    @api.model
    def create(self,vals):
        name = self.env['res.partner'].browse(vals['partner']).name
        calendar = self.env['medical.therapist.calendar'].create({
            'name': 'Disponibilidad %s' % name,
            'therapist': self.id})
        vals['availability'] = calendar.id
        return super(Therapist, self).create(vals)
    
class Therapy(models.Model):
    _name = 'medical.therapist.therapy'
    _description = 'Type of therapy'
    
    name = fields.Char(required=True)
    description = fields.Text()
    sequence = fields.Integer(string = "Sequence")
    therapist = fields.Many2many(comodel_name='medical.therapist',  relation='therapy_therapist_rel', column2='therapy', column1='therapist')
    