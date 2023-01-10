from odoo import api,fields,models


class rujukan(models.Model):
    _name = "h.rujukan"
    _description = "list rujukan"

    pasien_id = fields.Many2one('h.pasien', string='pasien')
    rekmedis_id = fields.Many2one('h.rekmedis', string='rekmedis', domain="[('pasien_id','=',self.pasien_id.id)]")
    name = fields.Char(compute='_compute_name', string='name')

    @api.depends('pasien_id')
    def _compute_name(self):
        self.name = self.pasien_id.name
        ress = self.env['h.rekmedis'].search([('pasien_id','=',self.pasien_id.id)])
        print(ress)