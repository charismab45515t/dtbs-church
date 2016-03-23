__author__ = 'andre'
"""
Module2 untuk field o2m employee.
"""
from openerp import models, fields
from member import GENDER


class Contact(models.Model):
    """
    Model untuk data kontak2 member.
    """
    _name = "dtbs.church.member.contact"
    _inherit = "dtbs.church.contact.template"

    member_id = fields.Many2one("dtbs.church.member.template", "Member", required=True, ondelete="cascade")
    emergency = fields.Boolean("Emergency Contact?", default=False)


class Address(models.Model):
    """
    Model untuk data alamat2 member.
    """
    _name = "dtbs.church.member.address"
    _inherit = "dtbs.church.address.template"

    member_id = fields.Many2one("dtbs.church.member.template", "Member", required=True, ondelete="cascade")
    emergency = fields.Boolean("Emergency Address?", default=False)


class Family(models.Model):
    """
    Model untuk data keterangan keluarga.
    """
    _name = "dtbs.church.member.family"
    _order = "position asc"

    member_id = fields.Many2one("dtbs.church.member.template", "Member", required=True, ondelete="cascade")

    position = fields.Char("Position", required=True)
    name = fields.Char("Name", required=True)
    gender = fields.Selection(GENDER, "Gender", required=True)
    dead = fields.Boolean("Passed Away", default=False)
    date_of_birth = fields.Date("Date of Birth")
    education_id = fields.Many2one("dtbs.church.last.education", "Education", required=True, ondelete="restrict")
    occupation = fields.Char("Occupation")


class Education(models.Model):
    """
    Model untuk keterangan sejarah edukasi member.
    """
    _name = "dtbs.church.member.education"
    _order = "start_year desc"

    member_id = fields.Many2one("dtbs.church.member.template", "Member", required=True, ondelete="cascade")

    education_id = fields.Many2one("dtbs.church.last.education", "Education", required=True, ondelete="restrict")
    major = fields.Char("Major")
    institution = fields.Char("Institution", size=500)
    location = fields.Char("Location")
    start_year = fields.Integer("Enrolment Year")
    end_year = fields.Integer("Graduation Year")


