# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Domicilio(models.Model):
    _name = 'umc_domicilio'

    x_name = fields.Char(
        string=u'Name',
    )
    x_calle = fields.Char(
        string=u'Calle',
    )
    x_colonia = fields.Char(
        string=u'Colonia',
    )
    x_municipio = fields.Char(
        string=u'Municipio',
    )
    x_estado_id = fields.Many2one(
        string=u'Estado',
        comodel_name='res.country.state',
        default=lambda self: 504,
        ondelete='set null',
    )
    """x_pais_id = fields.Many2one(
        string=u'País',
        comodel_name='res.country',
        default=lambda self: 157,
        ondelete='set null',
    )"""
    x_vivienda = fields.Many2one(
        string=u'Tipo Vivienda',
        comodel_name='umc_tipo_vivienda',
        ondelete='set null',
    )

    x_tipo_domicilio = fields.Selection(
        string=u'Tipo de domicilio ',
        selection=[('actual', 'Actual'), ('secundario','Secundario'), ('anterior', 'Anterior')],
        default='actual',
    )
    x_motivo_mudanza = fields.Text(
        string=u'Motivos de mudanza',        
    )  
    x_caracteristicas_ref = fields.Text(
        string=u'Caracteristicas y referencias',        
    )
    

    x_croquis = fields.Char(string="Geolocalización", default='{"position":{"lat":19.04360786502212,"lng":-98.19820135831833},"zoom":15}',
                            )

    x_evaluacion_id = fields.Many2one(
        string=u'Entrevista ID',
        comodel_name='umc_entrevistas',
        ondelete='set null',
    )
    x_empleo_id = fields.Many2one(
        string=u'Empleo ID',
        comodel_name='umc_empleos',
        ondelete='set null',
    )
    x_estudios_id = fields.Many2one(
        string=u'Estudio ID',
        comodel_name='umc_estudios',
        ondelete='set null',
    )
