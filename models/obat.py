from datetime import datetime
from email.policy import default
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class obat(models.Model):
    _name = 'h.obat'
    _inherit = ["mail.activity.mixin","mail.thread"]
    _description = 'list obat by bj'

    name = fields.Char('nama obat')
    stok = fields.Integer('stok', tracking=True)
    harga_jual = fields.Integer('harga jual')
    admin_id = fields.Many2one('res.users', string='admin', default=lambda self: self.env.user.id)
    tmpt_obat_id = fields.Many2one('h.tempatobat', string='tmpt_obat')
    history_ids = fields.One2many('h.history', 'obat_id', string='history')
    history_reverse_ids = fields.One2many('h.history', 'obat_id', string='history')

    @api.constrains('name','stok','harga_jual','tmpt_obat_id')
    def _onchange_history(self):
        self.env['h.history'].create({
            'obat_id':self.id,
            'name': self.name,
            'stok': self.stok,
            'harga_jual': self.harga_jual,
            'admin_id': self.admin_id.id,
            'tmpt_obat_id': self.tmpt_obat_id.id
            })
        if len(self.history_ids) > 12 :
            self.history_ids[0].unlink()
            
    def button_cek_active(self):
        seh = self.env['h.tempatobat']

    def button_wizzard_stok(self):
        pass

class tempat_obat(models.Model):
    _name = 'h.tempatobat'
    _description = 'tempat obat'

    name = fields.Char('nama tempat')
    tgl_masuk = fields.Datetime('tanggal masuk', default=datetime.now())
    catatan = fields.Text('catatan')

class history(models.Model):
    _name = 'h.history'
    _description = 'history obat'

    obat_id = fields.Many2one('h.obat', string='obat', ondelete='cascade')
    name = fields.Char('nama obat')
    stok = fields.Integer('stok')
    harga_jual = fields.Integer('harga jual')
    admin_id = fields.Many2one('res.users', string='admin')
    tmpt_obat_id = fields.Many2one('h.tempatobat', string='tmpt_obat')