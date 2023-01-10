from odoo import api,fields,models
from odoo.exceptions import ValidationError


class pasien(models.Model):
    _name = 'h.pasien'
    _description = 'list pasien'

    name = fields.Char('name')
    alamat = fields.Char('alamat')
    no_telp = fields.Char('no_telp')
    email = fields.Char('email')
    is_pasien = fields.Boolean('is_pasien')
    tipe_pasien = fields.Selection([
        ('bpjs', 'BPJS'),
        ('non','Non BPJS') 
    ], string='tipe_pasien', default='non')

    data = fields.Float('data')

    kamar = fields.Char('kamar')