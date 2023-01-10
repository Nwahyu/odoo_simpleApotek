from datetime import datetime
from email.policy import default
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class penjualan(models.Model):
    _name = 'h.penjualan'
    _description = 'hooh penjualan'


    name = fields.Char('name')


    rekmedis_id = fields.Many2one('h.rekmedis', string='rekmedis', readonly=True)

    no_antrian = fields.Integer('no_antrian', related='rekmedis_id.no_antrian')
    pasien_id = fields.Many2one('h.pasien', string='pasien', related='rekmedis_id.pasien_id')
    catatan = fields.Text('catatan', related='rekmedis_id.catatan')
    tgll = fields.Datetime('tgll', related='rekmedis_id.tgll')
    tipemedis_id = fields.Many2one('h.tipemedis', string='tipe medis', related='rekmedis_id.tipemedis_id')
    dpenjualan_ids = fields.One2many('h.dpenjualan','penjualan_id',string='tes_dpenjualan', related='rekmedis_id.dpenjualan_ids')

    is_buyer = fields.Boolean('is_buyer')

    catatan1 = fields.Text('catatan')
    tgll1 = fields.Datetime('tgll', default=datetime.now())
    idi = fields.Char('idi', readonly=True)
    dpenjualan_ids1 = fields.One2many('h.dpenjualan', 'penjualan_id', string='dpenjualan')
    
    # def create(self, vals_list):
    #     aa = super().create(vals_list)
    #     self.name = 'apotek'+
    #     return aa

    @api.onchange('is_buyer','tgll1','idi','dpenjualan_ids1')
    def _onchange_is_buyer(self):
        self.tgll = self.tgll1
        self.dpenjualan_ids = self.dpenjualan_ids1

    @api.ondelete(at_uninstall=True)
    def delete(self):
        # confirm = ' you sure?'
        for dat in self:
            aa = dat.env['h.dpenjualan'].search([('penjualan_id','=',dat.id)])
            for re in aa:
                print(re)
                re.obat_id.stok += re.qty