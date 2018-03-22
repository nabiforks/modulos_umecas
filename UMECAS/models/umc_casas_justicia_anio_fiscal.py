from odoo import models, api, fields

class umc_casas_justicia_anio_fiscal(models.Model):
    _name = 'umc_casas_justicia_anio_fiscal'
    company_id = fields.One2many('res.company', string='Casa de justicia', required=True, ondelete='set null')
    anio = fields.Integer(string='Año fiscal', required=True)
    secuencial = fields.Integer(string='Contador', default=0)
