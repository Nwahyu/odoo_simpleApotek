from odoo import api, fields, models
from odoo.exceptions import ValidationError


class kamar(models.Model):
    _name = 'h.kamar'
    _description = 'list kamar'
    _rec_name = 'nama_kamar'

    nama_kamar = fields.Char('nama_kamar', required=True)
    kapasitas = fields.Integer('kapasitas', default='1')
    penghuni_ids = fields.One2many('h.isikamar', 'kamar_id', string='penghuni')

    # @api.model
    # def create(self, vals_list):
    #     pes = super(kamar, self).create(vals_list)
    #     # cek isi penghuni kamar jika null
    #     looh = self.env['h.isikamar'].search([])
    #     print('c ini awal :',looh)
    #     for re in looh:
    #         print('c ini isi :',re.pasien_id.id)
    #         if re.pasien_id.id == False:
    #             raise ValidationError('ada kesalahan pada list penghuni kamar.')
    #     print('pjnjn',len(self.penghuni_ids))
    #     return pes

    # @api.model
    def write(self, vals):
        pes = super(kamar, self).write(vals)
        # cek isi kamar jika null
        for g in self.penghuni_ids:
            if g.pasien_id.id == False:
                raise ValidationError('ada kesalahan pada list penghuni kamar.')
        return pes


    @api.onchange('penghuni_ids')
    def _onchange_penghuni_ids(self):
        if len(self.penghuni_ids) > self.kapasitas:
            raise ValidationError('kapasitas kamar penuh')

        ror = self.env['h.isikamar'].search([]).mapped('pasien_id.name')
        if len(self.penghuni_ids) > 0:
            if self.penghuni_ids[-1].pasien_id.name in ror:
                raise ValidationError('pasien sudah berada di kamar lainnya.')

            for g in self.penghuni_ids:
                g.pasien_id.kamar = self.nama_kamar

        if len(self.penghuni_ids) > 1:              
            if self.penghuni_ids[-2].pasien_id.id == False:
                raise ValidationError('list pasien inap ada yang kosong')
    
    @api.constrains('penghuni_ids')
    def const_penghuni_ids(self):
        pasien = self.env['h.pasien'].search([])
        list_isi = self.env['h.isikamar'].search([]).mapped('pasien_id')
        for r in pasien:
            if r not in list_isi :
                r.kamar = False

class isi_kamar(models.Model):
    _name = 'h.isikamar'
    _description = 'list pasien rawat inap'
    _rec_name = 'pasien_id'

    kamar_id = fields.Many2one('h.kamar', string='kamar', readonly=True, ondelete='cascade')
    pasien_id = fields.Many2one('h.pasien', string='pasien')
    
    # @api.onchange('pasien_id')
    # def _onchange_pasien_id(self):
    #     print(self)