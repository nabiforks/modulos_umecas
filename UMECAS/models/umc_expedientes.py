# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from odoo import api, fields, models


class Expedientes(models.Model):
    _name = 'umc_expedientes'
    # _inherit = 'mail.thread'

    x_name = fields.Char('Expediente', required=True, readonly=True,
                         default=lambda self: 'Nuevo')
    partner_id = fields.Many2one(
        'res.partner',
        string=u'Imputado',
        readonly=True,
        ondelete='set null',
    )
    x_imputado_name = fields.Char(
        string=u'Imputado',
        related='partner_id.display_name',
        readonly=True,
        required=True,
    )
    x_cdi_nic = fields.Char(
        string=u'CDI/NIC',        
    )
    x_causa_penal = fields.Char(
        string=u'Causa Penal',        
    )
    x_numero_oficio = fields.Char(
        string=u'Oficio Número',
    )
    x_fecha_inicio = fields.Datetime(
        string=u'Fecha/Hora Inicio',
        default=fields.Datetime.now,
    )
    x_delito = fields.Many2many(
        'umc_delitos',
        string=u'Delitos'
    )
    x_delito_descripcion = fields.Text(
        string=u'Descripción Delito',
    )

    x_casa_justicia = fields.Many2one(
        string=u'Casa de Justicia',
        comodel_name='res.company',
        ondelete='set null',
        default=lambda self: self.env.user.company_id,
    )
    _sql_constraints = [
        ('folio_unique_expediente', 'UNIQUE(x_name)', 'Error al procesar la solicitud por favor intentelo más tarde.')
    ]

    @api.model
    def create(self, vals):
        if vals.get('x_name', 'New') == 'New':
            vals['x_name'] = self.env['ir.sequence'].next_by_code(
                'umc_expedientes') or 'New'
            now = datetime.now()
            folio = self.createFolioExpedienteByAnio(now.year,1)
            vals['x_name'] = folio or 'new'
            # print vals
        result = super(Expedientes, self).create(vals)
        return result

    @api.model
    def createFolioExpedienteByAnio(self, par_anio_fiscal, par_tipo_configuracion):
        folio = self.env[
                    'umc_casas_justicia_anio_fiscal'].getConsecutivoByAnioAndCasaJusticia(self.env.user.company_id.id,
                                                                                          par_anio_fiscal,
                                                                                          par_tipo_configuracion) + "/" + \
                self.env['umc_casas_justicia_anio_fiscal'].getPrefijoCasaById(
                    self.env.user.company_id.id) + "/" + str(par_anio_fiscal)
        return folio


    #//////////////////////////////////////////one2many evaluacion////////////
    #//////////////////////////////////////////one2many evaluacion////////////
    #//////////////////////////////////////////one2many evaluacion/////////////////
    #//////////////////////////////////////////one2many evaluacion///////////////////
    
    
    x_evaluacion_ids = fields.One2many(
        string=u'Solicitudes',
        comodel_name='umc_evaluacion',
        inverse_name='x_expediente_id',
    )
"""
  folio = self.env['core_generador_folio'].getFolio(
                self.env['umc_casas_justicia_anio_fiscal'].getPrefijoCasaById(
                    vals['x_casa_justicia']))
            # self.createFolioExpedienteByAnio(vals, now.year)
"""
