# -*- coding: utf-8 -*- 

from odoo import models, fields


class RecordDeletionHistory(models.Model):
    _name = 'record.deletion.history'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Record deletion history"
    _order = "create_date desc"

    model_name = fields.Char(string='Model',required=True,index=True)
    model_desc = fields.Char(string='Model',help='This is used for the sake of display from the perspective of user experience')
    res_id = fields.Integer(string='Record ID',required=True)
    user_id = fields.Many2one('res.users',string='User',required=True,index=True,help="The user who deleted this record")
    active = fields.Boolean(string='Active')
