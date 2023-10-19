# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import UserError
import json
import logging
_logger = logging.getLogger(__name__)


class BaseModelExtended(models.AbstractModel):
    _name = "base.model.extended"

    def _register_hook(self):
        origin_unlink = models.BaseModel.unlink

        def _get_record_details(self):
            # we have to generate two types of dictionary,json_record_details will be stored as key,value so that it can be used later as data source
            # and can be formatted to whatever format type we want(HTML,XML,PDF...),
            # display_record_details will be used as already formatted data that can be displayed directly
            # You can notice that we have generate the two types in the same method hence we have to return the both in method return,
            # although it can be seen as bad practice from code readability perspective,we have take this choice so that we don't need to do two loops
            # in the same datastructure only for change the type of returned data
            json_record_details = {}
            display_record_details = {'_rec_name':getattr(self,getattr(self,'_rec_name'),False)}
            for field_name, field in self._fields.items():
                json_record_details.update({field_name:getattr(self, field_name)})
                display_record_details.update({field.string: getattr(self, field_name)})
            return json.dumps(json_record_details, indent = 4,default=str),display_record_details

        def _convert_to_html(display_record_details):
            html = "<table class='table table-bordered'>\n"
            if display_record_details.get('_rec_name'):
                html += _("<center><h1>%s</h1></center>\n")%display_record_details.get('_rec_name')
            html += _("<tr><th><h3>Field</h3></th><th><h3>Value</h3></th></tr>\n")
            # remove the added _rec_name key before looping
            display_record_details.pop('_rec_name')
            for field_name, field_value in display_record_details.items():
                html += "<tr><td>%s</td><td>%s</td></tr>"%(field_name,field_value)
            html += "</table>\n"
            return html

        def _prepared_record_to_remove(self):
            records_to_remove = []
            for each in self:
                record_details,display_record_details = _get_record_details(self)
                record_details_html = _convert_to_html(display_record_details)
                records_to_remove.append({
                    'model_name': each._name,
                    'model_desc': each._description,
                    'res_id': each.id,
                    'user_id': each.env.user.id,
                    'item_ids':[(0,0,{'record_details': record_details,'record_details_html':record_details_html})]
                })
            return records_to_remove

        def make_unlink(self):
            # in case of issue in the added behaviour,this should not block the removing processes
            try:
                records_to_create = _prepared_record_to_remove(self)
                if records_to_create:
                    self.env['record.deletion.history'].sudo().create(records_to_create)
            except Exception as e:
                _logger.exception('Something went wrong when tracking the removing process %s !'%e)
            return origin_unlink(self)

        models.BaseModel.unlink = make_unlink

    # def write(self, vals):
    # Prevent updating the record_deletion_history group by adding or removing users,this group is fixed
    #    if self.env.ref('record_deletion_history_log.group_record_deletion_log').id in self.ids:
    #        raise UserError(_("Can not update a group record_deletion_history_log"))
    #    return super(Groups,self).write(vals)
