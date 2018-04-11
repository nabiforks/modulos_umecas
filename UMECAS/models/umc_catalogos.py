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
        selection=[('normal', 'Normal'), ('intramuros', 'INTRAMUROS'),('extramuros', 'EXTRAMUROS')]
    )            
    x_descripcion = fields.Text(
        string=u'¿Cuales?',
    )
    x_tiempo_libre = fields.Selection(
        string=u'¿Realiza otra(s) actividad en su tiempo libre?',
        selection=[('si', 'Si'), ('no', 'No')]
    )
    x_tiempo_libre_cuales = fields.Text(
        string=u'¿Cuales?',
    )
    x_entrevista2_id = fields.Many2one(
        string=u'Entrevista Id',
        comodel_name='umc_entrevistas',
        ondelete='cascade',
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
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////Catalogo de lengua/////////////////////////////////////////
class umc_lengua(models.Model):
    _name='umc_lengua'
    x_name = fields.Char(
        string=u'Lengua',        
        required=True,        
    )     
    x_codigo = fields.Char(
        string=u'Código',
    )
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////Catalogo de grupoetnico/////////////////////////////////////////
class umc_grupoetnico(models.Model):
    _name='umc_grupoetnico'
    x_name = fields.Char(
        string=u'Grupo Étnico',        
        required=True,        
    )     
    x_codigo = fields.Char(
        string=u'Código',
    )
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////Catalogo de idioma/////////////////////////////////////////
class umc_idioma(models.Model):
    _name='umc_idioma'
    x_name = fields.Char(
        string=u'Idioma',        
        required=True,        
    )     
    x_codigo = fields.Char(
        string=u'Código',
    )
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////Catalogo de autoridad/////////////////////////////////////////
class umc_autoridad(models.Model):
    _name='umc_autoridad'
    x_name = fields.Char(
        string=u'Autoridad',        
        required=True,        
    )     
    x_codigo = fields.Char(
        string=u'Código',
    )

#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////Catalogo de lugares/////////////////////////////////////////
class umc_lugares(models.Model):
    _name='umc_lugares'
    x_name = fields.Char(
        string=u'Lugares',        
        required=True,        
    )     
    x_codigo = fields.Char(
        string=u'Código',
    )