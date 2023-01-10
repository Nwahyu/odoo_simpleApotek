from datetime import datetime
from odoo import api,fields,models

class kunjungan(models.Model):
    _name = "h.kunjungan"
    _description = "list kunjngan"

    name = fields.Char('name')
    dokter_id = fields.Many2one('h.dokter', string='dokter')
    pasien_id = fields.Many2one('h.pasien', string='pasien')
    inipas = fields.Char('inipas')
    tipemedis_id = fields.Many2one('h.tipemedis', string='tipemedis')
    date_start = fields.Date('date start')
    date_end = fields.Datetime('date end')

    # @api.onchange('dokter_id')
    # def _onchange_dokter_id(self):
    #     print(self.tk,type(self.tk))
    #     print(self.tgll,type(self.tgll))
    #     print(self.env.context.get('active_ids', []))
    #     print(self.env['h.rekmedis'].search([('state','=','selesai')]))