from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    create_partner_from_answers = fields.Boolean(
        help="Create partner from answers.",
    )
    partner_tags = fields.Many2many(
        comodel_name="res.partner.category",
        help="Add these tags to partner created when survey is submitted",
    )
    phone_question = fields.Many2one(comodel_name="survey.question",
                domain="[('question_type','=','char_box'),('survey_id','=',id),('save_as_email','=',False),('save_as_nickname','=',False)]",
        help="Question which answer should be used as partner phone.")


    @api.onchange('create_partner_from_answers')
    def _onchange_create_partner_from_answers(self):
        if self.create_partner_from_answers and \
                not self._origin.create_partner_from_answers and \
                ( not True in self.question_ids.mapped('save_as_email') or \
                not True in self.question_ids.mapped('save_as_nickname')):
            self.add_answers_to_patient = False
            raise UserError(_('Ther should be one question for the user email and one for the user name (nickname will be used).'))