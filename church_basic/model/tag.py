__author__ = 'shamgar'
from openerp import models, fields
from ..text import VALIDATE_UNIQUE_NAME


class Tag(models.Model):
    """
    Model tag pengganti model tag nya odoo. Dibuat untuk menghapus dependency ke odoo.
    """
    _name = "dtbs.church.tag"

    name = fields.Char("Member Tag", required=True)
    member_ids = fields.Many2many("dtbs.church.member", "dtbs_church_tag_rel", string="Members")

    # constraint
    _constraints = [
        ("unique_name", "UNIQUE(name)", VALIDATE_UNIQUE_NAME)
    ]
