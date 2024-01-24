# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api

class AttendanceInOutGeo(models.Model):
    _name = "hr.attendance.in.out.geo"
    _description = "Attendance in and out as separate records with geolocation"
    _auto = False
    _rec_name = ''
    _order = 'check desc'
    
    id = fields.Integer()
    employee_id = fields.Many2one(comodel_name='hr.employee',readonly=True)
    is_check_in = fields.Boolean(readonly=True)
    check = fields.Datetime(readonly=True)
    latitude = fields.Float(readonly=True) 
    longitude = fields.Float(readonly=True)
    type = fields.Selection(selection=[('check_in','Check In'),('check_out','Check Out')], 
                            compute='_compute_type', readonly=True)
    date = fields.Char(compute='_compute_date', readonly=True)
    
    def name_get(self):
        result = []
        code = self._fields['type'].selection
        code_dict = dict(code)
        for record in self:
                rec_type = code_dict.get(record.type)
                result.append((record.id, '%s %s %s' % (record.employee_id.name,record.date,rec_type)))
        return result
    
    @api.depends('is_check_in')
    def _compute_type(self):
        for record in self:
            if record.is_check_in:
                record.type = 'check_in'
            else:
                record.type = 'check_out'
    
    @api.depends('check')
    def _compute_date(self):
        for record in self:
            if record.check:
                record.date = record.check.strftime('%d-%m-%Y')
            else:
                record.date = False
            
    def _query(self):
        query = """          
            select id, employee_id, true as is_check_in, check_in as check, check_in_latitude as latitude, check_in_longitude as longitude from hr_attendance
                union
            select (select count(*) from hr_attendance)+id as id, employee_id, false as is_check_in, check_out as check, check_out_latitude as latitude, check_out_longitude as longitude from hr_attendance
                where check_out is not NULL
        """
        return query
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))