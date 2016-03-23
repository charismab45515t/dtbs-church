__author__ = 'shamgar'

from openerp import models, fields, api
from openerp.exceptions import MissingError
from ..text import VALIDATE_UNIQUE_NAME


class LastEducation(models.Model):
    """
    Master Pendidikan Terakhir
    """
    _name = "dtbs.church.last.education"
    _order = "name"

    name = fields.Char("Name", required=True)


    _sql_constraints = (
        ("kode_unique", "UNIQUE(kode)", VALIDATE_UNIQUE_NAME),
    )
