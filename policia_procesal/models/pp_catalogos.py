# -*- coding: utf-8 -*-

from odoo import fields, models

#===========================
#|      CATALOGO JUECES    |
#===========================
class Jueces(models.Model):
    _name = 'pp.jueces'

    name = fields.Char(
        string='Nombre',
    )
    titulo = fields.Char(
        string='Título',
    )
    cargo = fields.Char(
        string='Cargo',
    )

#================================
#|      CATALOGO AUTORIDADES    |
#================================
class Autoridades(models.Model):
    _name = 'pp.autoridad'

    name = fields.Char(
    	string='Nombre'
    )
    titulo = fields.Char(
    	string='Titulo'
    )
    cargo = fields.Char(
    	string='Cargo'
    )

#============================
#|      CATALOGO MEDICOS    |
#============================
class Medicos(models.Model):
    _name = 'pp.medico'

    name = fields.Char(
    	string='Nombre'
    )
    cedula = fields.Char(
    	string='Cédula'
    )

#==============================
#|      CATALOGO VEHICULOS    |
#==============================
class Vehiculos(models.Model):
    _name = 'pp.vehiculos'

    name = fields.Char(
        string='Vehículo oficial',
    )
    no_economico = fields.Char(
        string='Número económico',
    )
    placas = fields.Char(
        string='Placas',
    )

#==============================
#|   CATALOGO DEPENDENCIAS    |
#==============================
class Vehiculos(models.Model):
    _name = 'pp.dependencias'

    codigo = fields.Char(
        string='Código',
    )
    name = fields.Char(
        string='Dependencia',
    )

#==============================
#|   CATALOGO RCI/RSA         |
#==============================
class Vehiculos(models.Model):
    _name = 'pp.responsable'

    name = fields.Char(
        string='Nombre completo',
    )

#==============================
#|  CATALOGO POLICIA PROCESAL |
#==============================
class Vehiculos(models.Model):
    _name = 'pp.jefe_pp'

    name = fields.Char(
        string='Nombre completo',
    )
    cargo = fields.Char(
        string='Cargo',
    )
    grupo = fields.Char(
        string='Grupo',
    )