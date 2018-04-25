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
            vals['x_name'] = self.env['ir.sequence'].next_by_code(
                'sup_entrevista_encuadre') or'Nuevo'
        result = super(sup_entrevista_encuadre, self).create(vals)
        return result
    
    x_imputado = fields.Many2one(
        string=u'Imputado',
        comodel_name='res.partner',
        ondelete='restrict',
        #readonly=True,        
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
    actividades_evaluacion = fields.Selection(
        string=u'Actividades de evaluación',
        selection=[('1', 'Entrevista de Evaluación'), ('2', 'Evaluación de riesgos'),('3','Opinión Técnica'),('4','Otra')]
    )
    x_otra_actividad = fields.Char(
        string=u'Otra',
    )
    x_resolucion = fields.Selection(
        string=u'Resolución',
        selection=[('mc', 'MC'), ('scp', 'SCP')],        
        readonly=True,        
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
    
    @api.depends('x_fecha_nacimiento','x_fecha_today')
    def calcular_edad(self):
        self.x_fecha_today = date.today()
        print "////////////////////////////",self.x_fecha_today
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
            
     
    
    
    
    
    
    
    
    