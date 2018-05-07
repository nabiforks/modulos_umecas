# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, date
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
    x_tipo_imputado = fields.Selection(
        [('retenido', 'Retenido'), ('adolescente',
                                    'Adolescente'), ('interno', 'Interno')],
        string=u'Tipo de imputado',
        related='x_imputado_id.x_imputado_tipo',
        readonly=True,
    )
    x_causa_penal = fields.Char(
        string=u'Causa Penal',
    )
    x_resolucion = fields.Selection(
        string=u'Resolución',
        selection=[('mc', 'MC'), ('scp', 'SCP')]
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
        default=fields.Date.context_today,
    )
    x_tiempo = fields.Char(
        string=u'Tiempo',
    )

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
         ('informe', 'Informe'),
         ('terminado', 'Terminado'),
         ('cancelado', 'Cancelado')],
        default='orden',
        readonly=True, string=u'Estatus',
    )
    @api.multi
    def get_ultima_entrevista(self):
        entrevistas=self.env['umc_entrevistas'].search([('x_imputado_id', '=', self.x_imputado_id.id)])
        if entrevistas:
            entrevista = entrevistas[-1]
            #domicilio_aux= ''
            #self.copy(domicilio_aux : entrevista.x_domicilio_actual.ids)
            #print "==============0--",domicilio_aux
            datos={
                'x_sexo':entrevista.x_sexo,
                'x_lugar_nacimiento':entrevista.x_lugar_nacimiento,
                'x_fecha_nacimiento':entrevista.x_fecha_nacimiento,
                'x_estado_civil':entrevista.x_estado_civil,
                'x_estado_civil_otro':entrevista.x_estado_civil_otro,
                'x_telefono':entrevista.x_telefono,
                'x_telefono_otro':entrevista.x_telefono_otro,
                #'x_domicilio_actual':[(6,0,entrevista.x_domicilio_actual.ids)],
                #'x_enfermedades_ids':[(6,0,entrevista.x_enfermedades_ids.ids)],
                'x_discapacidad_padece':entrevista.x_discapacidad_padece,
                'x_discapacidad_id':entrevista.x_discapacidad_id.id,
                #'x_empleos_ids':[(6,0,entrevista.x_empleos_ids.ids)],
                #'x_contacto_ids':[(6,0,entrevista.x_contacto_ids.ids)],
                #'x_amistades_ids':[(6,0,entrevista.x_amistades_ids.ids)],
                #'x_actividades_ids':[(6,0,entrevista.x_actividades_ids.ids)],
                'x_consume_sustancias':entrevista.x_consume_sustancias,
                #'x_sustancias_ids':[(6,0,entrevista.x_sustancias_ids.ids)],
                'x_observaciones_actitud':entrevista.x_observaciones_actitud

            }
            partner = self.env['sup_entrevista_encuadre'].search([('id', '=', self.x_encuadre_id.id)])
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
                                  'x_resolucion':self.x_resolucion,
                                  'x_delitos_id':(4,0,self.x_expediente_id.x_delito)}
            res = self.env['sup_entrevista_encuadre'].create(valores_entrevista)
            self.x_encuadre_id = res
            self.get_ultima_entrevista()
            return res
        else:
            if self.x_supervisor_id and self.x_encuadre_id:
                self.state = 'encuadre'
                partner = self.env['sup_entrevista_encuadre'].search([('id', '=', self.x_encuadre_id.id)])
                valores_entrevista = {'x_orden_id': self.id,
                                    'x_supervisor_id': self.x_supervisor_id.id,
                                    'x_imputado': self.x_imputado_id.id,
                                    #'x_casa_justicia': self.x_casa_justicia.id,
                                    #'x_cdi': self.x_expediente_id.x_cdi_nic,
                                    'x_numero_causa': self.x_causa_penal,
                                    'x_apellido_pat': self.x_imputado_id.ap_paterno,
                                    'x_apellido_mat': self.x_imputado_id.ap_materno,
                                    'x_nombre_entrevistado': self.x_imputado_id.name,
                                    'x_resolucion':self.x_resolucion,
                                    'x_delitos_id':[(6,0,self.x_expediente_id.x_delito.ids)]}
                partner.write(valores_entrevista)
            
    @api.multi
    def regresar_capturar_medidas(self):
        self.state = 'mc-scp'
        #print "////////////////////delitos",self.x_expediente_id.x_delito.ids
        #self.get_ultima_entrevista()
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
        store=True,        
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
        codigo='<p> Estimado  texto de prueba </p> '
        codigo+='<p>Línea 2</p><br>'
        return codigo
    
    #////////////////////////////////Carta de compromiso y apoyo moral
    x_compromiso_html = fields.Html(
        string='Carta compromiso',
        default=lambda self: self.carta_compromiso(),
    )
    x_apoyo_moral_html = fields.Html(
        string='Apoyo a la moral',
        default=lambda self: self.carta_apoyo_moral(),
    )
    def carta_compromiso(self):
        default_code="""
            <h4>DIRECCIÓN DE MEDIDAS CAUTELARES Y POLICÍA PROCESAL ÁREA DE SUPERVISIÓN</h4>
            <h4>CARTA-COMPROMISO DEL IMPUTADO</h4>
            <br/>
            <strong>Entiendo que:</strong>
            <ul">
                <li>
                    <p>
                        El(los) supervisor(es) de la Unidad de Medidas Cautelares estará(n) en comunicación constante conmigo y con mi familia
                        , mediante llamadas telefónicas, visitas domiciliarias, entrevistas o cualquier otro medio electrónico contemplado en el
                        plan de supervisión y/o atribuciones contemplada en el Artículo 177 del Código Penal Nacional de Procedimientos Penales
                        mismas que se me han dado lectura y he comprendido para asegurar que estoy cumpliendo con las Medidas Cautelares o con 
                        la Suspensión Condicional del Proceso impuestas por el Juez de Control en el número de causa ___________________.
                    </p>
                </li>
                <li>
                    <p>
                        El(los) supervisor(es) de la Unidad de Medidas Cautelares intercambiará información con la institución designada por el 
                        Juez de Control para mi supervisión, con la finalidad de verificar que se cumplan las Medidas Cautelares o con la Suspensión 
                        Condicional del Proceso en el citado número de causa.
                    </p>
                </li>
                <li>
                    <p>
                        Cualquier incumplimiento de las Medidas Cautelares o con la Suspensión Condicional del Proceso impuesta por el Juez de Control
                        será informado al mismo, así como al Ministerio Público y a mi Defensor.
                    </p>
                </li>
                <li>
                    <p>
                        En caso de incumplimiento de informará al Ministerio Público y a mi Defensor; y el Juez de Control decidirá sobre la modificación 
                        de la(s) Medida(s) Cautelar(es) que me fueron impuestas por otras más restrictivas.
                    </p>
                </li>
            </ul>
            <strong>Me comprometo a:</strong>
            <ul>
                <li>
                    <p>Presentarme en cada audiencia que se requiera durante mi Proceso Penal.</p>
                </li>
                <li>
                    <p>Cumplir con las Medidas Cautelares o con las Condiciones impuestas por el Juez de Control, a partir de esta fecha.</p>
                </li>
                <li>
                    <p>
                        Entregar la documentación que me sea requerida por parte del (los) supervisor(es) en tiempo y forma, la cual acredite el cumplimiento 
                        de las Medidas Cautelares o Condiciones que me comprometí a cumplir.
                    </p>
                </li>
                <li>
                    <p>Avisar a mi supervisor de cualquier cambioen mi entorno socio-ambiental (domicilio, número de teléfono celular y/o fijo, empleo  u otro).</p>
                </li>
                <li>
                    <p>
                        Mantener comunicación con mi supervisor asignado por los medios estipulados en esta entrevista (llamadas telefónicas, visitas a las oficinas 
                        de Medidas Cautelares en caso de tener alguna duda en cuanto al cumplimiento, visitas domiciliarias o cualquier otra vía necesaria).
                    </p>
                </li>
                <li>
                    <p>
                        Informar al personal de Supervisión de inmediato de cualquier circunstancia que dificulte el cumplimiento de las Medidas Cautelares 
                        o Condiciones impuestas.
                    </p>
                </li>
                <li>
                    <p>
                    A proporcionar las facilidades para el desarrollo de las visitas no anuncuadas al domicilio particular, laboral, habitual o algun otro que 
                    sea necesario (sin menoscabo de lo establecido por el artículo 266 de Código Nacional de Procedimientos Penales).
                    </p>
                </li>
            </ul>
            <strong>Autorizó a:</strong>
            <ul>
                <li>
                    <p>
                    Personal de la dirección de Medidas Cautelares y Policía Procesal, realizar actuaciones apegadas a sus atribuciones así como verificar la validez 
                    de la documentación tanto pública como privada que exhiba como soporte de mi cumplimiento de las Medidas Cautelares y/o Condiciones que me fueron 
                    impuestas.
                    </p>
                </li>
            </ul>
            <br>
            <strong>
                <p>
                Enterado y comprendido lo anterior así como de las consecuencias que implicaría mi acción, omisión y/o desinterés respecto a las Medidas Cautelares 
                o Condiciones que me comprometí a cumplir; firmo de conformidad.
                </p>
            </strong>
            <br>
            <br>
            <p>NOMBRE DEL IMPUTADO:       __________________________________</p>
            <p>NOMBRE DEL SUPERVISAR:__________________________________</p>
        """
        return default_code   
    
    def carta_apoyo_moral(self):
        apoyo_code = """
            <h4>CARTA COMPROMISO DEL APOYO MORAL</h4>
            <br>
            <strong>Entiendo que:</strong>
            <ul>
                <li>
                    <p>
                    A partir de esta fecha me comprometo a apoyar y ayudar a __________________________________ para que cumpla con las medidas cautelares o con la suspensíon condicional 
                    del proceso a prueba que le fueron impuestas por el Juez en su proceso penal.
                    </p>
                </li>
                <li>
                    <p>
                        El Supervisor de Medidas Cautelares podrá solicitarme cualquier información sobre el comportamiento de __________________________________ con la finalidad de verificar 
                        que se cumplan las medidas cautelares o suspensión condicional del proceso a prueba impuestas.
                    </p>
                </li>
            </ul>
            <strong>Me comprometo a:</strong>
            <ul>
                <li>
                    <p>
                    Apoyar y ayudar a __________________________________ quien es mi __________________________________, cumpla con las medidas cautelares o suspensión 
                    condicional del proceso a prueba impuestas por el Juez tendientes a garantizar su presencia en el proceso judicial que enfrenta.
                    </p>
                </li>
                <li>
                    <p>
                    Mantener comunicación con el supervisor asignado, por los medios estipulados en esta entrevista. (Llamadas telefónicas, visitas domiciliarias, 
                    correos electrónicos, mensajes de texto y etc.).
                    </p>
                </li>
                <li>
                    <p>
                    Informar inmediatamente al Supervisor de Medidas Cautelares por cualquier incumplimiento por parte de __________________________________.
                    </p>
                </li>
                <li>
                    <p>
                    Informar al Supervisor de Medidas Cautelares de forma inmediata en caso de que haya cambiado de mi domicilio, mi numero de teléfono celular y/o fijo 
                    o del imputado.
                    </p>
                </li>
                <li>
                    <p>
                    Motivar a __________________________________ para que asista a todas las audiencias y cumpla con las imposiciones judiciales.
                    </p>
                </li>
            </ul>
            <br>
            <br>
            <p>NOMBRE DEL APOYO MORAL: __________________________________</p>
            <p>NOMBRE DEL SUPERVISOR:     __________________________________</p>
        """
        return apoyo_code

    #///////////////////////////////////////////// campo relacional con expedientes
    #///////////////////////////////////////////// campo relacional con expedientes
    #///////////////////////////////////////////// campo relacional con expedientes

    x_expediente_id = fields.Many2one(
        string=u'Expediente ID',
        comodel_name='umc_expedientes',
        ondelete='cascade',
        readonly=True,
    )
