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
                                  'x_nombre_entrevistado': self.x_imputado_id.name}
            res = self.env['sup_entrevista_encuadre'].create(valores_entrevista)
            self.x_encuadre_id = res
            return res
        else:
            self.state = 'encuadre'
    @api.multi
    def regresar_capturar_medidas(self):
        self.state = 'mc-scp'
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

    #/////////////////////////////////////////////
    #/////////////////////////////////////////////
    #/////////////////////////////////////////////

    x_expediente_id = fields.Many2one(
        string=u'Expediente ID',
        comodel_name='umc_expedientes',
        ondelete='cascade',
        readonly=True,
    )
