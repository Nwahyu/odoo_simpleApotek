from odoo import api, fields, models

class meeting(models.Model):
    _name = 'h.meetingdetail'
    _description = 'detail meeting'

    name = fields.Char('name')
    detail = fields.Text('detail')