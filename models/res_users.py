# -*- coding: utf-8 -*-

from odoo import models, fields,_
from odoo.exceptions import UserError

class Groups(models.Model):
    _inherit = "res.groups"


    #def write(self, vals):
        # Prevent updating the record_deletion_history group by adding or removing users,this group is fixed
    #    if self.env.ref('record_deletion_history_log.group_record_deletion_log').id in self.ids:
    #        raise UserError(_("Can not update a group record_deletion_history_log"))
    #    return super(Groups,self).write(vals)