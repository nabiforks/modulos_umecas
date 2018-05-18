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
    
    x_cargo = fields.Text(
        string='Cargo',
        default='DIRECTOR DE MEDIDAS CAUTELARES Y POLICÍA PROCESAL'
    )
    x_observaciones = fields.Text(
        string='Observaciones',
    )
    x_parrafo = fields.Text(
        string='Presente',
        default=lambda self:self.parrafo_default()
    )
    
    def parrafo_default(self):
        text = "De conformidad con los artículos 153, 154, 155, 156, 157, 164, 174, 177, 182 y 195 del Código Nacional de Procedimeintos Penales; 69 y 70 de la ley de Ejecución de Medidas Cautelares y Sanciones Penales; 17 fracciones XIII y XIV de la Ley de Seguridad Pública, todas para el Estado de Puebla, en cumplimiento a los planes de supervisión de las Medidas Cautelares y Condiciones de Suspensión Condicional, elaborados por la responsable del Área de Evaluación de Riesgos y Suspensión de Medidas Cautelares de la Región Judicial Centro, se debe realizar lo siguiente:"
        return text