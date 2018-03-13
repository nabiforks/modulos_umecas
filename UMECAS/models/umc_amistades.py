# -*- coding: utf-8 -*-
from odoo import api, fields, models


class umc_amistades(models.Model):
    _name = 'umc_amistades'

    x_name = fields.Char(
        string=u'Nombre Completo',
        required=True,
    )
    x_domicilio_ids = fields.One2many(
        string=u'Domicilio',
        comodel_name='umc_domicilio',
        inverse_name='x_empleo_id',
    )
    x_relacion = fields.Many2one(
        string=u'Tipo de relación',
        comodel_name='umc_parentesco',
        ondelete='set null',
    )
    x_numero = fields.Char(
        string=u'Teléfono (Casa, empleo, cel.)',
    )
    x_anios_conocer = fields.Integer(
        string=u'Años',
    )
    x_meses_conocer = fields.Integer(
        string=u'Meses',
    )

    x_entrevista_id = fields.Many2one(
        string=u'Entrevista _ID',
        comodel_name='umc_entrevistas',
        ondelete='cascade',
    )
