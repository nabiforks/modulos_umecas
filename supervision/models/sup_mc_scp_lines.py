# -*- coding: utf-8 -*-
from odoo import api, fields, models


class sup_mc_lines(models.Model):
    _name = 'sup_mc_lines'

    
    name = fields.Many2one(
        string=u'MC',
        comodel_name='sup_mc',
        ondelete='set null',        
        required=True,        
    )  
    codigo = fields.Char(
        string='Código',        
        related='name.codigo',        
        readonly=True,                
    )    
    descripcion = fields.Text(
        string=u'Descripción',
    )
    cumplio_mc = fields.Boolean(
        string=u'Cumplió MC',
    )
    #/////////////////////////////////////////////
    
    x_registro_id = fields.Many2one(
        string=u'Registro ID',
        comodel_name='sup_mc_scp',
        ondelete='cascade',      
    )
    
class sup_scp_lines(models.Model):
    _name = 'sup_scp_lines'

    
    name = fields.Many2one(
        string=u'SCP',
        comodel_name='sup_scp',
        ondelete='set null',        
        required=True,        
    )
    codigo = fields.Char(
        string='Código',        
        related='name.codigo',        
        readonly=True,                
    )    
    descripcion = fields.Text(
        string=u'Descripción',
    )
    cumplio_scp = fields.Boolean(
        string=u'Cumplió SCP',
    )
    #/////////////////////////////////////////////
    
    x_registro_id = fields.Many2one(
        string=u'Registro ID',
        comodel_name='sup_mc_scp',
        ondelete='cascade',      
    )
class sup_otro_lines(models.Model):
    _name = 'sup_otro_lines'
    
    name = fields.Text(
        string=u'Otro',        
    )
    cumplio_resolucion = fields.Boolean(
        string=u'Cumplió Resolución',
    )
    #/////////////////////////////////////////////    
    x_registro_id = fields.Many2one(
        string=u'Registro ID',
        comodel_name='sup_mc_scp',
        ondelete='cascade',      
    )
    
    
    
    
    
    
    
    

    