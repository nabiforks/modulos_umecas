# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Entrevistas(models.Model):
    _name = 'umc_entrevistas'

    x_name = fields.Char('Entrevista', required=True, readonly=True,
                         default=lambda self: 'Nuevo'
                         )
    x_lugar_entrevista = fields.Char(
        string=u'Lugar',
    )
    x_fecha_entrevista = fields.Datetime(
        string=u'Fecha y hora',
        default=fields.Datetime.now,
    )    
    x_evaluacion_id = fields.Many2one(
        string=u'Evaluación',
        comodel_name='umc_evaluacion',
        readonly=True,
        ondelete='set null',
    )
    x_evaluador_id = fields.Integer(
        string=u'Evaluador ID',
        readonly=True,
        related='x_evaluacion_id.x_evaluador_id.id',        
    )
    x_evaluador_name = fields.Char(
        string=u'Evaluador',
        readonly=True,
        related='x_evaluacion_id.x_evaluador_id.name',
        store=True        
    )
    x_imputado_name = fields.Char(
        string=u'Imputado',
        readonly=True,
        related='x_evaluacion_id.partner_id.display_name',        
    )
    
    @api.model
    def create(self, vals):
        if vals.get('x_name', 'Nuevo') == 'Nuevo':
            vals['x_name'] = self.env['ir.sequence'].next_by_code(
                'umc_entrevistas') or'Nuevo'
        result = super(Entrevistas, self).create(vals)
        return result
    #///////////////////////////////////////Campos de las entrevistas////////////////
    #///////////////////////////////////////Campos de las entrevistas////////////////
    #///////////////////////////////////////Campos de las entrevistas////////////////

    #/////////////////////Datos personales//////////////
    x_apellido_pat = fields.Char(
        string=u'Apellido Paterno',
        # related='partner_id.lastname',
    )

    x_apellido_mat = fields.Char(
        string=u'Apellido Materno',
        # related='partner_id.x_apellido_mat',
    )
    x_nombre_entrevistado = fields.Char(
        string=u'Nombre(s)',
        # related='partner_id.firstname',
    )
    x_otronombre = fields.Char(
        string=u'Otro nombre',
    )
    x_apodo = fields.Char(
        string=u'Apodo',
    )
    x_lugar_nacimiento = fields.Char(
        string=u'Lugar de Nacimiento',
    )
    x_fecha_nacimiento = fields.Date(
        string=u'Fecha de nacimiento',
    )
    x_edad = fields.Integer(
        string=u'Edad',
    )
    x_sexo = fields.Selection(
        string=u'Sexo',
        selection=[('m', 'Masculino'), ('f', 'Femenino')]
    )

    #///////////////////////// II.-Domicilio/////////////////

    x_domicilio_actual = fields.One2many(
        string=u'Domicilio(s)',
        comodel_name='umc_domicilio',
        inverse_name='x_evaluacion_id',
    )
    
    
    #//////////////////////////////////III.- Lazos con la comunidad////////////////
    x_actividades_ids = fields.One2many(
        string=u'Actividades que realiza',
        comodel_name='umc_actividades',
        inverse_name='x_entrevista2_id',
    )
    #//////////////////////////////////IV.-Relaciones familiares/////////////////    
    x_contacto_ids = fields.One2many(
        string=u'Familiares',
        comodel_name='res.partner',
        inverse_name='x_entrevistas_id',
    )
    x_imputado_id = fields.Integer(
        string=u'Inputado',
        related='x_evaluacion_id.partner_id.id',        
    )
    #//////////////////////////////////V.-Amistades Referencias personales/////////////////





    #//////////////////////////////////VI.-Empleo/////////////////
    
    x_empleos_ids = fields.One2many(
        string=u'Empleos',
        comodel_name='umc_empleos',
        inverse_name='x_entrevista_id',
    )
    #//////////////////////////////////VII.-Estudios/////////////////
    
    x_estudios_ids = fields.One2many(
        string=u'Estudios',
        comodel_name='umc_estudios',
        ondelete='set null',
        inverse_name="x_entrevista_id"
    )

    #//////////////////////////////////VIII.-Antecedentes penales/////////////////
    
    x_antecedentes_ids = fields.Many2many(
        'umc_expedientes',
        string=u'Antecedentes',        
        default=lambda self: self.env['umc_expedientes'].search([('partner_id','=',self.x_imputado_id)]).ids,        
    )

    
    
    