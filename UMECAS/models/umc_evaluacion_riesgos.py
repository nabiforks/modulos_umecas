# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class umc_evaluacion(models.Model):
    _name = 'umc_evaluacion'
    # _inherit = 'mail.thread'

    x_name = fields.Char('Solicitud', required=True, readonly=True,
                         default=lambda self: 'Nuevo')
    folio_evalucion = fields.Char('Folio de la evaluación', readonly=True, default=lambda self: '')

    x_expediente_id = fields.Many2one(
        'umc_expedientes',
        string=u'Expediente',
        readonly=True,
        required=True,
        ondelete='set null',
    )
    x_evaluador_id = fields.Many2one(
        'res.users',
        string=u'Evaluador',
        required=True,
        ondelete='set null',        
        domain="[('company_id','=',x_casa_justicia)]",        
    )
    partner_id = fields.Many2one(
        'res.partner',
        string=u'Imputado ID',
        readonly=True,
        required=True,
        default=lambda self: self.env.context.get('partner_id'),
        ondelete='set null',
    )
    x_imputado_name = fields.Char(
        string=u'Imputado',
        related='partner_id.display_name',
        readonly=True,
    )
    x_tipo_entrevista = fields.Selection(
        [('retenido', 'Retenido'), ('adolescente', 'Adolescente'), ('interno', 'Interno'),('citacion', 'Citación')], default='1', required=True, string=u'Tipo de Entrevista')
    
    x_fecha_inicio = fields.Datetime(
        string=u'Fecha/Hora Inicio',
    )
    x_fecha_final = fields.Datetime(
        string=u'Fecha/Hora Final',
    )
    x_tiempo_transcurrido = fields.Float(
        string=u'Tiempo transcurrido',        
        readonly=True,        
    )
    
    

    state = fields.Selection([
        ('solicitud', 'Solicitud'),
        ('entrevista', 'Entrevista'),
        ('analisis', 'Escala de Riesgos'),
        ('evaluacion', 'Evaluación'),
        ('evaluacion_terminada', 'Evaluación Terminada'),
    ], default='solicitud', readonly=True, string='Estatus')
    x_casa_justicia = fields.Many2one(
        string=u'Casa de Justicia',
        comodel_name='res.company',
        ondelete='set null',
        readonly=True,
        required=True,
    )

    @api.model
    def create(self, vals):
        if vals.get('x_name', 'Nuevo') == 'Nuevo':
            vals['x_name'] = self.env['ir.sequence'].sudo().next_by_code(
                'umc_evaluacion') or 'Nuevo'
        result = super(umc_evaluacion, self).create(vals)
        return result

    @api.multi
    def asignar_borrador(self):
        self.state = 'solicitud'

    @api.multi
    def generar_entrevista(self):
        if self.x_evaluador_id:
            self.state = 'entrevista'
            valores_entrevista = {'x_evaluacion_id': self.id,
                                  'x_evaluador_id': self.x_evaluador_id,
                                  'x_imputado_id': self.partner_id,
                                  'x_casa_justicia': self.x_casa_justicia.id,
                                  'x_cdi':self.x_expediente_id.x_cdi_nic,
                                  'x_causa_penal':self.x_expediente_id.x_causa_penal,
                                  'x_apellido_pat':self.partner_id.ap_paterno,
                                  'x_apellido_mat':self.partner_id.ap_materno,
                                  'x_nombre_entrevistado':self.partner_id.name}
            res = self.env['umc_entrevistas'].create(valores_entrevista)
            self.x_entrevista_id = res
            return res

    @api.multi
    def terminar_entrevista(self):
        if self.x_entrevista_status == 'terminado':
            self.state = 'analisis'
            secciones = self.env['ucm.escalavalores.secciones'].search([]).ids
            for seccion in secciones:
                self.env['ucm.escalavalores.evaluacion'].create(
                    {'seccion': seccion, 'x_evaluacion_id': self.id})
        else:
            raise ValidationError("La entrevista aun no ha sido terminada")

    @api.multi
    def getFolioEvaluacion(self):
        now = datetime.now()
        folio = self.env['umc_expedientes'].createFolioExpedienteByAnio(now.year, 2)
        return folio

    """@api.multi
    def getFolioEvaluacion(self):
        now = datetime.now()
        folio = self.env['umc_expedientes'].createFolioExpedienteByAnio(now.year, 2)
        return folio"""

    @api.multi
    def terminar_analisis(self):
        self.state = 'evaluacion'

    @api.multi
    def terminar_evaluacion(self):
        print self.folio_evalucion
        if self.folio_evalucion:
            print "-->>  Ya fue asignado el folio de la evalución -->>"
            return
        else:
            self.folio_evalucion = self.getFolioEvaluacion()
            self.calcular_tiempo()
            self.state='evaluacion_terminada'
    @api.multi
    def calcular_tiempo(self):
        if not self.x_fecha_final:
            self.x_fecha_final = datetime.now()
        if self.x_fecha_inicio and self.x_fecha_final:
            start_date = fields.Datetime.from_string(self.x_fecha_inicio)
            end_date = fields.Datetime.from_string(self.x_fecha_final)
            dias = float((end_date - start_date).days*24)
            horas = float((end_date - start_date).seconds/3600)
            minutos = float((((end_date - start_date).seconds%3600)/60))
            self.x_tiempo_transcurrido=dias + horas+(minutos/60)
        
        


    # ///////////////////////////////////////Campos de las entrevistas////////////////
    # ///////////////////////////////////////Campos de las entrevistas////////////////
    # ///////////////////////////////////////Campos de las entrevistas////////////////

    x_entrevista_id = fields.Many2one(
        string=u'Entrevista',
        comodel_name='umc_entrevistas',
        readonly=True,
        ondelete='restrict',
    )
    x_entrevista_status = fields.Selection(
        string=u'Estatus de Entrevista',
        readonly=True,
        related='x_entrevista_id.state',
    )

    # ///////////////////////////////////////////Escala de riesgos///////////////////////////////////////////////
    # ///////////////////////////////////////////Escala de riesgos///////////////////////////////////////////
    # ///////////////////////////////////////////Escala de riesgos///////////////////////////////////////////////
    # ///////////////////////////////////////////Escala de riesgos////////////////////////////////////////////////

    x_fecha_analisis = fields.Date(
        string=u'Fecha Analisis de Riesgos',
        default=fields.Date.context_today,
    )
    x_ponderacion = fields.Integer(
        string=u'Ponderación',
        compute='calcular_ponderacion'
    )
    x_escala_riesgos = fields.Selection(
        string=u'Escala de riesgo',
        selection=[('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto')],
        compute='calcular_ponderacion',        
        store=True,        
    )
    x_escala_valores_id = fields.Many2one(
        string=u'Escala valores ID',
        comodel_name='umc_escalas',
        store=True,
        default=lambda self: self.env['umc_escalas'].search([]),
        ondelete='set null',
    )

    x_escalas_ids = fields.One2many(
        string=u'Escala de valores',
        comodel_name='ucm.escalavalores.evaluacion',
        inverse_name='x_evaluacion_id',
        # default=lambda self: self.env['ucm.escalavalores.evaluacion'].search([]).ids,
    )

    @api.multi
    @api.depends('x_escalas_ids', 'x_escala_valores_id.x_bajo', 'x_escala_valores_id.x_alto')
    def calcular_ponderacion(self):
        for record in self:
            sumador = 0
            for linea_escala in record.x_escalas_ids:
                sumador += linea_escala.num_valor
            record.x_ponderacion = sumador
            if sumador >= record.x_escala_valores_id.x_bajo:
                record.x_escala_riesgos = 'bajo'
            elif sumador <= record.x_escala_valores_id.x_alto:
                record.x_escala_riesgos = 'alto'
            else:
                record.x_escala_riesgos = 'medio'

    # ///////////////////////////////////////////Evaluación/////////////////////////////////////////////
    # ///////////////////////////////////////////Evaluación/////////////////////////////////////////////
    # ///////////////////////////////////////////Evaluación/////////////////////////////////////////////
    # ///////////////////////////////////////////Evaluación/////////////////////////////////////////////

    x_conclusion = fields.Text(
        string=u'Conclusión',
    )

    
    #==========Campos para reporte==========
    x_name_abogado = fields.Char(
        string='Abogado',
    )
    x_area = fields.Char(
        string='Área',
    )
    x_puesto = fields.Char(
        string='Puesto',
    )
    x_actividades_desarrolladas = fields.Text(
        string='Tipo de actividades desarrolladas',
    )
    x_nucleo_primario = fields.Text(
        string='Núcleo primario',
    )
    x_nucleo_secundario = fields.Text(
        string='Núcleo secundario',
    )
    x_ref_personales = fields.Text(
        string='Referencias personales',
    )
    x_sintesis_act_laboral = fields.Text(
        string='Síntesis de actividad laboral',
    )
    x_ant_laborales = fields.Text(
        string='Antecedentes laborales',
    )
    x_sintesis_domiciliaria = fields.Text(
        string='Síntesis domiciliaria',
    )
    x_sintesis_educativa = fields.Text(
        string='Síntesis educativa',
    )
    x_inf_destacada = fields.Text(
        string='Información destacada',
    )
    x_mc_anteriores = fields.Text(
        string='Cumplimiento de medidas cautelares anteriores',
    )
    x_verificacion_datos = fields.Text(
        string='Verificación de datos',
    )
    x_comportamiento = fields.Text(
        string='Comportamiento en la entrevista',
    )
    x_conc_domiciliaria = fields.Text(
        string='Domiciliario',
    )
    x_conc_laboral_esc = fields.Text(
        string='Laboral y/o escolar',
    )
    x_conc_familiar = fields.Text(
        string='Familiar',
    )
    x_conc_victima = fields.Text(
        string='Victima u ofendido',
    )
    x_conc_testigos = fields.Text(
        string='Testigos',
    )
    x_conc_comunidad = fields.Text(
        string='Comunidad y/o sociedad',
    )
    x_conc_retencion = fields.Text(
        string='Retención',
    )
    x_conc_ant_reincidencias = fields.Text(
        string='Antecedentes y/o Reincidencias',
    )
    x_conc_ingresos = fields.Text(
        string='Ingresos económicos',
    )
    x_conc_proximidad = fields.Text(
        string='Proximidad',
    )
    x_nombre_elav = fields.Char(
        string='Elaboró',
    )
    x_puesto_elav = fields.Char(
        string='Puesto',
    )
    x_seccion = fields.Char(
        string='Sección',
    )
    x_serie = fields.Char(
        string='Serie',
    )
    x_sub_serie = fields.Char(
        string='Subserie',
    )

    #==========Default value==========
    x_parrafo = fields.Text(
        string='Párrafo inicializado',
        default='En atención al oficio X, asignado por el Abogado X, Agente del Ministerio Público Adscrito a la Unidad de Flagrancia de fecha, con fundamento en lo dispuesto por los articulos 153, 155, 156, 157, 158, 164, 168, 169 y 170 del Código Nacional de Procedimientos Penales: 65, 66, 67 y 68 de la Ley de Ejecucíón de Medidas Cautelares y Sanciones Penales para el Estado de Puebla y 17 fracción XIII y XIV de la Ley de Seguridad Pública del Estado; se emite la presente evaluación de riesgos del entrevistado X, dentro de la Carpeta de Investigación  X. Con base al resultado de la entrevista y recopilación de datos.',
    )

