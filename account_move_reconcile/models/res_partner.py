from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_payroll = fields.Boolean()
    blocked_for_payments =fields.Char()
