from odoo import models, api, fields

class Lead(models.Model):
    _inherit='crm.lead'
    
    def _track_template(self, tracking):
        res = super()._track_template(tracking)
        lead = self[0]
        if "stage_id" in tracking and lead.stage_id.mail_template_id:
            res["stage_id"] = (
                lead.stage_id.mail_template_id,
                {
                    "auto_delete_message": True,
                    "subtype_id": self.env["ir.model.data"].xmlid_to_res_id(
                        "mail.mt_note"
                    ),
                    "email_layout_xmlid": "mail.mail_notification_light",
                },
            )
        return res
        
    @api.model_create_multi
    def create(self, vals_list):
        Partner = self.env['res.partner']
        for vals in vals_list:
            if 'user_id' in vals and 'partner_id' in vals:
                if vals['user_id'] and vals['user_id'] not in Partner.browse(vals['partner_id']).authorized_users_crm.ids:
                    Partner.browse(vals['partner_id']).write({'authorized_users_crm': [(4,vals['user_id'],0)]})
        return super(Lead, self).create(vals_list)
    
    def write(self, vals):
        Partner = self.env['res.partner']
        for record in self:
            if not record.user_id or not record.partner_id:
                user_id = record.user_id.id or vals.get('user_id',False)
                partner_id = record.partner_id.id or vals.get('partner_id',False)
                if user_id and partner_id:
                    if user_id not in Partner.browse(partner_id).authorized_users_crm.ids:
                        Partner.browse(partner_id).write({'authorized_users_crm': [(4,user_id,0)]})
            else:
                record._reset_partner_auth_users(vals=vals)
                    
        return super(Lead, self).write(vals)

    def unlink(self):
        for record in self:
            record._reset_partner_auth_users()
        return super(Lead, self).unlink()
    
    def _reset_partner_auth_users(self, vals=False):
        ''' Compute authorized users for partner excluding self and reset them '''
        Partner = self.env['res.partner']
        users = self.search([('partner_id','=',self.partner_id.id),('id','!=',self.id)]).mapped('user_id')
        if vals and vals.get('user_id',False):
            users |= vals['user_id']
        if not users:
            Partner.browse(self.partner_id.id).sudo().write({'authorized_users_crm': False})
        else:
            Partner.browse(self.partner_id.id).sudo().write({'authorized_users_crm': [(6,0,users.ids)]})

class Stage(models.Model):
    _inherit = "crm.stage"
        
    mail_template_id = fields.Many2one(
        comodel_name="mail.template",
        string="Email Template",
        domain=[("model", "=", "crm.lead")],
        help="If set an email will be sent to the "
        "customer when the opportunity"
        "reaches this step.",
    )    