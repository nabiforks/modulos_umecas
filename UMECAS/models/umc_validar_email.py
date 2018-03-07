# -*- coding: utf-8 -*-
import re
from odoo import api, models,exceptions
from odoo.exceptions import ValidationError,Warning


class ResPartner_email(models.Model):
    _inherit = 'res.partner'

    @api.constrains('email')
    def validar_email(self):
        for record in self:
            if record.email:
                if not (re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", record.email) != None):
                    #raise ValidationError("Email inválido: %s" % record.email)
                    raise exceptions.ValidationError('Email invalido: %s ' %record.email)
                    #raise osv.except_osv('Invalid Email', 'Please enter a valid email address')
                    #raise Warning('Invalid Email Please enter a valid email address')
