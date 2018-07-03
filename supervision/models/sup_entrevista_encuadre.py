# -*- coding: utf-8 -*-
from datetime import timedelta, datetime,date
from odoo import api, fields, models


class sup_entrevista_encuadre(models.Model):
    
    _inherit = 'umc_entrevistas'   
    _name = 'sup_entrevista_encuadre'

    x_name = fields.Char('Entrevista', required=True, readonly=True,
                         default=lambda self: 'Nuevo'
                         )
    @api.model
    def create(self, vals):
        if vals.get('x_name', 'Nuevo') == 'Nuevo':
            vals['x_name'] = self.env['ir.sequence'].sudo().next_by_code(
                'sup_entrevista_encuadre') or'Nuevo'
        result = super(sup_entrevista_encuadre, self).create(vals)
        return result
    
    x_imputado = fields.Many2one(
        string=u'Imputado',
        comodel_name='res.partner',
        ondelete='restrict',
        readonly=True,        
        required=True,        
    )
    x_orden_id = fields.Many2one(
        string=u'Orden de Supervisión',
        comodel_name='sup_mc_scp',
        ondelete='cascade',
        readonly=True,        
    )    
    fecha_hora_inicio = fields.Datetime(
        string=u'Fecha/Hora inicio',
        default=fields.Datetime.now,
    )
    x_supervisor_id = fields.Many2one(
        string=u'Supervisor',
        comodel_name='res.users',
        ondelete='set null',
        #readonly=True,
    )
    actividades_entrevista = fields.Boolean(
        string=u'Entrevista de evaluación',        
    )
    
    actividades_evaluacion = fields.Boolean(
        string=u'Evaluación de Riesgos',
    )
    actividades_opinion = fields.Boolean(
        string=u'Opinión Técnica',
    )
    x_otra_actividad = fields.Char(
        string=u'Otra',
    )
    x_resolucion = fields.Selection(
        string=u'Resolución',
        selection=[('mc', 'MC'), ('scp', 'SCP'),('otro','Otra')]
    )
    x_numero_causa = fields.Char(
        string=u'Número de causa',
    )
    x_delitos_id = fields.Many2many(
        string=u'Delito(s)',
        comodel_name='umc_delitos',
    )
    x_reclasificado = fields.Selection(
        string=u'Reclasificado',
        selection=[('si', 'Si'), ('no', 'No')]
    )
    
    x_factores_riesgos = fields.Text(
        string=u'Factores de Riesgos',
    )
    x_factores_estabilidad = fields.Text(
        string=u'Factores de Estabilidad',
    )
    #=====Renombrar el campo para quitarle el attr required y no marque error    
    x_evaluacion_id = fields.Many2one(
        string=u'Evaluacion_id',
        comodel_name='umc_evaluacion',        
        required=False,        
        ondelete='set null',
    )
    @api.multi
    def set_actualizar_entrevista(self):
        self.x_orden_id.get_ultima_entrevista()
        return True
    #================================================================================
    #=====Renombrar campos para o2m y m2o============================================
    #================================================================================
    x_domicilio_actual = fields.One2many(
        string=u'Domicilio(s)',
        comodel_name='umc_domicilio',
        inverse_name='x_encuadre_id',
    )
    x_enfermedades_ids = fields.One2many(
        string=u'Enfermedades',
        comodel_name='umc_enfermedades_padece',
        inverse_name='x_encuadre_id',
    )
    x_empleos_ids = fields.One2many(
        string=u'Empleos',
        comodel_name='umc_empleos',
        inverse_name='x_encuadre_id',
    )
    x_contacto_ids = fields.One2many(
        string=u'Familiares',
        comodel_name='res.partner',
        inverse_name='x_encuadre_id',
    )
    x_amistades_ids = fields.One2many(
        string=u'Amistades (Referencias personales)',
        comodel_name='umc_amistades',
        inverse_name='x_encuadre_id',
    )
    x_actividades_ids = fields.One2many(
        string=u'Actividades que realiza',
        comodel_name='umc_actividades',
        inverse_name='x_encuadre_id',
    )
    x_sustancias_ids = fields.One2many(
        string=u'Consume sustancias',
        comodel_name='umc_sustancias_consume',
        inverse_name='x_encuadre_id',
    )
    #=============Termina renombramiento de campos relacionales
    
    @api.depends('x_fecha_nacimiento','x_fecha_today')
    def calcular_edad(self):
        self.x_fecha_today = date.today()
        if self.x_fecha_nacimiento:
            start_date = fields.Datetime.from_string(self.x_fecha_nacimiento)
            end_date = fields.Datetime.from_string(self.x_fecha_today)
            dias = int((end_date - start_date).days)
            bisiesto = (dias/365)/4
            anios =(dias+bisiesto)/365
            self.x_edad=anios
    #/////////////////////Datos personales//////////////////////////////////////////////////////
    #/////////////////////Datos personales//////////////////////////////////////////////////////
    #/////////////////////Datos personales//////////////////////////////////////////////////////
    #/////////////////////Datos personales//////////////////////////////////////////////////////
    
    x_sexo = fields.Selection(
        string=u'Género',
        selection=[('m', 'Masculino'), ('f', 'Femenino'), ('o', 'Otro')]
    )     
    x_celular = fields.Char(
        string=u'Teléfono Celular',
    )
    x_imputado_id = fields.Integer(
        string=u'Inputado',
        related='x_imputado.id',
    )
    #==========Datos para reporte==========
    x_dia_hora_firma = fields.Char(
        string='Día y hora de firma',
    )
    x_hora_conclusion = fields.Float(
        string='Hora de conclusión',
    )
    x_abogado = fields.Char(
        string='Nombre del abogado',
    )
    seccion = fields.Char(
        string='Sección',
        default='11S',
    )
    serie = fields.Char(
        string='Serie',
        default='11S.3',
    )
    sub_serie = fields.Char(
        string='Subserie',
    )
            
     
    
    
    
    
    
    
    
    