# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models


class Expedientes(models.Model):
    _name = 'umc_expedientes'
    #_rec_name = 'application_number'
    #_order = "application_number desc"

    x_name = fields.Char('Expediente', required=True, readonly=True,
                         default=lambda self: 'Nuevo')

    partner_id = fields.Many2one(
        'res.partner',
        string=u'Imputado',        
        readonly=True,        
        ondelete='set null',
    )

    x_cdi_nic = fields.Char(
        string=u'CDI/NIC',
    )
    x_numero_oficio = fields.Char(
        string=u'Oficio Número',
    )

    x_fecha_inicio = fields.Datetime(
        string=u'Fecha Inicio',
        default=fields.Datetime.now,
    )

    x_delito = fields.Selection(
        string=u'Delito',
        selection=[('del1', 'ROBO (FARDERO)'), ('del2',
                                                'DETENTACION DE VEHICULO ROBADO'), ('del3', 'VIOLENCIA FAMILIAR')]
    )

    x_delito_descripcion = fields.Text(
        string=u'Descripción Delito',
    )
    
    @api.model
    def create(self, vals):
        if vals.get('x_name', 'New') == 'New':
            vals['x_name'] = self.env['ir.sequence'].next_by_code('umc_expedientes') or'New'
        print vals
        result = super(Expedientes, self).create(vals)
        return result
