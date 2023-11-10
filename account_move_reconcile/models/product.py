from odoo import api, models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    digit = fields.Integer()

