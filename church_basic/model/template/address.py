__author__ = 'shamgar'
from openerp import models, fields, api


class AddressTemplate(models.Model):
    """
    Template untuk address.
    """
    _name = "dtbs.church.address.template"

    country_id = fields.Many2one("res.country", "Country")
    state_id = fields.Many2one("res.country.state", "State")
    city = fields.Char("City")
    street = fields.Text("Street")