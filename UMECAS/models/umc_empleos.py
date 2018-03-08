# -*- coding: utf-8 -*-
from odoo import api, fields, models


class umc_empleos(models.Model):
    _name = 'umc_empleos'

    x_name = fields.Many2one(
        string=u'Ocupación',
        comodel_name='umc_ocupacion',
        required=True,
        ondelete='set null',
    )
    x_actual_anterior = fields.Selection(
        string=u'Actual/Anterior',
        selection=[('1', 'Actual'), ('2', 'Anterior')],
        default='1',
    )
    x_tipo_empleo = fields.Selection(
        string=u'Tipo de Empleo',
        selection=[('1', 'Constante'), ('2', 'Variable')]
    )
    x_formal = fields.Selection(
        string=u'Formal',
        selection=[('1', 'Formal'), ('2', 'Informal')]
    )
    x_propio = fields.Selection(
        string=u'Propio',
        selection=[('1', 'Por cuenta propia'), ('2', 'Al servicio de alguien')]
    )
    x_entrevista_id = fields.Many2one(
        string=u'Entrevista ID',
        comodel_name='umc_entrevistas',
        ondelete='set null',
    )
    x_domicilio_ids = fields.One2many(
        string=u'Domicilio',
        comodel_name='umc_domicilio',
        inverse_name='x_empleo_id',
    )
    x_patron = fields.Char(
        string=u'Patrón o Jefe inmediato y/o empresa',
    )
    x_salario = fields.Float(
        string=u'Salario mensual',
    )
    x_dias_trabaja = fields.Integer(
        string=u'Días a la semana',
    )
    x_hora_inicio = fields.Float(
        string=u'Trabaja desde',
    )
    x_hora_fin = fields.Float(
        string=u'Trabaja hasta',
    )
    x_anios_trabajando = fields.Integer(
        string=u'Años',
    )
    x_meses_trabajando = fields.Integer(
        string=u'Meses',
    )
