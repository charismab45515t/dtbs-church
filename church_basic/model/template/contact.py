__author__ = 'shamgar'
from openerp import models, fields, api
from openerp.exceptions import ValidationError
from ...text import VALIDATE_PHONE_FORMAT


class ContactTemplate(models.Model):
    """
    Model template untuk nomor kontak.
    """
    _name = "dtbs.church.contact.template"

    contact_type_id = fields.Many2one("dtbs.church.contact.type", "Contact Type", required=True)
    number = fields.Char("Number", required=True)

    # # constraints
    # @api.constrains("number")
    # def _validate_number(self):
    #     """
    #     Validasi nomor telp.
    #     """
    #     validate_phone = self.env["sisu.common.validation"].validate_phone

    #     for record in self:
    #         if record.number and not validate_phone(record.number):
    #             raise ValidationError(VALIDATE_PHONE_FORMAT)
