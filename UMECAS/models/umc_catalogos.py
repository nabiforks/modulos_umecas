# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models

#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////Catalogo de delitos/////////////////////////////////////////
class Delitos(models.Model):
    _name='umc_delitos'

    
    x_name = fields.Char(
        string=u'Delito',
        required=True,
    )    
    x_expedientes_id = fields.Many2one(
        string=u'Expedientes_ids',
        comodel_name='umc_expedientes',
        ondelete='set null',
    )
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////Catalogo de tipo de vivienda/////////////////////////////////////////
class Tipo_vivienda(models.Model):
    _name='umc_tipo_vivienda'
    x_name = fields.Char(
        string=u'Tipo',required=True,
    )
    x_valor = fields.Integer(
        string=u'Valor',
    )

#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////Catalogo de actividades que realiza/////////////////////////////////////////
class actividades_participa(models.Model):
    _name='umc_actividades'
    
    x_name= fields.Many2one(
        string=u'Actividad',
        comodel_name='umc_actividad',
        ondelete='set null',
        required=True, 
    )
    x_tipo = fields.Selection(
        string=u'Tipo',
        selection=[('1', 'Cívica'), ('2', 'Cultural'),('3', 'Religiosa'),('4', 'Deportiva'),('5', 'Otro')]
    )            
    x_descripcion = fields.Text(
        string=u'Descripción',
    )    
    x_entrevista_id = fields.Many2one(
        string=u'Entrevista Id',
        comodel_name='umc_entrevistas',
        ondelete='set null',
    )
    x_entrevista2_id = fields.Many2one(
        string=u'Entrevista Id',
        comodel_name='umc_entrevistas',
        ondelete='set null',
    )
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////Catalogo de actividades/////////////////////////////////////////
class actividades_catalogo(models.Model):
    _name='umc_actividad'    
    x_name = fields.Char(
        string=u'Actividad',
    )
    
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////Catalogo de parentesco/////////////////////////////////////////
class umc_parentesco(models.Model):
    _name='umc_parentesco'
    x_name = fields.Char(
        string=u'Parentesco',        
        required=True,        
    )
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////Catalogo de ocupacion/////////////////////////////////////////
class umc_ocupacion(models.Model):
    _name='umc_ocupacion'
    x_name = fields.Char(
        string=u'Ocupación',        
        required=True,        
    )  
    

#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////Catalogo de nacionalidad/////////////////////////////////////////
class umc_nacionalidad(models.Model):
    _name='umc_nacionalidad'
    x_name = fields.Char(
        string=u'Nacionalidad',        
        required=True,        
    )     
    x_codigo = fields.Char(
        string=u'Código',
    )
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////Catalogo de identificacion/////////////////////////////////////////
class umc_identificacion(models.Model):
    _name='umc_identificacion'
    x_name = fields.Char(
        string=u'Identificación',        
        required=True,        
    )     
    x_codigo = fields.Char(
        string=u'Código',
    )    