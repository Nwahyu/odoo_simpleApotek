# todo list

# create meeting / kunjugan
# bug fix multi warehouse amount barang
# diagram pada dashboard
# short name trx
# bikin report rujukan
# perbaikan error penambahan pasien

# selesai
# betulin formview penjualan
# person
# rekam medis
# custom name -> done tinggal gabungin
#ambil data rekam medis selesai kirim ke daftar transaksi with depend

from odoo import api,fields,models

class dokter(models.Model):
    _name = 'h.dokter'
    _description = 'list dokter'

    name = fields.Char('name')
    alamat = fields.Char('alamat')
    no_telp = fields.Char('no_telp')
    email = fields.Char('email')
    is_dokter = fields.Boolean('is_dokter')
    tipemedis_id = fields.Many2one('h.tipemedis', string='tipemedis', help='isi ini ada di menu backdoor > tipe medis')

    date_s = fields.Date('date_s')
    date_o = fields.Date('date_o')