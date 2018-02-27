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
class Actividades_participa(models.Model):
    _name='umc_actividades'
    x_name = fields.Char(
        string=u'Actividad',        
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
#/////////////////////////////Catalogo de parentesco/////////////////////////////////////////
class umc_parentesco(models.Model):
    _name='umc_parentesco'
    x_name = fields.Char(
        string=u'Parentesco',        
        required=True,        
    )
#/////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////Catalogo de parentesco/////////////////////////////////////////
class umc_ocupacion(models.Model):
    _name='umc_ocupacion'
    x_name = fields.Char(
        string=u'Ocupación',        
        required=True,        
    )  
    

