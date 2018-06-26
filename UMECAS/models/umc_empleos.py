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
        selection=[('actual', 'ACTUAL'), ('actual2',
                                          'ACTUAL INTRAMUROS'), ('anterior', 'ANTERIOR')],
        default='actual',
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
        string=u'Salario',
    )
    x_moneda = fields.Selection(
        string=u'Moneda',
        selection=[('peso', 'Pesos'), ('dolar', 'Dolares'), ('otro', 'Otro')]
    )
    x_salario_pagos = fields.Selection(
        string=u'Pagos ',
        selection=[('1', 'Por hora'), ('2', 'Diarios'),
                   ('3', 'Semanal'), ('4', 'Quincenal'), ('5', 'Mensual'), ('6','Otro')]
    )
    x_dias_trabaja = fields.Selection(
        string=u'Días',
        selection=[('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miercoles'),
                   ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sábado'), ('7', 'Domingo')]
    )
    x_dias_trabaja_hasta = fields.Selection(
        string=u'Hasta',
        selection=[('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miercoles'),
                   ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sábado'), ('7', 'Domingo')]
    )
    x_hora_inicio = fields.Float(
        string=u'Horario',
    )
    x_hora_fin = fields.Float(
        string=u'Trabaja hasta',
    )
    x_anios_trabajando = fields.Integer(
        string=u'Tiempo trabajando',
    )
    x_tiempo_unidad = fields.Selection(
        string=u'Días/Semanas/Meses/Años',
        selection=[('dias', 'Días'), ('semanas', 'Semanas'),
                   ('meses', 'Meses'), ('anios', 'Años')]
    )
    x_motivo = fields.Char(
        string=u'Motivo de cambio',
    )
    x_telefono_empleo = fields.Char(
        string=u'Teléfono',
    )
    x_variable = fields.Boolean(
        string='Variable'
    )
