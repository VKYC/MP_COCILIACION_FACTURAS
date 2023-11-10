from odoo import api, models, fields, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    facturas_conciliacion_id = fields.Many2one(comodel_name='mp.facturas.conciliacion', readonly=True)

    def button_reconcile_custom(self):
        tree_view = self.env.ref("account_move_reconcile.account_facturacion_conciliacion_wizard_tree")
        self.with_context(default_move_id=self.id)
        facturas_conciliacion_ids = self.env['mp.facturas.conciliacion'].search([
            ('rzn_soc_emisor', '=', self.partner_id.name),
            ('rut_emisor', '=', self.partner_id.vat),
            ('monto_total', '=', self.amount_total),
            ('estado', '=', False),
        ])
        self.env['account.facturacion.conciliacion.wizard'].search([]).unlink()
        for facturas_conciliacion_id in facturas_conciliacion_ids:
            self.env['account.facturacion.conciliacion.wizard'].create({
                'move_id': self.id,
                'factura_conciliacion_id': facturas_conciliacion_id.id
            })

        return {
            'name': _('Reconcile document'),
            'view_id': tree_view.id,
            'view_mode': 'tree',
            'res_model': 'account.facturacion.conciliacion.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'flags': {'hasSelectors': False, 'initial_mode': 'view'},
            'context': {
                'default_move_id': self.id,
            }
        }
