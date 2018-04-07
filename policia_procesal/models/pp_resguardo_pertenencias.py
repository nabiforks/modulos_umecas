# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Pertenencias(models.Model):
    _name = 'pp.pertenencias'

    """name = fields.Char(
        string='Registro',
        default='Detalles'
    )"""
    fecha_hora_registro = fields.Datetime(
        string='Fecha y hora de registro',
        default=lambda self: fields.datetime.now()
    )
    fecha_hora_devolucion = fields.Datetime(
        string='Fecha y hora de devolución',
        default=lambda self: fields.datetime.now()
    )
    conducta = fields.Text(
        string='Conducta del imputado',
    )

    #==========relationship fields==========

    employee_id = fields.Many2one(
        'hr.employee',
        string='Nombre',
    )
    pertenencias_list_ids = fields.One2many(
        'pp.pertenencia_list',
        'resguardo_id',
        string='Lista de pertenencias',
    )
    custodia_id = fields.Many2one(
        'pp.custodia',
        string='Custodia',
    )
    name = fields.Many2one(#partner_id
        'res.partner',
        string=u'Nombre del imputado',
        required=True,
        #default=lambda self: self.env.context.get('partner_id'),
        ondelete='set null',
    )

