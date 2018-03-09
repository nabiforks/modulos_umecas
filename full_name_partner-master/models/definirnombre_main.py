# -*- coding: utf-8 -*-
from odoo import api, models, fields


class Definirnombre_main(models.Model):
	_inherit = 'res.partner'

	#nombre_completo = fields.Char(compute='obtener_nombre_completo')
	display_name = fields.Char(compute='obtener_nombre_completo')

	ap_paterno = fields.Char(string="Apellido paterno", required=True)
	ap_materno = fields.Char(string="Apellido materno", required=True)

	@api.multi
	@api.depends('name','ap_paterno','ap_materno')
	def obtener_nombre_completo(self):
		for record in self:
			if record.name and record.ap_paterno and record.ap_materno:
				record.display_name = record.name + " " + record.ap_paterno + " " + record.ap_materno
			else:
				record.display_name = record.name