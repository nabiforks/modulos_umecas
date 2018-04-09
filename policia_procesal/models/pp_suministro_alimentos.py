# -*- coding: utf-8 -*-

from odoo import fields, models

class SuministroAlimentos(models.Model):
    _name = 'pp.suministro'

    """name = fields.Char(
        string='Detalles',
        default='Detalles'
    )"""
    conducta = fields.Text(
        string='Conducta del imputado',
    )

    #==========RELATIONSHIP FIELDS==========
    name = fields.Many2one(
        'res.partner',
        string='Nombre del imputado',
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Nombre',
    )
    alimentos_list = fields.One2many(
        'pp.suministro_list',
        'suministro_id',
        string='Lista',
    )
    """partner_id = fields.Many2one(
        'res.partner',
        string=u'Nombre del imputado',
        required=True,
        default=lambda self: self.env.context.get('partner_id'),
        ondelete='set null',
    )"""

    #==========RELATED==========
    """nombre_completo = fields.Char(
        related='partner_id.display_name',
        string='Nombre del imputado',
    )"""
    #Agrgar campo de 'conducta'


