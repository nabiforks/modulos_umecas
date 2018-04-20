# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, date
from odoo import api, fields, models


class sup_mc_scp(models.Model):
    _name = 'sup_mc_scp'

    x_name = fields.Char('Registro', required=True, readonly=True,
                         default=lambda self: 'Nuevo'
                         )
    @api.model
    def create(self, vals):
        if vals.get('x_name', 'Nuevo') == 'Nuevo':
            vals['x_name'] = self.env['ir.sequence'].next_by_code(
                'sup_mc_scp') or'Nuevo'
        result = super(sup_mc_scp, self).create(vals)
        return result
    
    x_imputado_id = fields.Many2one(
        string=u'Imputado',
        comodel_name='res.partner',
        ondelete='restrict',        
        readonly=True,        
    )
    x_resolucion = fields.Selection(
        string=u'Resolución',
        selection=[('mc', 'MC'), ('scp', 'SCP')]
    )
    x_numero_oficio = fields.Char(
        string=u'Oficio número',
    )
    
    x_inicia = fields.Date(
        string=u'Fecha de Inicio',
        default=fields.Date.context_today,
    )
    x_finaliza = fields.Date(
        string=u'Fecha de Término',
        default=fields.Date.context_today,
    )
    x_tiempo = fields.Char(
        string=u'Tiempo',
    )
        
    x_foja = fields.Integer(
        string=u'Foja',
    )
    x_libro = fields.Char(
        string=u'Libro',
    )
    #/////////////////////////////////////////////
    #/////////////////////////////////////////////
    #/////////////////////////////////////////////
    
    x_expediente_id = fields.Many2one(
        string=u'Expediente ID',
        comodel_name='umc_expedientes',
        ondelete='cascade',        
        readonly=True,        
    )
    
    
    
    
    
    
    
    
    

    