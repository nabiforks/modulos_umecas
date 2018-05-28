# -*- coding: utf-8 -*-

from odoo import api, fields, models

class sup_documentos(models.Model):
    _name = 'sup_documentos'

    x_name = fields.Char(
        string='Nombre',
        readonly=True, 
        required=True,
        default=lambda self: 'Nuevo'
    )
    x_contenido = fields.Html(
        string='Contenido',
        #default=lambda self: self.tipo_contenido(),
    )
    x_modelo_id = fields.Char(
        string='ID del Recurso',
        readonly=True, 
    )
    x_orden_name = fields.Char(
        string=u'Orden de Supervisión',
        readonly=True,        
    )
    x_orden_id = fields.Many2one(
        'sup_mc_scp',
        string='Supervisión',
    )
    x_res_model = fields.Char(
        string='Modelo relacionado',
        readonly=True, 
    )
    x_fecha_documento = fields.Date(
        string='Fecha',
        default=fields.Date.today()
    )
    x_tipo_documento = fields.Char(
        string='Tipo documento',
    )
    x_imputado_id = fields.Many2one(
        'res.partner',
        string='Imputado',
        readonly=True, 
    )
    x_supervisor_id = fields.Many2one(
        'res.users',
        string='Supervisor',
        readonly=True, 
    )
    x_causa_penal = fields.Char(
        string='Causa penal',
        readonly=True, 
    )
    x_nombre_apoyo_moral = fields.Char(
        string='Nombre del apoyo moral',
    )
    x_parentesco_id = fields.Many2one(
        'umc_parentesco',
        string='Parentesco con el imputado',
    )
    
    x_lista_mc_scp = fields.Char(
        string='Lista',
    )
    x_print_clasificacion = fields.Boolean(
        
    )
    x_print_clasificacion = fields.Selection(
        string='¿Imprimir clasificación achivística?',
        selection=[('si', 'Si'), ('no', 'No')],
        default='si'
    )
    seccion = fields.Char(
        string='Sección',
        default='11S',
    )
    serie = fields.Char(
        string='Serie',
        default='11S.2',
    )
    sub_serie = fields.Char(
        string='Subserie',
    )

    @api.model
    def create(self, vals):
        if vals.get('x_name', 'Nuevo') == 'Nuevo':
            vals['x_name'] = self.env['ir.sequence'].next_by_code(
                'sup_documentos') or'Nuevo'
        result = super(sup_documentos, self).create(vals)
        return result
     
   
    def carta_compromiso(self):
    	nombre_imputado = self.x_imputado_id.display_name
    	nombre_sup = self.x_supervisor_id.name
        default_code="""
            <div class="row">
                <div class="col-xs-2"></div>
                <div class="col-xs-8 text-center">
                   <h4>DIRECCIÓN DE MEDIDAS CAUTELARES Y POLICÍA PROCESAL ÁREA DE SUPERVISIÓN</h4>
                   <br>
                    <h4>CARTA-COMPROMISO DEL IMPUTADO</h4>
                </div>
                <div class="col-xs-2"></div>
            </div>
            <br/>
            <strong>Entiendo que:</strong>
            <ul>
                <li>
                    <p class="text-justify">
                        El(los) supervisor(es) de la Unidad de Medidas Cautelares estará(n) en comunicación constante conmigo y con mi familia
                        , mediante llamadas telefónicas, visitas domiciliarias, entrevistas o cualquier otro medio electrónico contemplado en el
                        plan de supervisión y/o atribuciones contemplada en el Artículo 177 del Código Penal Nacional de Procedimientos Penales
                        mismas que se me han dado lectura y he comprendido para asegurar que estoy cumpliendo con las Medidas Cautelares o con 
                        la Suspensión Condicional del Proceso impuestas por el Juez de Control en el número de causa """+str(self.x_causa_penal)+""".
                    </p>
                </li>
                <li>
                    <p class="text-justify">
                        El(los) supervisor(es) de la Unidad de Medidas Cautelares intercambiará información con la institución designada por el 
                        Juez de Control para mi supervisión, con la finalidad de verificar que se cumplan las Medidas Cautelares o con la Suspensión 
                        Condicional del Proceso en el citado número de causa.
                    </p>
                </li>
                <li>
                    <p class="text-justify">
                        Cualquier incumplimiento de las Medidas Cautelares o con la Suspensión Condicional del Proceso impuesta por el Juez de Control
                        será informado al mismo, así como al Ministerio Público y a mi Defensor.
                    </p>
                </li>
                <li>
                    <p class="text-justify">
                        En caso de incumplimiento de informará al Ministerio Público y a mi Defensor; y el Juez de Control decidirá sobre la modificación 
                        de la(s) Medida(s) Cautelar(es) que me fueron impuestas por otras más restrictivas.
                    </p>
                </li>
            </ul>
            <strong>Me comprometo a:</strong>
            <ul>
                <li>
                    <p class="text-justify">Presentarme en cada audiencia que se requiera durante mi Proceso Penal.</p>
                </li>
                <li>
                    <p class="text-justify">Cumplir con las Medidas Cautelares o con las Condiciones impuestas por el Juez de Control, a partir de esta fecha.</p>
                </li>
                <li>
                    <p class="text-justify">
                        Entregar la documentación que me sea requerida por parte del (los) supervisor(es) en tiempo y forma, la cual acredite el cumplimiento 
                        de las Medidas Cautelares o Condiciones que me comprometí a cumplir.
                    </p>
                </li>
                <li>
                    <p class="text-justify">Avisar a mi supervisor de cualquier cambioen mi entorno socio-ambiental (domicilio, número de teléfono celular y/o fijo, empleo  u otro).</p>
                </li>
                <li>
                    <p class="text-justify">
                        Mantener comunicación con mi supervisor asignado por los medios estipulados en esta entrevista (llamadas telefónicas, visitas a las oficinas 
                        de Medidas Cautelares en caso de tener alguna duda en cuanto al cumplimiento, visitas domiciliarias o cualquier otra vía necesaria).
                    </p>
                </li>
                <li>
                    <p class="text-justify">
                        Informar al personal de Supervisión de inmediato de cualquier circunstancia que dificulte el cumplimiento de las Medidas Cautelares 
                        o Condiciones impuestas.
                    </p>
                </li>
                <li>
                    <p class="text-justify">
                    A proporcionar las facilidades para el desarrollo de las visitas no anuncuadas al domicilio particular, laboral, habitual o algun otro que 
                    sea necesario (sin menoscabo de lo establecido por el artículo 266 de Código Nacional de Procedimientos Penales).
                    </p>
                </li>
            </ul>
            <strong>Autorizó a:</strong>
            <ul>
                <li>
                    <p class="text-justify">
                    Personal de la dirección de Medidas Cautelares y Policía Procesal, realizar actuaciones apegadas a sus atribuciones así como verificar la validez 
                    de la documentación tanto pública como privada que exhiba como soporte de mi cumplimiento de las Medidas Cautelares y/o Condiciones que me fueron 
                    impuestas.
                    </p>
                </li>
            </ul>
            <br>
            <strong>
                <p class="text-justify">
                Enterado y comprendido lo anterior así como de las consecuencias que implicaría mi acción, omisión y/o desinterés respecto a las Medidas Cautelares 
                o Condiciones que me comprometí a cumplir; firmo de conformidad.
                </p>
            </strong>
            <br>
            <br>
            <p class="text-justify">NOMBRE DEL IMPUTADO:  <strong>"""+nombre_imputado.encode('utf-8')+"""</strong></p>
            <div class="row">
            	<div class="col-xs-8">
            		Firma:_______________________________
            	</div>
            	<div class="col-xs-4">
            		Fecha: <strong>"""+str(self.x_fecha_documento)+"""</strong>
            	</div>
            </div>
            <br>
            <div class="row">
            	<div class="col-xs-8">
           			 <p class="text-justify">NOMBRE DEL SUPERVISOR:  <strong>"""+nombre_sup.encode('utf-8')+"""</strong></p>
            	</div>
            	<div class="col-xs-4">
            		Firma:_______________________________
            	</div>
            </div>
        """
        self.x_contenido = default_code

    def carta_apoyo_moral(self):
    	nombre_imputado = self.x_imputado_id.display_name
    	nombre_sup = self.x_supervisor_id.name
        nombre_a_moral = "_________________________"
    	parentesco = "_________________________"

        if self.x_nombre_apoyo_moral:
            nombre_a_moral = self.x_nombre_apoyo_moral
        if self.x_parentesco_id:
            parentesco = self.x_parentesco_id.x_name
        default_code = """
            <div class="row">
                <div class="col-xs-2"></div>
                <div class="col-xs-8 text-center">
                    <h4>DIRECCIÓN DE MEDIDAS CAUTELARES Y POLICÍA PROCESAL ÁREA DE SUPERVISIÓN</h4>
                    <br>
                    <h4>CARTA COMPROMISO DEL APOYO MORAL</h4>
                </div>
                <div class="col-xs-2"></div>
            </div>
            <br/>
            <strong>Entiendo que:</strong>
            <ul>
                <li>
                    <p class="text-justify">
                    A partir de esta fecha me comprometo a apoyar y ayudar a  <strong>"""+nombre_imputado.encode('utf-8')+"""</strong> para que cumpla con las medidas cautelares o con la suspensíon condicional 
                    del proceso a prueba que le fueron impuestas por el Juez en su proceso penal.
                    </p>
                </li>
                <li>
                    <p class="text-justify">
                        El Supervisor de Medidas Cautelares podrá solicitarme cualquier información sobre el comportamiento de  <strong>"""+nombre_imputado.encode('utf-8')+"""</strong> con la finalidad de verificar 
                        que se cumplan las medidas cautelares o suspensión condicional del proceso a prueba impuestas.
                    </p>
                </li>
            </ul>
            <strong>Me comprometo a:</strong>
            <ul>
                <li>
                    <p class="text-justify">
                    Apoyar y ayudar a  <strong>"""+nombre_imputado.encode('utf-8')+"""</strong> quien es mi <strong>"""+parentesco.encode('utf-8')+"""</strong>, cumpla con las medidas cautelares o suspensión 
                    condicional del proceso a prueba impuestas por el Juez tendientes a garantizar su presencia en el proceso judicial que enfrenta.
                    </p>
                </li>
                <li>
                    <p class="text-justify">
                    Mantener comunicación con el supervisor asignado, por los medios estipulados en esta entrevista. (Llamadas telefónicas, visitas domiciliarias, 
                    correos electrónicos, mensajes de texto y etc.).
                    </p>
                </li>
                <li>
                    <p class="text-justify">
                    Informar inmediatamente al Supervisor de Medidas Cautelares por cualquier incumplimiento por parte de  <strong>"""+nombre_imputado.encode('utf-8')+"""</strong>.
                    </p>
                </li>
                <li>
                    <p class="text-justify">
                    Informar al Supervisor de Medidas Cautelares de forma inmediata en caso de que haya cambiado de mi domicilio, mi numero de teléfono celular y/o fijo 
                    o del imputado.
                    </p>
                </li>
                <li>
                    <p class="text-justify">
                    Motivar a  <strong>"""+nombre_imputado.encode('utf-8')+"""</strong> para que asista a todas las audiencias y cumpla con las imposiciones judiciales.
                    </p>
                </li>
            </ul>
            <br>
			<br>
            <p class="text-justify">NOMBRE DEL APOYO MORAL:  <strong>"""+nombre_a_moral.encode('utf-8')+"""</strong></p>
            <div class="row">
            	<div class="col-xs-8">
            		Firma:_______________________________
            	</div>
            </div>
            <br>
            <div class="row">
            	<div class="col-xs-4">
           			 <p class="text-justify">NOMBRE DEL SUPERVISOR:  <strong>"""+nombre_sup.encode('utf-8')+"""</strong></p>
            	</div>
            	<div class="col-xs-4">
            		Firma:_______________________________
            	</div>
            	<div class="col-xs-4">
            		Fecha:  <strong>"""+str(self.x_fecha_documento)+"""</strong>
            	</div>
            </div>
        """
        self.x_contenido = default_code

    def informe_html(self):
        nombre_imputado = self.x_imputado_id.display_name
        lista = self.x_lista_mc_scp
        default_code = """
            <div class="row">
                <div class="col-xs-12 text-right">
                    Oficio número: <br>
                    Asunto: <br>
                    Causa Penal: <br>
                </div>
            </div>
            <div class="row">
                <div class="col-xs-12">
                    Abogado: <br>
                    ______________________________ <br>
                    ______________________________ <br>
                    P r e s e n t e: <br>
                </div>
            </div>
            <p> 
                Con fundamento en lo dispuesto por los artículos 176, 177, 184, 191, 195 y 209 del Código Nacional de Procedimiento Penales;
                69 y 70 de la Ley de Ejecución de Medidas Cautelares y Sanciones Penales; 17 fracciones XIII y XIV de la Ley de Seguridad Pública; 
                8, 30 Bis Fracciones II, III IV, V, VI, VIl y VIII del Reglamento Interior de la Secretaria de Seguridad Pública todas para el Estado de Puebla;
                en cumplimiento a su oficio número _______________, de fecha _______________, dictado dentro de la causa penal indicada al rubro, mediante el cual 
                solicita se vigile el cumplimiento de las condiciones decretadas al imputado """+nombre_imputado.encode('utf-8')+""" por el plazo de un año, contados a partir de día de 
                la emisión del oficio en comento siendo las condiciones siguientes: 
            </p>
            """+lista.encode('utf-8')+"""

        """
        self.x_contenido = default_code