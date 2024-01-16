from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    add_answers_to_patient = fields.Boolean(
        help="Add survey answers to patient information",
    )
    patient_tag_ids = fields.Many2many(
        comodel_name="medical.patient.tag",
        help="Add these tags to patient when survey is submitted",
    )
#    email_question = fields.Many2one(comodel_name="survey.question",
#                domain="[('question_type','=','char_box'),('survey_id','=',id)]",
#        help="Question which answer should allow to identify the patient by his/her email.")
    is_for_couple = fields.Boolean(
        help="If marked means that the answers will be added to the couple patient related.")

    @api.onchange('add_answers_to_patient')
    def _onchange_add_answers_to_patient(self):
        if self.add_answers_to_patient and \
                not self._origin.add_answers_to_patient and \
                not True in self.question_ids.mapped('save_as_email'):
            self.add_answers_to_patient = False
            raise UserError(_('Ther should be one question for the user email.'))