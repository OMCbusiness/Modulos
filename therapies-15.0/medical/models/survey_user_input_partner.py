from odoo import models

class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"
    
    def _mark_done(self):
        """Create contact and add it to opportunity"""
        super(SurveyUserInput, self)._mark_done()
        if not self.survey_id.create_partner_from_answers or not self.opportunity_id:
            return
        phone_question = self.survey_id.phone_question
        phone = False
        for line in self.user_input_line_ids:
            if line.question_id == phone_question:
                phone = line.value_char_box
            if line.question_id.save_as_email:
                email = line.value_char_box
            if line.question_id.save_as_nickname:
                name = line.value_char_box
        partner = self.env['res.partner'].search([('email','=',email)])
        if not partner:
            partner = self.env['res.partner'].create({
                    'email': email,
                    'name': name,
                    'phone': phone,
                })
        self.opportunity_id.partner_id = partner.id
        # self._create_opportunity_post_process()
        return