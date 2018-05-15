# -*- coding: utf-8 -*-
from odoo import api, fields, models


class sup_eventos(models.Model):

    _inherit = 'calendar.event'
    
    x_supervision_id = fields.Many2one(
        string=u'Supervisión ID',
        comodel_name='sup_mc_scp',
        ondelete='set null',
    )
    x_imputado_name = fields.Char(
        string=u'Imputado',
        readonly=True,
        related='x_supervision_id.x_imputado_id.display_name',
    )
    x_cumplio = fields.Boolean(
        string=u'Cumplió/Realizado',
    )
    @api.multi
    def set_cumplio_firma(self):
        if self.recurrency:
            print "************************* entro pero no funciona"            
        else:
            print "************************* recurrente no activado"
    
    @api.multi
    def action_detach_recurring_event(self):
        
        res = super(sup_eventos, self).action_detach_recurring_event()
        self.write({'x_cumplio':True})
        print "******************* res = ",res
        return res
        