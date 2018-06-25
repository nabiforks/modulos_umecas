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
        [('retenido', 'Retenido'), ('adolescente', 'Adolescente'), ('interno', 'Interno'), ('citacion', 'Citación')],
        default='1', required=True, string=u'Tipo de Entrevista')

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
        ('impedimento', 'Impedimento'),
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
                                  'x_cdi': self.x_expediente_id.x_cdi_nic,
                                  'x_causa_penal': self.x_expediente_id.x_causa_penal,
                                  'x_apellido_pat': self.partner_id.ap_paterno,
                                  'x_apellido_mat': self.partner_id.ap_materno,
                                  'x_nombre_entrevistado': self.partner_id.name,
                                  'x_hechos_conducta': self.x_expediente_id.x_delito_descripcion,
                                  'x_lugar_detencion': self.lugar_delito()
                                  }
            res = self.env['umc_entrevistas'].create(valores_entrevista)
            self.x_entrevista_id = res
            return res

    def lugar_delito(self):
        text = ""
        if self.x_expediente_id.x_lugar_delito:
            text += str(self.x_expediente_id.x_lugar_delito.encode('utf-8'))
        if self.x_expediente_id.x_colonia_delito_id:
            text += ", "+str(self.x_expediente_id.x_colonia_delito_id.name.encode('utf-8'))
        if self.x_expediente_id.x_municipio_delito_id:
            text += ", "+str(self.x_expediente_id.x_municipio_delito_id.name.encode('utf-8'))
        print text
        return text

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
        self.x_name_abogado = self.x_expediente_id.x_abogado
        self.x_puesto = self.x_expediente_id.x_abogado_cargo
        self.x_historia_personal = self.historia_personal()
        self.x_actividades_desarrolladas = self.actividades_desarrolladas()
        self.x_rel_familiares = self.rel_familiares()
        self.x_ref_personales = self.ref_personales()
        self.x_sintesis_act_laboral = self.ev_empleos()
        self.x_sintesis_domiciliaria = self.sintesis_domiciliaria()
        self.x_sintesis_educativa = self.sintesis_educativa()
        self.x_inf_destacada = self.inf_destacada()
        self.x_nombre_elav = self.x_entrevista_id.x_entrevistador.name

    @api.multi
    def terminar_evaluacion(self):
        print self.folio_evalucion
        if self.folio_evalucion:
            print "-->>  Ya fue asignado el folio de la evalución -->>"
            return
        else:
            self.folio_evalucion = self.getFolioEvaluacion()
            self.calcular_tiempo()
            self.state = 'evaluacion_terminada'

    @api.multi
    def calcular_tiempo(self):
        if not self.x_fecha_final:
            self.x_fecha_final = datetime.now()
        if self.x_fecha_inicio and self.x_fecha_final:
            start_date = fields.Datetime.from_string(self.x_fecha_inicio)
            end_date = fields.Datetime.from_string(self.x_fecha_final)
            dias = float((end_date - start_date).days * 24)
            horas = float((end_date - start_date).seconds / 3600)
            minutos = float((((end_date - start_date).seconds % 3600) / 60))
            self.x_tiempo_transcurrido = dias + horas + (minutos / 60)

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

    def historia_personal(self):
        text = "Entrevistado: " + self.x_imputado_name.encode('utf-8') + '\n'
        text += "Fecha de nacimiento: " + str(self.x_entrevista_id.x_fecha_nacimiento) + '\n'
        text += "Edad: """ + str(self.x_entrevista_id.x_edad) + '\n'
        if self.x_entrevista_id.x_apodo:
            text += "Alias o apodo: " + str(self.x_entrevista_id.x_apodo.encode('utf-8')) + '\n'

        if self.x_entrevista_id.x_lugar_nacimiento:
            text += "Lugar de nacimiento: " + str(self.x_entrevista_id.x_lugar_nacimiento.encode('utf-8')) + '\n'

        if self.x_entrevista_id.x_lengua.x_name:
            text += "Lengua y/o dialecto: " + str(self.x_entrevista_id.x_lengua.x_name.encode('utf-8')) + '\n'

        if self.x_entrevista_id.x_grupo_etnico.x_name:
            text += "Grupo étnico: " + str(self.x_entrevista_id.x_grupo_etnico.x_name.encode('utf-8')) + '\n'

        if self.x_entrevista_id.x_estado_civil:
            text += "Estado civil: " + str(self.x_entrevista_id.x_estado_civil.encode('utf-8')) + '\n'

        if self.x_entrevista_id.x_domicilio_actual:
            for record in self.x_entrevista_id.x_domicilio_actual:
                if record.x_tipo_domicilio == 'actual':
                    domicilio = ""
                    if record.x_calle:
                        domicilio = str(record.x_calle.encode('utf-8')) + ", "
                    if record.x_colonia.name:
                        domicilio += str(record.x_colonia.name.encode('utf-8')) + ", "
                    if record.x_municipio.name:
                        domicilio += str(record.x_municipio.name.encode('utf-8')) + ", "
                    if record.x_estado_id.name:
                        domicilio += str(record.x_estado_id.name.encode('utf-8')) + ", "
                    if record.x_vivienda:
                        domicilio += "vivienda " + str(record.x_vivienda.x_name.encode('utf-8')) + ", "
                    if record.x_tiempo_cantidad:
                        domicilio += str(record.x_tiempo_cantidad) + " "
                    if record.x_tiempo_unidad:
                        domicilio += str(dict(record._fields['x_tiempo_unidad'].selection).get(record.x_tiempo_unidad))
                    text += "Domicilio actual: " + domicilio + '\n'

        return text

    def actividades_desarrolladas(self):
        if self.x_entrevista_id.x_actividades_ids:
            text = "Aludió realizar las siguientes actividades:" + '\n'
            for record in self.x_entrevista_id.x_actividades_ids:
                text += str(record.x_name.x_name.encode('utf-8')) + ", " + str(
                    record.x_descripcion.encode('utf-8')) + '\n'

            if self.x_entrevista_id.x_tiempo_libre == 'si':
                text += '\n'
                text += "Comentó que en su tiempo libre realiza:" + '\n'

                if self.x_entrevista_id.x_tiempo_libre_cuales:
                    text += str(self.x_entrevista_id.x_tiempo_libre_cuales.encode('utf-8'))

        elif not self.x_entrevista_id.x_actividades_ids and self.x_entrevista_id.x_tiempo_libre == 'si':
            text = "Comentó que en su tiempo libre realiza:" + '\n'

            if self.x_entrevista_id.x_tiempo_libre_cuales:
                text += str(self.x_entrevista_id.x_tiempo_libre_cuales.encode('utf-8'))

        else:
            text = "Aludió no realizar actividades cívicas, culturales, religiosas ni deportivas que generen lazos con la comunidad."

        return text

    def rel_familiares(self):
        text = ""
        if self.x_entrevista_id.x_intrafamiliares_primario:
            text += "Núcleo primario" + '\n'
            text += str(self.x_entrevista_id.x_intrafamiliares_primario.encode('utf-8'))+'\n'+'\n'
        if self.x_entrevista_id.x_intrafamiliares_secundario:
            text += "Núcleo secundario" + '\n'
            text += str(self.x_entrevista_id.x_intrafamiliares_secundario.encode('utf-8')) + '\n'

        return text

    def ref_personales(self):
        text = ""
        if self.x_entrevista_id.x_amistades_ids:
            text += "Refirió los siguietes nombres:" + '\n'
            for record in self.x_entrevista_id.x_amistades_ids:
                text += str(record.x_name.encode('utf-8'))
                text += ", con domicilio en "
                for rec in record.x_domicilio_ids:
                    domicilio = ""
                    if rec.x_calle:
                        domicilio = str(rec.x_calle.encode('utf-8')) + ", "
                    if rec.x_colonia.name:
                        domicilio += str(rec.x_colonia.name.encode('utf-8')) + ", "
                    if rec.x_municipio.name:
                        domicilio += str(rec.x_municipio.name.encode('utf-8')) + ", "
                    if rec.x_estado_id.name:
                        domicilio += str(rec.x_estado_id.name.encode('utf-8'))
                    text += domicilio
                if record.x_relacion:
                    text += ", quién es su " + str(record.x_relacion.x_name.encode('utf-8'))
                if record.x_numero:
                    text += ", número de teléfono " + str(record.x_numero.encode('utf-8'))
                if record.x_tiempo_cantidad:
                    text += " con " + str(record.x_tiempo_cantidad) + " "
                if record.x_tiempo_unidad:
                    text += str(
                        dict(record._fields['x_tiempo_unidad'].selection).get(record.x_tiempo_unidad)) + " de conocerlo"
                text += '\n'

        if self.x_entrevista_id.x_no_menciono:
            text += '\n' + str(self.x_entrevista_id.x_no_menciono.encode('utf-8'))

        return text

    def ev_empleos(self):
        text = ""
        if self.x_entrevista_id.x_empleos_ids:
            for record in self.x_entrevista_id.x_empleos_ids:
                if record.x_actual_anterior == 'actual':
                    if record.x_anios_trabajando:
                        text += "Comentó que desde " + str(record.x_anios_trabajando)
                    if record.x_tiempo_unidad:
                        text += " " + str(
                            dict(record._fields['x_tiempo_unidad'].selection).get(record.x_tiempo_unidad)) + " "

                    text += "se desempeña "
                    if record.x_tipo_empleo:
                        text += "de manera " + str(
                            dict(record._fields['x_tipo_empleo'].selection).get(record.x_tipo_empleo))
                    if record.x_formal:
                        text += ", " + str(dict(record._fields['x_formal'].selection).get(record.x_formal))
                    text += " como " + str(record.x_name.x_name.encode('utf-8')) + '\n'
                    if record.x_propio:
                        if record.x_propio == '2':
                            if record.x_patron:
                                text += "Al servicio de: " + str(record.x_patron.encode('utf-8')) + '\n'
                        else:
                            text += "Al servicio de: " + "Por cuenta propia" + '\n'
                    if record.x_domicilio_ids:
                        text += "Con dirección: "
                        for rec in record.x_domicilio_ids:
                            domicilio = ""
                            if rec.x_calle:
                                domicilio = str(rec.x_calle.encode('utf-8')) + ", "
                            if rec.x_colonia.name:
                                domicilio += str(rec.x_colonia.name.encode('utf-8')) + ", "
                            if rec.x_municipio.name:
                                domicilio += str(rec.x_municipio.name.encode('utf-8')) + ", "
                            if rec.x_estado_id.name:
                                domicilio += str(rec.x_estado_id.name.encode('utf-8'))
                            text += domicilio + '\n'
                    text += "Salario " + str(
                        dict(record._fields['x_salario_pagos'].selection).get(record.x_salario_pagos)) + " de " + str(
                        record.x_salario) + " " + str(
                        dict(record._fields['x_moneda'].selection).get(record.x_moneda)) + '\n'
                    text += "Horario: " + str(record.x_dias_trabaja) + " a " + str(
                        record.x_dias_trabaja_hasta) + " de " + str(record.x_hora_inicio) + " a " + str(
                        record.x_hora_fin)

        if self.x_entrevista_id.x_no_menciono_emp:
            text += '\n' + str(self.x_entrevista_id.x_no_menciono_emp.encode('utf-8'))

        return text

    def sintesis_domiciliaria(self):
        text = "SÍNTESIS DOMICILIARIA" + '\n'
        if self.x_entrevista_id.x_domicilio_actual:
            for record in self.x_entrevista_id.x_domicilio_actual:
                if record.x_tipo_domicilio == 'actual':
                    domicilio = "Indicó que desde " + str(record.x_tiempo_cantidad) + " " + str(
                        dict(record._fields['x_tiempo_unidad'].selection).get(record.x_tiempo_unidad))
                    domicilio += " habita en una vivienda"
                    if record.x_vivienda:
                        domicilio += " " + str(record.x_vivienda.x_name.encode('utf-8'))
                    domicilio += " ubicado en la dirección: "
                    if record.x_calle:
                        domicilio += str(record.x_calle.encode('utf-8')) + ", "
                    if record.x_colonia.name:
                        domicilio += str(record.x_colonia.name.encode('utf-8')) + ", "
                    if record.x_municipio.name:
                        domicilio += str(record.x_municipio.name.encode('utf-8')) + ", "
                    if record.x_estado_id.name:
                        domicilio += str(record.x_estado_id.name.encode('utf-8'))
                    text += domicilio + '\n'

            text += '\n' + "DOMICILIOS SECUNDARIOS" + '\n'
            for record in self.x_entrevista_id.x_domicilio_actual:
                if record.x_tipo_domicilio == 'secundario':
                    domicilio = "Indicó que desde " + str(record.x_tiempo_cantidad) + " " + str(
                        dict(record._fields['x_tiempo_unidad'].selection).get(record.x_tiempo_unidad))
                    domicilio += " habita en una vivienda"
                    if record.x_vivienda:
                        domicilio += " " + str(record.x_vivienda.x_name.encode('utf-8'))
                    domicilio += " ubicado en la dirección: "
                    if record.x_calle:
                        domicilio += str(record.x_calle.encode('utf-8')) + ", "
                    if record.x_colonia.name:
                        domicilio += str(record.x_colonia.name.encode('utf-8')) + ", "
                    if record.x_municipio.name:
                        domicilio += str(record.x_municipio.name.encode('utf-8')) + ", "
                    if record.x_estado_id.name:
                        domicilio += str(record.x_estado_id.name.encode('utf-8'))
                    text += domicilio + '\n'

            text += '\n' + "DOMICILIOS ANTERIORES" + '\n'
            for record in self.x_entrevista_id.x_domicilio_actual:
                if record.x_tipo_domicilio == 'anterior':
                    domicilio = "Así mismo indico que desde " + str(record.x_tiempo_cantidad) + " " + str(
                        dict(record._fields['x_tiempo_unidad'].selection).get(record.x_tiempo_unidad))
                    domicilio += " radicó en una vivienda"
                    if record.x_vivienda:
                        domicilio += " " + str(record.x_vivienda.x_name.encode('utf-8'))
                    domicilio += " ubicado en la dirección: "
                    if record.x_calle:
                        domicilio += str(record.x_calle.encode('utf-8')) + ", "
                    if record.x_colonia.name:
                        domicilio += str(record.x_colonia.name.encode('utf-8')) + ", "
                    if record.x_municipio.name:
                        domicilio += str(record.x_municipio.name.encode('utf-8')) + ", "
                    if record.x_estado_id.name:
                        domicilio += str(record.x_estado_id.name.encode('utf-8'))
                    text += domicilio + '\n'

        return text

    def sintesis_educativa(self):
        text = "Manifestó haber estudiado en:" + '\n'
        if self.x_entrevista_id.x_estudios_ids:
            for record in self.x_entrevista_id.x_estudios_ids:
                text += "Escolaridad: " + str(record.x_name.x_name.encode('utf-8')) + " "
                if record.x_institucion:
                    text += "en la institución: " + str(record.x_institucion.encode('utf-8')) + " "
                for rec in record.x_domicilio_ids:
                    domicilio = ",con domicilio en "
                    if rec.x_calle:
                        domicilio += str(rec.x_calle.encode('utf-8')) + ", "
                    if rec.x_colonia.name:
                        domicilio += str(rec.x_colonia.name.encode('utf-8')) + ", "
                    if rec.x_municipio.name:
                        domicilio += str(rec.x_municipio.name.encode('utf-8')) + ", "
                    if rec.x_estado_id.name:
                        domicilio += str(rec.x_estado_id.name.encode('utf-8'))
                    text += domicilio + '\n'
                if record.x_desercion:
                    text += "Motivos de desercion: " + str(record.x_desercion.encode('utf-8')) + '\n'

        return text

    def inf_destacada(self):
        text = ""
        if self.x_entrevista_id.x_consume_sustancias == 'si':
            if self.x_entrevista_id.x_sustancias_ids:
                text += "El entrevistado manisfestó consumir las siguientes sustancias:" + '\n'
                for record in self.x_entrevista_id.x_sustancias_ids:
                    text += str(record.x_name.x_name.encode('utf-8')) + " " + str(
                        record.x_cantidad.encode('utf-8')) + " " + str(
                        dict(record._fields['x_frecuencia'].selection).get(
                            record.x_frecuencia)) + " con última fecha de consumo en " + str(record.x_ultimo_consumo)

        return text

    x_conclusion_primero = fields.Text(
        string="Conclusión",
        default="Con base a los parámetro establecidos en la escala de riesgos y derivado de la verificación de campo y gabinete, se desprende el siguiente resultado:"+'\n'+"Los riesgos procesales son XXXX debido a:"
    )
    x_conclusion = fields.Text(
        string='Conclusión',
        default="Por lo que el nivel de riesgo (), la o las medidas cautelares que se pudieran solicitar para su imposición, estas deberán ser una herramienta que confirmen la protección a la comunidad, así como aseguren la comparecencia del entrevistado a los actos procesales que sea citado."+'\n'+'\n'+"El Plan de Supervición que se elaboraría tedría complejidad para supervisar por parte de esta Dirección de Medidad Cautelares, debido a las condiciones socio-ambientales del entrevistado."
    )    
    x_expedientes_ids = fields.Many2many(
        string=u'Registro de Antecedentes',
        comodel_name='umc_expedientes',
    )    
    x_expedientes_observaciones = fields.Text(
        string=u'Observaciones de Antecedentes',
    )    
    # ==========Campos para reporte==========
    x_name_abogado = fields.Char(
        string='Abogado',
    )
    x_puesto = fields.Char(
        string='Puesto',
    )
    x_historia_personal = fields.Text(
        string="Historia Personal"
    )
    x_actividades_desarrolladas = fields.Text(
        string='Tipo de actividades desarrolladas',
    )
    x_rel_familiares = fields.Text(
        string="Relaciones familiares"
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
    x_conc_sjp = fields.Text(
        string='Conocimiento del SJP',
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
    x_conc_nota = fields.Text(
        string='Nota',
    )
    x_conc_antecedentes = fields.Text(
        string="Antecedentes"
    )
    x_nombre_elav = fields.Char(
        string='Elaboró',
    )
    x_puesto_elav = fields.Char(
        string='Puesto',
    )
    x_seccion = fields.Char(
        string='Sección',
        default='11s'
    )
    x_serie = fields.Char(
        string='Serie',
        default='11S.3'
    )
    x_sub_serie = fields.Char(
        string='Subserie',
    )

    # ==========Default value==========
    x_parrafo = fields.Text(
        string='Presente',
        default='En atención al oficio X, asignado por el Abogado X, Agente del Ministerio Público Adscrito a la Unidad de Flagrancia de fecha, con fundamento en lo dispuesto por los articulos 153, 155, 156, 157, 158, 164, 168, 169 y 170 del Código Nacional de Procedimientos Penales: 65, 66, 67 y 68 de la Ley de Ejecucíón de Medidas Cautelares y Sanciones Penales para el Estado de Puebla y 17 fracción XIII y XIV de la Ley de Seguridad Pública del Estado; se emite la presente evaluación de riesgos del entrevistado X, dentro de la Carpeta de Investigación  X. Con base al resultado de la entrevista y recopilación de datos.',
    )
    x_parrafo_segundo = fields.Text(
        string="Análisis de riesgos",
        default="Al constituirse de manera física y legal en el área de xxxxx, y una vez que se realizó el conversatorio con el xxxxx, este expreso y  autorizó la recolección de datos  y su posterior comprobación; en razón de lo anterior siendo las xxxxx horas del xxxx procedió a realizar la entrevista"
    )
