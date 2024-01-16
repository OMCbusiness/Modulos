from odoo import models, fields, api

class TherapistCalendar(models.Model):
    _name = 'medical.therapist.calendar'
    _inherit = 'resource.calendar'
    _description = 'Therapists availability'
    
    therapist = fields.Many2one(comodel_name='medical.therapist', ondelete='cascade')
    availability_ids = fields.One2many(
        'medical.therapist.calendar.availability', 'calendar_id', 'Working Time',)
            
class TherapistCalendarAttendance(models.Model):
    _name = 'medical.therapist.calendar.availability'
    _inherit = "resource.calendar.attendance"
    _description = "Therapists attendance"

    calendar_id = fields.Many2one("medical.therapist.calendar", string="Therapist's Calendar", required=True, ondelete='cascade')