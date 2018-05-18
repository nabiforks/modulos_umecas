# -*- coding: utf-8 -*-
from odoo import api, fields, models


class sup_planeacion_actividades(models.Model):
    _name = 'sup_planeacion_actividades'
    
    
    x_name = fields.Char('Planeación Actividades', required=True, readonly=True,
                         default=lambda self: 'Nuevo'
                         )
    @api.model
    def create(self, vals):
        if vals.get('x_name', 'Nuevo') == 'Nuevo':
            vals['x_name'] = self.env['ir.sequence'].next_by_code(
                'sup_planeacion_actividades') or'Nuevo'
        result = super(sup_planeacion_actividades, self).create(vals)
        return result
    x_oficio = fields.Char(
        string=u'Oficio',
    )
    x_asunto = fields.Char(
        string=u'Asunto',
    )    
    x_supervisados_ids = fields.Many2many(
        string=u'Actividades',
        comodel_name='sup_mc_scp',
    )
    x_dirigido_a = fields.Char(
        string='Dirigido a',
    )
    x_fecha_limite = fields.Date(
        string=u'Fecha límite',
    )
    
    
    
    
    
    
    
