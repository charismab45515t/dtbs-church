__author__ = 'shamgar'
from openerp import models, fields


class ContactType(models.Model):
    """
    Tipe2 kontak
    """
    _name = "dtbs.church.contact.type"

    name = fields.Char("Contact Type Name", required=True)
    description = fields.Text("Description")
