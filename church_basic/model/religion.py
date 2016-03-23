__author__ = 'shamgar'
from openerp import models, fields
from ..text import VALIDATE_UNIQUE_NAME


class Religion(models.Model):
    """
    Model religion.
    """
    _name = "dtbs.church.religion"

    name = fields.Char("Religion", required=True)

    # constraint
    _constraints = [
        ("unique_name", "UNIQUE(name)", VALIDATE_UNIQUE_NAME)
    ]
