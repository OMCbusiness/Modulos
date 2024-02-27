from odoo import models, fields

class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"
    
    state = fields.Selection([
        ('new', 'Not started yet'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed')], string='Status', default='in_progress', readonly=True)
    
    def _mark_done(self):
        """Prepare and add the data to the patient"""
        super(SurveyUserInput, self)._mark_done()
        if not self.survey_id.add_answers_to_patient:
            return
        patient = self._get_patient()
        if patient:
            patient.write({'patient_provided_info': self._prepare_patient_data(patient)})
        # self._create_opportunity_post_process()
        return
    
    def _get_patient(self):
#        email_question = self.survey_id.email_question
#        lines = self.user_input_line_ids.filtered(lambda x: x.question_id == email_question)
#        if lines:
#            email = lines[0].value_char_box
        patients = self.env['medical.patient'].search([('partner.email','=',self.email)])
        if patients:
            if self.survey_id.is_for_couple:
                couple = patients[0].couple
                return couple
            else:
                return patients[0]
        else:
            return False
        
    def _prepare_patient_data(self, patient):
        date = self.end_datetime.date()
        data = ''     
        for line in self.user_input_line_ids:
            question_string = line.question_id.title
            if line.question_id.save_as_email:
                continue
            if line.answer_type == 'text_box':
                answer_string = line.value_text_box
            elif line.answer_type == 'char_box':
                answer_string = line.value_char_box
            elif line.answer_type == 'numerical_box':
                answer_string = line.value_numerical_box
            elif line.answer_type == 'date':
                answer_string = line.value_date
            elif line.answer_type == 'datetime':
                answer_string = line.value_datetime
            elif line.answer_type == 'suggestion':
                answer_string = line.suggested_answer_id.value
            data += '<p>'+question_string+': '+answer_string+'</p>'
        return [(0,0,{'date':date, 'patient': patient.id, 'data':data})]
    
            