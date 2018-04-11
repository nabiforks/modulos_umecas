
# -*- coding: utf-8 -*-
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx


class PartnerXlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, partners):
        report_name = 'name'
        # One sheet by partner
        sheet = workbook.add_worksheet(report_name[:31])
        bold = workbook.add_format({'bold': True,'bg_color': '#FFAB86'})
        color='#DCDCDC'
        
        # imprimir encabezado
        sheet.write(0, 0, 'Nombre', bold)
        sheet.write(0, 1, 'Sexo', bold)
        sheet.write(0, 2, 'Edad', bold)
        sheet.write(0, 3, 'Expediente', bold)
        sheet.write(0, 4, 'Delitos', bold)
        sheet.write(0, 5, 'Distrito', bold)
        sheet.write(0, 6, 'CDI', bold)
        sheet.write(0, 7, 'Causa', bold)
        aux = 1
        aux_celda = 1
        for obj in partners:
            if aux_celda == 1:
                color='#DCDCDC'
                aux_celda = 0
            else:
                color='#ccff99'
                aux_celda = 1
            celda = workbook.add_format({'bg_color': color})
            sheet.write(aux, 0, obj.display_name,celda)
            sheet.write(aux, 1, obj.edad,celda)
            sheet.write(aux, 2, obj.edad,celda)
            expedientes = self.env['umc_expedientes'].search(
                [('partner_id', '=', obj.id)])
            if expedientes:
                for expediente in expedientes:
                    sheet.write(aux, 3, expediente.x_name,celda)
                    delito_cad = ''
                    for delito in expediente.x_delito:
                        delito_cad = delito_cad + ',' + delito.x_name
                    sheet.write(aux, 4, delito_cad,celda)
                    sheet.write(aux, 5, expediente.x_casa_justicia.name,celda)
                    sheet.write(aux, 6, expediente.x_cdi_nic,celda)
                    sheet.write(aux, 7, expediente.x_causa_penal,celda)
                    aux = aux + 1
            else:
                aux = aux + 1


PartnerXlsx('report.res.partner.xlsx', 'res.partner')
