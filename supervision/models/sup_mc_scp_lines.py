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
    descripcion = fields.Text(
        string=u'Descripción',
    )
    #/////////////////////////////////////////////
    #/////////////////////////////////////////////
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
    descripcion = fields.Text(
        string=u'Descripción',
    )
    #/////////////////////////////////////////////
    #/////////////////////////////////////////////
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
    #/////////////////////////////////////////////
    #/////////////////////////////////////////////
    #/////////////////////////////////////////////    
    x_registro_id = fields.Many2one(
        string=u'Registro ID',
        comodel_name='sup_mc_scp',
        ondelete='cascade',      
    )
    
    
    
    
    
    
    
    

    