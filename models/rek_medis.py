from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import ValidationError


class rek_medis(models.Model):
    _name = 'h.rekmedis'
    _description = 'ini rekam medis'
    _rec_name = 'pasien_id'

    no_antrian_id = fields.Many2one('h.idp', string='no_antrian', required=True)
    no_antrian = fields.Integer('no_antrian')
    pasien_id = fields.Many2one('h.pasien', string='pasien', required=True, domain="[('is_pasien','=','True')]")
    dokter_id = fields.Many2one('h.dokter', string='dokter', required=True, domain="[('is_dokter','=','True')]")
    catatan = fields.Text('catatan')
    dpenjualan_ids = fields.One2many('h.dpenjualan', 'rekmedis_id', string='dpenjualan')
    tgll = fields.Datetime('tgll', default=datetime.now())
    tipemedis_id = fields.Many2one('h.tipemedis', string='tipe medis', related="dokter_id.tipemedis_id")
    
    state = fields.Selection([
        ('antri', 'Antri'),
        ('cek', 'Medical Check Up'),
        ('berobat', 'Berobat'),
        ('selesai', 'Selesai'),
        ('utang','proses pembayaran')
    ], string='Status', default='antri', required=True)
    state1 = fields.Selection(related='state')
    
    kekeyi = fields.Boolean('kekeyi')

    #dana keuangan pasien
    @api.onchange('pasien_id')
    def _onchange_data(self):
        if self.pasien_id.data < 1 :
            self.kekeyi = True
        else: self.kekeyi = False

    @api.model
    def create(self, vals):
        sup = super(rek_medis, self).create(vals)
        c = sum(self.env['h.dpenjualan'].search([('rekmedis_id', '=', sup.id)]).mapped('obat_id.stok'))
        a = sum(self.env['h.dpenjualan'].search([('rekmedis_id', '=', sup.id)]).mapped('obat_id.harga_jual'))
        b = self.env['h.idp'].search([('name', '=', sup.no_antrian_id.name)])
        if sup.no_antrian_id:
            sup.no_antrian_id.antrian += 1
        sup.no_antrian = b.antrian
        return sup

    @api.ondelete(at_uninstall=True)
    def delte(self):
        for z in self:
            aa = z.env['h.penjualan'].search([('rekmedis_id','=',z.id)])
            if aa:
                raise ValidationError('ini merupakan transaksi selesai')
            a = []
            for c in z:
                a = c.env['h.dpenjualan'].search([('rekmedis_id', '=', c.id)])
                for d in a:
                    d.obat_id.stok += d.qty

    def write(self, vals):
        for z in self:
            a = self.env['h.dpenjualan'].search([('rekmedis_id', '=', z.id)])
            for data in a:
                data.obat_id.stok += data.qty
        sup = super(rek_medis, self).write(vals)
        for z in self:
            b = self.env['h.dpenjualan'].search([('rekmedis_id', '=', z.id)])
            for data in b:
                if data in a:
                    data.obat_id.stok -= data.qty
                else: pass
        return sup

    def button_state_next(self):
        if self.state == 'antri':
            self.state = 'cek'
        elif self.state == 'cek':
            self.state = 'berobat'
        elif self.state == 'berobat':
            if self.pasien_id.tipe_pasien == 'bpjs':
                self.state = 'selesai'
                self.env['h.penjualan'].sudo().create({
                    'rekmedis_id' : self.id,
                    'name' : 'rek medis / '+str(self.no_antrian)+' / '+str(self.pasien_id.name)})
            else: self.state = 'utang'
        # elif self.state == 'selesai':
        #     self.state = 'utang'
        elif self.state == 'utang':
            self.env['h.penjualan'].sudo().create({
                'rekmedis_id' : self.id,
                'name' : self.pasien_id})
            self.state = 'selesai'

    def button_state_prev(self):
        if self.state == 'antri':
            self.state = 'antri'
        elif self.state == 'cek':
            self.state = 'antri'
        elif self.state == 'berobat':
            self.state = 'cek'
        elif self.state == 'selesai':
            self.state = 'berobat'
        elif self.state == 'utang':
            self.state = 'selesai'


class dpenjualan(models.Model):
    _name = 'h.dpenjualan'
    _description =  'detail penjualan hooh'
    _rec_name = 'rekmedis_id'

    penjualan_id = fields.Many2one('h.penjualan', string='penjualan')
    rekmedis_id = fields.Many2one('h.rekmedis', string='rekmedis', ondelete='cascade')
    
    obat_id = fields.Many2one('h.obat', string='obat', required=True)
    qty = fields.Integer('qty', default=1, required=True)
    sub_total = fields.Integer(compute='_compute_sub_total', string='sub_total')

    harga_satuan = fields.Integer('harga_satuan')
    
    @api.depends('qty','obat_id')
    def _compute_sub_total(self):
        for z in self:
            z.sub_total = z.obat_id.harga_jual * z.qty

    #add penjualan
    @api.model
    def create(self, vals_list):
        print(f'-'*20)
        sup = super(dpenjualan, self).create(vals_list)
        a = self.env['h.obat'].search([('id', '=', sup.obat_id.id)])
        print(a)
        a.stok -= sup.qty
        return sup

    #cek qty per barang
    @api.constrains('qty')
    def cek_qty(self):
        for z in self:
            if z.qty < 1 :
                raise ValidationError('qty < 1')
            if z.obat_id.stok < z.qty :
                raise ValidationError('qty luber')



class id_penjualan(models.Model):
    _name = 'h.idp'
    _description = 'kumpulan id'

    penjualan_ids = fields.One2many('h.rekmedis', 'no_antrian_id', string='penjualan')
    name = fields.Char('name')
    antrian = fields.Integer('nomor antrian')


class tipe_medis(models.Model):
    _name = 'h.tipemedis'
    _description = 'list tipe medis'

    name = fields.Char('name')
    # dokter_id = fields.Many2one('h.dokter', string='dokter')
    dokter_ids = fields.One2many('h.dokter', 'tipemedis_id', string='dokter')
    tipemedis = fields.Char('tipemedis')