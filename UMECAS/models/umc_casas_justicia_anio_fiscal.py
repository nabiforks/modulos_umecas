# -*- coding: utf-8 -*-
from odoo import models, api, fields


class umc_casas_justicia_anio_fiscal(models.Model):
    _name = 'umc_casas_justicia_anio_fiscal'
    company_id = fields.Many2one('res.company',
                                 string='Casa de justicia',
                                 ondelete='set null')
    anio = fields.Integer(string='Año fiscal', required=True, default=lambda self: 2018)
    secuencial = fields.Integer(string='Contador', default=0)
    _sql_constraints = [
        ('casa_de_justicia_ejercicio','UNIQUE(company_id,anio)','El año fiscal de la casa de justicia ya existe')
    ]
    # agregar el constrain

    def getConsecutivoByAnioAndCasaJusticia(self, par_casa_justicia, par_anio):
        datos_casa = self.env['umc_casas_justicia_anio_fiscal'].search(
            [('anio', '=', par_anio), ('company_id', '=', par_casa_justicia)])
        secuencia = 1
        if datos_casa:
            secuencia = int(datos_casa.secuencial) + 1;
            datos_casa.write({'secuencial': secuencia});
            return str(secuencia).zfill(5)
        else:
            self.create({'company_id': par_casa_justicia, 'anio': par_anio, 'secuencial': 1});
            return str(secuencia).zfill(5)
        return False

    def getPrefijoCasaById(self, par_casa_id):
        prefijo = self.env['res.company'].search([('partner_id', '=', par_casa_id)])
        if prefijo.x_abreviatura:
            return  prefijo.x_region.x_codigo + "/" + prefijo.x_abreviatura
        return ""
