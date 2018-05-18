# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class sup_mc_scp(models.Model):
    _name = 'sup_mc_scp'

    x_name = fields.Char('Registro', required=True, readonly=True,
                         default=lambda self: 'Nuevo'
                         )

    @api.model
    def create(self, vals):
        if vals.get('x_name', 'Nuevo') == 'Nuevo':
            vals['x_name'] = self.env['ir.sequence'].next_by_code(
                'sup_mc_scp') or'Nuevo'
        result = super(sup_mc_scp, self).create(vals)
        return result

    x_imputado_id = fields.Many2one(
        string=u'Imputado',
        comodel_name='res.partner',
        ondelete='restrict',
        readonly=True,
        required=True,
    )

    x_causa_penal = fields.Char(
        string=u'Causa Penal',
    )
    x_resolucion = fields.Selection(
        string=u'Resolución',
        selection=[('mc', 'MC'), ('scp', 'SCP'), ('otro', 'Otra')]
    )
    x_numero_oficio = fields.Char(
        string=u'Oficio número',
    )
    x_inicia = fields.Date(
        string=u'Fecha de Inicio',
        default=fields.Date.context_today,
    )
    x_finaliza = fields.Date(
        string=u'Fecha de Término',
        compute='calcular_fecha_finaliza',
        readonly=True,
        store=True,
    )
    x_tiempo_anios = fields.Integer(
        string=u'Años',
    )
    x_tiempo_meses = fields.Integer(
        string=u'Meses',
    )
    # 3
    # Función para calcular la fecha de finalización

    @api.depends('x_inicia', 'x_tiempo_anios', 'x_tiempo_meses')
    def calcular_fecha_finaliza(self):
        if self.x_inicia:
            start_date = fields.Datetime.from_string(self.x_inicia)
            if self.x_tiempo_anios > 0:
                start_date = start_date + \
                    relativedelta(years=self.x_tiempo_anios)
            if self.x_tiempo_meses > 0:
                start_date = start_date + \
                    relativedelta(months=self.x_tiempo_meses)
            self.x_finaliza = start_date

    x_supervisor_id = fields.Many2one(
        string=u'Supervisor',
        comodel_name='res.users',
        ondelete='set null',
        # domain="[('company_id','=',x_casa_justicia)]",
        #domain=lambda self: [( "groups_id", "=", self.env.ref( "UMECAS.umc_supervisor" ).id )]
        # no funciona domain=lambda self:[('company_id','=',self.env.x_casa_justicia)]
        domain=lambda self: ['&', ('company_id', '=', self.env.user.company_id.id), (
            "groups_id", "=", self.env.ref("UMECAS.umc_supervisor").id)]
    )

    x_foja = fields.Integer(
        string=u'Foja',
    )
    x_libro = fields.Char(
        string=u'Libro',
    )
    x_casa_justicia = fields.Many2one(
        string=u'Casa/Centro de Justicia',
        comodel_name='res.company',
        ondelete='set null',
        related='x_expediente_id.x_casa_justicia',
        readonly=True,
    )
    state = fields.Selection(
        [('orden', 'Orden sup.'),
         ('mc-scp', 'MC-SCP'),
         ('encuadre', 'Ent. Encuadre'),
         ('compromisos', 'Compromisos'),
         ('supervision', 'Supervisión'),
         ('informe', 'Informe'),
         ('terminado', 'Terminado'),
         ('archivado', 'Archivado')],
        default='orden',
        readonly=True, string=u'Estatus',
    )
    x_ultimasupervision = fields.Date(
        string=u'Ultima Supervisión',
    )
    @api.onchange('x_inicia')
    def get_fechainicia(self):
        #if not self.x_ultimasupervision:
        self.x_ultimasupervision = self.x_inicia
    
    x_incumplimiento_scp = fields.Boolean(
        string=u'Incumplimiento de MC/SCP',
        readonly=True,
        compute='get_incumplimiento'
    )

    @api.depends('x_scp_ids', 'x_mc_ids', 'x_resolucion')
    def get_incumplimiento(self):
        for record in self:
            record.x_incumplimiento_scp = False
            if record.x_resolucion == 'scp':
                if record.x_scp_ids:
                    for scp in record.x_scp_ids:
                        if not scp.cumplio_scp:
                            record.x_incumplimiento_scp = True                            
            elif record.x_resolucion == 'mc':
                if record.x_mc_ids:
                    for mc in record.x_mc_ids:
                        if not mc.cumplio_mc:
                            record.x_incumplimiento_scp = True
            elif record.x_resolucion == 'otro':
                if record.x_otro_ids:
                    for otro in record.x_otro_ids:
                        if not otro.cumplio_resolucion:
                            record.x_incumplimiento_scp = True
                            

    @api.multi
    def get_ultima_entrevista(self):
        entrevistas = self.env['umc_entrevistas'].search(
            [('x_imputado_id', '=', self.x_imputado_id.id)])
        if entrevistas:
            entrevista = entrevistas[-1]
            #domicilio_aux= ''
            # self.copy(domicilio_aux : entrevista.x_domicilio_actual.ids)
            # print "==============0--",domicilio_aux
            datos = {
                'x_sexo': entrevista.x_sexo,
                'x_lugar_nacimiento': entrevista.x_lugar_nacimiento,
                'x_fecha_nacimiento': entrevista.x_fecha_nacimiento,
                'x_estado_civil': entrevista.x_estado_civil,
                'x_estado_civil_otro': entrevista.x_estado_civil_otro,
                'x_telefono': entrevista.x_telefono,
                'x_telefono_otro': entrevista.x_telefono_otro,
                #'x_domicilio_actual':[(6,0,entrevista.x_domicilio_actual.ids)],
                #'x_enfermedades_ids':[(6,0,entrevista.x_enfermedades_ids.ids)],
                'x_discapacidad_padece': entrevista.x_discapacidad_padece,
                'x_discapacidad_id': entrevista.x_discapacidad_id.id,
                #'x_empleos_ids':[(6,0,entrevista.x_empleos_ids.ids)],
                #'x_contacto_ids':[(6,0,entrevista.x_contacto_ids.ids)],
                #'x_amistades_ids':[(6,0,entrevista.x_amistades_ids.ids)],
                #'x_actividades_ids':[(6,0,entrevista.x_actividades_ids.ids)],
                'x_consume_sustancias': entrevista.x_consume_sustancias,
                #'x_sustancias_ids':[(6,0,entrevista.x_sustancias_ids.ids)],
                'x_observaciones_actitud': entrevista.x_observaciones_actitud

            }
            partner = self.env['sup_entrevista_encuadre'].search(
                [('id', '=', self.x_encuadre_id.id)])
            #partner = self.copy(default={'x_domicilio_actual':entrevista.x_domicilio_actual.ids})
            partner.write(datos)

    @api.multi
    def capturar_medidas(self):
        self.state = 'mc-scp'

    @api.multi
    def generar_entrevista(self):
        if self.x_supervisor_id and not self.x_encuadre_id:
            self.state = 'encuadre'
            valores_entrevista = {'x_orden_id': self.id,
                                  'x_supervisor_id': self.x_supervisor_id.id,
                                  'x_imputado': self.x_imputado_id.id,
                                  #'x_casa_justicia': self.x_casa_justicia.id,
                                  #'x_cdi': self.x_expediente_id.x_cdi_nic,
                                  'x_numero_causa': self.x_causa_penal,
                                  'x_apellido_pat': self.x_imputado_id.ap_paterno,
                                  'x_apellido_mat': self.x_imputado_id.ap_materno,
                                  'x_nombre_entrevistado': self.x_imputado_id.name,
                                  'x_resolucion': self.x_resolucion,
                                  'x_delitos_id': (4, 0, self.x_expediente_id.x_delito)}
            res = self.env['sup_entrevista_encuadre'].create(
                valores_entrevista)
            self.x_encuadre_id = res
            self.get_ultima_entrevista()
            return res
        else:
            if self.x_supervisor_id and self.x_encuadre_id:
                self.state = 'encuadre'
                partner = self.env['sup_entrevista_encuadre'].search(
                    [('id', '=', self.x_encuadre_id.id)])
                valores_entrevista = {'x_orden_id': self.id,
                                      'x_supervisor_id': self.x_supervisor_id.id,
                                      'x_imputado': self.x_imputado_id.id,
                                      #'x_casa_justicia': self.x_casa_justicia.id,
                                      #'x_cdi': self.x_expediente_id.x_cdi_nic,
                                      'x_numero_causa': self.x_causa_penal,
                                      'x_apellido_pat': self.x_imputado_id.ap_paterno,
                                      'x_apellido_mat': self.x_imputado_id.ap_materno,
                                      'x_nombre_entrevistado': self.x_imputado_id.name,
                                      'x_resolucion': self.x_resolucion,
                                      'x_delitos_id': [(6, 0, self.x_expediente_id.x_delito.ids)]}
                partner.write(valores_entrevista)

    @api.multi
    def regresar_capturar_medidas(self):
        self.state = 'mc-scp'
        # print "////////////////////delitos",self.x_expediente_id.x_delito.ids
        # self.get_ultima_entrevista()
    #///////////////////////////////// Supervisión
    #///////////////////////////////// Supervisión
    #///////////////////////////////// Supervisión

    x_supervisado = fields.Boolean(
        string=u'Supervisado',
    )
    x_tipovisita_id = fields.Many2one(
        string=u'Tipo Visita',
        comodel_name='sup_tipo_visita',
        ondelete='set null',
    )
    x_cumplio = fields.Boolean(
        string=u'Cumplió',
    )

    #///////////////////////////////// Datos generales
    #///////////////////////////////// Datos generales
    #///////////////////////////////// Datos generales
    x_tipo_imputado = fields.Selection(
        [('retenido', 'Retenido'), ('adolescente',
                                    'Adolescente'), ('interno', 'Interno')],
        string=u'Tipo de imputado',
        related='x_imputado_id.x_imputado_tipo',
        readonly=True,
        store=True,
    )
    x_imputado_sexo = fields.Selection(
        string=u'Sexo',
        selection=[('m', 'Masculino'), ('f', 'Femenino'), ('o', 'Otro')],
        related='x_imputado_id.x_sexo',
        store=True,
        readonly=True,
    )
    x_imputado_edad = fields.Integer(
        string=u'Edad',
        related='x_imputado_id.edad',
        store=True,
        readonly=True,
    )
    x_colonia_imputado = fields.Many2one(
        string=u'Colonia',
        comodel_name='umc_colonia',
        ondelete='set null',
        related='x_imputado_id.street2',
        store=True,
        readonly=True,
    )
    x_sector_imputado = fields.Selection(
        string=u'Sector',
        selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')],
        related='x_imputado_id.street2.x_sector',
        store=True,
        readonly=True
    )
    x_municipio_imputado = fields.Many2one(
        string=u'Municipio',
        comodel_name='umc_municipio',
        ondelete='set null',
        related='x_imputado_id.city',
        store=True,
        readonly=True,
    )
    x_ruta_imputado = fields.Integer(
        string=u'Ruta',
        related='x_imputado_id.city.x_ruta',
        store=True,
        readonly=True,
    )

    #///////////////////////////////// Medidas Cautelares
    #///////////////////////////////// Medidas Cautelares
    #///////////////////////////////// Medidas Cautelares

    x_mc_ids = fields.One2many(
        string=u'Medidas Cautelares',
        comodel_name='sup_mc_lines',
        inverse_name='x_registro_id',
    )
    #///////////////////////////////// SCP
    #///////////////////////////////// SCP
    #///////////////////////////////// SCP
    #///////////////////////////////// SCP

    x_scp_ids = fields.One2many(
        string=u'SCP',
        comodel_name='sup_scp_lines',
        inverse_name='x_registro_id',
    )
    #///////////////////////////////// otro
    #///////////////////////////////// otro
    #///////////////////////////////// otro
    #///////////////////////////////// otro

    x_otro_ids = fields.One2many(
        string=u'otro',
        comodel_name='sup_otro_lines',
        inverse_name='x_registro_id',
    )
    #///////////////////////////////// Entrevista encuadre
    #///////////////////////////////// Entrevista encuadre
    #///////////////////////////////// Entrevista encuadre
    #///////////////////////////////// Entrevista encuadre

    x_encuadre_id = fields.Many2one(
        string=u'Entrevista de Encuadre',
        comodel_name='sup_entrevista_encuadre',
        readonly=True,
        ondelete='restrict',
    )
    x_encuadre_status = fields.Selection(
        string=u'Estatus de Entrevista',
        readonly=True,
        related='x_encuadre_id.state',
    )
    #///////////////////////////////// Visita periodica
    #///////////////////////////////// Visita periodica
    #///////////////////////////////// Visita periodica
    #///////////////////////////////// Visita periodica

    """x_eventos_ids = fields.One2many(
        string=u'Eventos',
        comodel_name='calendar.event',
        inverse_name='x_supervision_id',
    )"""

    x_eventos_ids = fields.Many2many(
        string=u'Eventos Programados',
        comodel_name='calendar.event',
    )

    x_eventos = fields.Integer(
        string=u'Eventos',
        compute='compute_registros_count',
        # store=True,
    )

    @api.multi
    def compute_registros_count(self):
        for contador in self:
            contador.x_eventos = self.env['calendar.event'].search_count(
                [('x_supervision_id', '=', contador.id)])

    #/////////////////////////////////Informe Supervisor
    #/////////////////////////////////Informe Supervisor
    #/////////////////////////////////Informe Supervisor
    #/////////////////////////////////Informe Supervisor

    x_informe_html = fields.Html(
        string=u'Informe',

        default=lambda self: self.html_default(),

    )

    def html_default(self):
        codigo = '<p> Estimado  texto de prueba </p> '
        codigo += '<p>Línea 2</p><br>'
        return codigo

    #///////////////////////////////////////////// campo relacional con expedientes
    #///////////////////////////////////////////// campo relacional con expedientes
    #///////////////////////////////////////////// campo relacional con expedientes

    x_expediente_id = fields.Many2one(
        string=u'Expediente ID',
        comodel_name='umc_expedientes',
        ondelete='cascade',
        readonly=True,
    )
    x_nombre_apoyo_moral = fields.Char(
        string='Nombre del apoyo moral',
    )
    x_parentesco_id = fields.Many2one(
        'umc_parentesco',
        string='Relación con el imputado',
    )

    x_compromiso_documento_id = fields.Many2one(
        string=u'Carta compromiso',
        comodel_name='sup_documentos',
        readonly=True,
        ondelete='restrict',
    )
    x_apoyo_documento_id = fields.Many2one(
        string=u'Apoyo moral',
        comodel_name='sup_documentos',
        readonly=True,
        ondelete='restrict',
    )
    x_informe_id = fields.Many2one(
        string=u'Informe',
        comodel_name='sup_documentos',
        readonly=True,
        ondelete='restrict',
    )
    x_actas_ids = fields.One2many(
        'sup_documentos',
        'x_orden_id',
        string='Actas circunstanciadas',
        ondelete='restrict',
    )
    default_acta = fields.Html(
        string='Contenido',
        default=lambda self: self.default_acta_text(),
    )
    x_lista_mc_scp = fields.Char(
        string='Lista',
    )

    #////////////////////////////////CARTAS Y/O DOCUMENTOS//////////////////////////////

    @api.multi
    def generar_carta_compromiso(self):
        if not self.x_compromiso_documento_id:
            res_model = str(self.__class__.__name__)
            valores_documento = {
                'x_orden_name': self.x_name,
                'x_res_model': res_model,
                'x_modelo_id': self.id,
                'x_imputado_id': self.x_imputado_id.id,
                'x_causa_penal': self.x_causa_penal,
                'x_supervisor_id': self.x_supervisor_id.id,
                'x_tipo_documento': 'Carta compromiso'
            }
            res = self.env['sup_documentos'].create(valores_documento)
            self.x_compromiso_documento_id = res
            self.x_compromiso_documento_id.carta_compromiso()
            return res

    @api.multi
    def generar_carta_apoyo_moral(self):
        if self.x_compromiso_documento_id and not self.x_apoyo_documento_id:
            res_model = str(self.__class__.__name__)
            self.state = 'compromisos'
            valores_documento = {
                'x_orden_name': self.x_name,
                'x_res_model': res_model,
                'x_modelo_id': self.id,
                'x_imputado_id': self.x_imputado_id.id,
                'x_causa_penal': self.x_causa_penal,
                'x_supervisor_id': self.x_supervisor_id.id,
                'x_parentesco_id': self.x_parentesco_id.id,
                'x_nombre_apoyo_moral': self.x_nombre_apoyo_moral,
                'x_tipo_documento': 'Carta compromiso del apoyo moral'
            }
            res = self.env['sup_documentos'].create(valores_documento)
            self.x_apoyo_documento_id = res
            self.x_apoyo_documento_id.carta_apoyo_moral()
            return res
        elif self.x_compromiso_documento_id:
            self.state = 'compromisos'

    @api.multi
    def generar_actas(self):
        if self.x_apoyo_documento_id:
            self.state = 'supervision'

    @api.multi
    def generar_informe(self):
        if not self.x_informe_id:
            res_model = str(self.__class__.__name__)
            self.state = 'informe'
            self.get_mc()
            valores_documento = {
                'x_orden_name': self.x_name,
                'x_res_model': res_model,
                'x_modelo_id': self.id,
                'x_imputado_id': self.x_imputado_id.id,
                'x_lista_mc_scp': self.x_lista_mc_scp,
                'x_tipo_documento': 'Informe'
            }
            res = self.env['sup_documentos'].create(valores_documento)
            self.x_informe_id = res
            self.x_informe_id.informe_html()
            return res
        elif self.x_informe_id:
            self.state = 'informe'

    def default_acta_text(self):
        default_code = """
        <div class="text-center">
            <h4>ACTA CIRCUNSTANCIADA()</h4>
        </div>
        <p style="font-size:12px;">
            En la ciudad de Puebla, Puebla siendo las __________ horas del día __________ de __________ del __________, el (los) Supervisor(es) ______________________________ y ______________________________, adscrito(s) a la 
            Dirección de Medidas Cautelares y Policía Procesal dependiente de la Dirección General de Centros de Reinserción Social del Estado, con domicilio en Prolongación 11 sur, número
            11921, Colonia Ex-Hacienda Castillotla, Puebla; quién(es) actúa(n) legalmente con testigos de asistencia, siendo los (las) CC. ______________________________ y ______________________________, 
            en consecuencia y fundamentos de los artículos 14, 20 inciso c) fracción VI, 21 de la Constitución Política de los Estados
            Unidos Mexicanos, 153, 154, 155, 157, 164. 169, 170, 177, 191, 192, 195 Y demás relativos y aplicables del Código Nacional de Procedimientos Penales; 29 del Código de Procedimientos Civiles, 
            de aplicación supletoria en términos del artículo 5 fracción VII, 17 Fracciones XIII y XIV de la Ley de Segundad Pública, 7 fracciones V, VII, XII y XIX,
             8 y 30 Bis fracciones del Reglamento Interior de la Secretaría de Seguridad Pública todas para el Estado de Puebla.
        </p>
        <p style="font-size:12px;">
            A efecto de supervisar al C. ____________________________________________________________ 
            nos constituimos legalmente en el domicilio que obra en actuaciones dentro del expediente administrativo en que se actúa, ubicado en la calle ____________________________________________________________ número __________
            de la colonia ______________________________ del municipio de ______________________________, por lo que una vez que nos cercioramos plena y legalmente de ser éste el domicilio de la citada persona 
            (víctima, ofendido o testigo), por así indicarlo la nomenclatura, de la calle y el número de la casa, el cual tiene las siguientes características 
            ________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
            , se procede a tocar en la puerta de acceso de dicho inmueble, siendo atendidos por el(a) C.____________________________________________________________, con la siguiente fisonomía __________________________________________________________________________________________,
            quién dijo ser ______________________________ del supervisado mismo(a) que se identifica con ____________________________________________________________, previa copia simple de la misma para constancia 
            y al preguntar por el (la) C. ______________________________________________________________________________________ manifestó:
            ________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
        </p>
        <p style="font-size:12px;">
            Lo que se hace constar para los efectos legales correspondientes, firmando al calce los que en esta intervinieron para constancia legal con lo antenor se da por terminada la presente 
            acta de supervisión siendo las ___________ del día en que se actúa.
        </p>
        <br>
        <br>
        <div class="row">
            <div class="col-xs-6 text-center">
                ________________________________________
                <p> T. DE A.</p>
            </div>
            <div class="col-xs-6 text-center">
                ________________________________________
                <p>SUPERVISOR</p>
            </div>
        </div>
        <br>
        <div class="row">
            <div class="col-xs-6 text-center">
                ________________________________________
               <p> T. DE A.</p>
            </div>
            <div class="col-xs-6 text-center">
                ________________________________________
                <p>SUPERVISOR</p>
            </div>
        </div>
        """
        return default_code

    def get_mc(self):
        if self.x_resolucion == 'mc':
            n = 1
            lista = """
                    <div style='padding:20px;'>
                """
            for mc in self.x_mc_ids:
                lista += "<p>" + str(n) + '.- ' + mc.descripcion + "</p>"
                n = n + 1
            lista += "</div>"
            self.x_lista_mc_scp = lista

        elif self.x_resolucion == 'scp':
            n = 1
            lista = """
                    <div style='padding:20px;'>
                """
            for scp in self.x_scp_ids:
                lista += "<p>" + str(n) + '.- ' + scp.descripcion + "</p>"
                n = n + 1
            lista += "</div>"
            self.x_lista_mc_scp = lista

        elif self.x_resolucion == 'otro':
            n = 1
            lista = """
                    <div style='padding:20px;'>
                """
            for otro in self.x_otro_ids:
                lista += "<p>" + str(n) + '.- ' + otro.name + "</p>"
                n = n + 1
            lista += "</div>"
            self.x_lista_mc_scp = lista
