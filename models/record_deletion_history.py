# -*- coding: utf-8 -*- 

from odoo import models, fields,api,_


class RecordDeletionHistory(models.Model):
    _name = 'record.deletion.history'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Record deletion history"
    _order = "create_date desc"

    model_name = fields.Char(string='Model',required=True,index=True)
    model_desc = fields.Char(string='Model',help='This is used for the sake of display from the perspective of user experience',required=True)
    name = fields.Char(compute='_compute_name',store=True,index=True)
    res_id = fields.Integer(string='Record ID',required=True,index=True)
    user_id = fields.Many2one('res.users',string='User',required=True,index=True,help="The user who deleted this record")
    item_ids = fields.One2many('record.deletion.history.line','history_id')
    active = fields.Boolean(string='Active',default=True)

    @api.depends('model_desc','res_id')
    def _compute_name(self):
        for each in self:
            each.name = "%s(%s)"%(each.model_desc,each.res_id)

    def show_details(self):
        self.ensure_one()
        domain = [('history_id', 'in', self.ids)]
        history_detail = self.env['record.deletion.history.line'].search(domain,limit=1)
        return {
            'name': _('Deletion history details'),
            'view_mode': 'form',
            'views': [(self.env.ref('record_deletion_history_log.record_deletion_history_line_form_view').id, 'form')],
            'res_model': 'record.deletion.history.line',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': history_detail.id,
        }
class RecordDeletionHistoryLine(models.Model):
    _name = 'record.deletion.history.line'
    _description = "Record deletion history details"

    history_id = fields.Many2one('record.deletion.history',ondelete='cascade',required=True,index=True)
    record_details = fields.Text(string='Record details')
    record_details_html = fields.Html(string='Record details')
