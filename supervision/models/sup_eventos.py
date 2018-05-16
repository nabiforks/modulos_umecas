# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import timedelta, datetime

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
        readonly=True,        
    )
    x_atrasado = fields.Boolean(
        string=u'Atrasado',        
        readonly=True,        
        compute='get_atrasados'
    )
    estatus = fields.Selection(
        [('pendiente', 'Pendiente'),
         ('realizado', 'Realizado'),
         ('atrasado', 'Atrasado')],
        default='pendiente',
        readonly=True, string=u'Estatus',
        #compute='get_atrasados'
    )
    @api.multi
    @api.depends('start_datetime','estatus')
    def get_atrasados(self):
        fecha = datetime.now()
        for record in self:
            fecha_inicio = fields.Datetime.from_string(record.start_datetime)
            if fecha_inicio < fecha:
                record.x_atrasado = True
                record.estatus = 'atrasado'
    @api.multi
    def set_cumplio_firma(self):
        self.x_cumplio= True
        self.estatus = 'realizado'
    @api.multi
    def set_incumplimiento(self):
        self.x_cumplio= False
        self.estatus = 'pendiente'
    #@api.multi
    def action_detach_recurring_event(self):        
        res = super(sup_eventos, self).action_detach_recurring_event()
        evento = self.env['calendar.event'].search([('id', '=', res['res_id'])])
        evento.write({'x_cumplio':True,'estatus':'realizado'})
        return