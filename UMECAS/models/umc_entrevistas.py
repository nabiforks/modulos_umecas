# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Entrevistas(models.Model):
    _name = 'umc_entrevistas'

    x_name = fields.Char('Entrevista', required=True, readonly=True,
                         default=lambda self: 'Nuevo'
                         )        
    x_lugar_entrevista = fields.Many2one(
        string=u'Lugar',
        comodel_name='umc_lugares',
        ondelete='restrict',
    )    
    x_causa_penal = fields.Char(
        string=u'Causa Penal',
    )        
    x_fecha_entrevista = fields.Date(
        string=u'Fecha y hora',        
    )
    x_fecha_entrevista = fields.Date(
        string=u'Fecha',
        default=fields.Date.context_today,
    )
    x_hora_inicio = fields.Float(
        string=u'Hora inicio',
    )
    x_hora_fin = fields.Float(
        string=u'Hora de conclusión',
    )
    x_evaluacion_id = fields.Many2one(
        string=u'Solicitud',
        comodel_name='umc_evaluacion',
        readonly=True,
        ondelete='cascade',
        required=True,
    )
    x_tipo = fields.Selection(
        string=u'Tipo de Entrevista',
        related='x_evaluacion_id.x_tipo_entrevista'
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
    x_casa_justicia = fields.Many2one(
        string=u'Casa de Justicia',
        comodel_name='res.company',
        ondelete='set null',
        readonly=True,
    )

    @api.model
    def create(self, vals):
        if vals.get('x_name', 'Nuevo') == 'Nuevo':
            vals['x_name'] = self.env['ir.sequence'].next_by_code(
                'umc_entrevistas') or'Nuevo'
        result = super(Entrevistas, self).create(vals)
        return result
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('terminado', 'Terminado'),
    ], default='borrador', string='Estatus', readonly=True)

    @api.multi
    def entrevista_realizada(self):
        self.state = 'terminado'

    #///////////////////////////////////////Campos de las entrevistas////////////////
    #///////////////////////////////////////Campos de las entrevistas////////////////
    #///////////////////////////////////////Campos de las entrevistas////////////////

    #/////////////////////Datos personales//////////////
    x_apellido_pat = fields.Char(
        string=u'Apellido Paterno',
        related='x_evaluacion_id.partner_id.ap_paterno',
    )
    x_apellido_mat = fields.Char(
        string=u'Apellido Materno',
        related='x_evaluacion_id.partner_id.ap_materno',
    )
    x_nombre_entrevistado = fields.Char(
        string=u'Nombre(s)',
        related='x_evaluacion_id.partner_id.name',
    )
    x_otronombre = fields.Char(
        string=u'Otro nombre',
    )
    x_apodo = fields.Char(
        string=u'Apodo',
        related='x_evaluacion_id.partner_id.x_apodo',
    )
    x_lugar_nacimiento = fields.Char(
        string=u'Lugar de Nacimiento',
    )
    x_fecha_nacimiento = fields.Date(
        string=u'Fecha de nacimiento',
        related='x_evaluacion_id.partner_id.fecha_nacimiento',
    )
    x_edad = fields.Integer(
        string=u'Edad',
        related='x_evaluacion_id.partner_id.edad',
    )
    x_sexo = fields.Selection(
        string=u'Sexo',
        selection=[('m', 'Masculino'), ('f', 'Femenino'),('o', 'Otro')]
    )
    x_estado_civil = fields.Selection(
        string=u'Estado civil',
        selection=[('soltero', 'Soltero'), ('casado', 'Casado'),('cuncubinato','Cuncubinato'),('otro','Otro')]
    )    
    x_estado_civil_otro = fields.Char(
        string=u'Otro',
    )
    x_tiempo = fields.Integer(
        string=u'Tiempo',
    )
    x_tiempo_unidad = fields.Selection(
        string=u'Días/Semanas/Meses/Años',
        selection=[('dias', 'Días'), ('semanas', 'Semanas'),('meses', 'Meses'),('anios', 'Años')]
    )
    x_lengua = fields.Many2one(
        string=u'Lengua',
        comodel_name='umc_lengua',
        ondelete='set null',
    )
    x_grupo_etnico = fields.Many2one(
        string=u'Grupo Etnico',
        comodel_name='umc_grupoetnico',
        ondelete='set null',
    )
    x_nacionalidad = fields.Many2one(
        string=u'Nacionalidad',
        comodel_name='umc_nacionalidad',
        ondelete='set null',
    )
    x_idioma = fields.Many2one(
        string=u'Idioma',
        comodel_name='umc_idioma',
        ondelete='set null',
    )
    x_leer_escribir = fields.Selection(
        string=u'¿Sabe leer y escribir?',
        selection=[('si', 'Si'), ('no', 'No')]
    )
    x_telefono = fields.Char(
        string=u'Teléfono Casa',
    )
    x_telefono_otro = fields.Char(
        string=u'Teléfono Otros',
    )
    
    #///////////////////////// II.-Domicilio/////////////////

    
    x_ubicacion_intramuros = fields.Many2one(
        string=u'Ubicación Intramuros',
        comodel_name='umc_ubicacion_intramuros',
        ondelete='set null',
    )
    
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
    x_tiempo_libre = fields.Selection(
        string=u'¿Realiza otra(s) actividad en su tiempo libre?',
        selection=[('si', 'Si'), ('no', 'No')]
    )
    x_tiempo_libre_cuales = fields.Text(
        string=u'¿Cuales?',
    )
    
    
    #//////////////////////////////////IV.-Relaciones familiares/////////////////
    x_contacto_ids = fields.One2many(
        string=u'Familiares',
        comodel_name='res.partner',
        inverse_name='x_entrevistas_id',
    )
    x_intrafamiliares_primario = fields.Char(
        string=u'¿Tipo de relaciones intrafamiliares?',
    )
    x_intrafamiliares_secundario = fields.Char(
        string=u'¿Tipo de relaciones intrafamiliares?(Secundario)',
    )
    
    x_imputado_id = fields.Integer(
        string=u'Inputado',
        related='x_evaluacion_id.partner_id.id',
    )
    #//////////////////////////////////V.-Amistades Referencias personales/////////////////
    x_amistades_ids = fields.One2many(
        string=u'Amistades (Referencias personales)',
        comodel_name='umc_amistades',
        inverse_name='x_entrevista_id',
    )

    #//////////////////////////////////VI.-Empleo/////////////////

    x_empleos_ids = fields.One2many(
        string=u'Empleos',
        comodel_name='umc_empleos',
        inverse_name='x_entrevista_id',
    )
    #//////////////////////////////////VII.-Estudios/////////////////
    
    x_escolaridad_intramuros = fields.Selection(
        string=u'¿Se ha incorporado a algun sistema educativo?',
        selection=[('si', 'Si'), ('no', 'No')]
    )
    x_escolaridad_intramuros_cual = fields.Char(
        string=u'¿Cúal?',
    )
    x_observaciones = fields.Char(
        string=u'Observaciones',
    )
    x_estudios_ids = fields.One2many(
        string=u'Estudios',
        comodel_name='umc_estudios',
        ondelete='set null',
        inverse_name="x_entrevista_id"
    )

    #//////////////////////////////////VIII.-Antecedentes penales/////////////////

    x_antecedentes = fields.Selection(
        string=u'¿Ha estado detenido anteriormente?',
        selection=[('si', 'Si'), ('no', 'No')]
    )
    x_donde_lugar = fields.Char(
        string=u'Lugar',
    )
    x_donde_institucion = fields.Char(
        string=u'Institución penitenciaria',
    )
    x_delitos = fields.Many2many(
        string=u'¿Porqué delito?',
        comodel_name='umc_delitos',
    )
    x_temporalidad_cantidad = fields.Integer(
        string=u'Temporalidad',
    )
    x_temporalidad_unidad = fields.Selection(
        string=u'Días/Semanas/Meses/Años',
        selection=[('dias', 'Días'), ('semanas', 'Semanas'),('meses', 'Meses'),('anios', 'Años')]
    ) 
    
    

    #//////////////////////////////////IX.-Enfermedades/////////////////
    x_enfermedades_ids = fields.One2many(
        string=u'Enfermedades',
        comodel_name='umc_enfermedades_padece',
        inverse_name='x_entrevista_id',
    )
    x_discapacidad_id = fields.Many2one(
        string=u'¿Cúal?',
        comodel_name='umc_discapacidad',
        ondelete='set null',
    )
    x_discapacidad_padece = fields.Selection(
        string=u'¿Padece alguna discapacidad?',
        selection=[('si', 'Si'), ('no', 'No')]
    )
     

    #//////////////////////////////////X.- Consumo de sustancias/////////////////
    x_sustancias_ids = fields.One2many(
        string=u'Consume sustancias',
        comodel_name='umc_sustancias_consume',
        inverse_name='x_entrevista_id',
    )
    x_consume_sustancias = fields.Selection(
        string=u'¿Consume sustancias?',
        selection=[('si', 'Si'), ('no', 'No')]
    )

    #/////////////////////////////////// XI.- Información del proceso actual///////////////
    
    x_delitos_ids = fields.One2many(
        string=u'Delitos',
        comodel_name='umc_delitos_proceso',
        inverse_name='x_entrevista_id',
    )
    x_hechos_conducta = fields.Text(
        string=u'Dinámica de los hechos de la conducta antisocial',
    )
    x_lugar_detencion = fields.Char(
        string=u'Lugar de detención',
    )
    x_autoridad_id = fields.Many2one(
        string=u'Autoridad que realizó la detención',
        comodel_name='umc_autoridad',
        ondelete='set null',        
    )
    x_fecha_disposicion = fields.Datetime(
        string=u'Puesta a disposición',
    )
    x_fecha_detencion = fields.Datetime(
        string=u'Detención',
    )
    x_comportamiento = fields.Text(
        string=u'Comportamiento ante la detención: (Resistencia, persecución, violencia, etc.',
    )
    
    x_otras_personas = fields.Selection(
        string=u'¿Detuvieron a otras personas junto con el entrevistado?',
        selection=[('si', 'Si'), ('no', 'No')]
    )
    x_otras_personas_ids = fields.One2many(
        string=u'Otras personas',
        comodel_name='umc_detenidos_con',
        inverse_name='x_entrevista_id2'
    )
    x_victima_nombre = fields.Char(
        string=u'Nombre de la víctima',
    )
    x_victima_edad = fields.Integer(
        string=u'Edad',
    )
    x_victima_anios = fields.Selection(
        string=u'Meses/años',
        selection=[('meses', 'Meses'), ('anios', 'Años')]
    )
    x_victima_domicilio = fields.Char(
        string=u'Domicilio de la víctima',
    )    
    x_victima_relacion = fields.Many2one(
        string=u'Relación con la víctima',
        comodel_name='umc_parentesco',
        ondelete='set null',
    )
    
    x_cumplio_medidas = fields.Selection(
        string=u'Cumplió con medidas cautelares',
        selection=[('si', 'Si'),( 'no','No')]
    )
    x_cumplio_scp = fields.Selection(
        string=u'Cumplió con SCP',
        selection=[('si', 'Si'),( 'no','No')]
    )
    x_colaboro_anteriores = fields.Selection(
        string=u'Permitió o Colaboró con procesos anteriores',
        selection=[('si', 'Si'),( 'no','No')]
    )
    x_observaciones_actitud = fields.Text(
        string=u'Observaciones (Actitud ante la entrevista)',
    )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
