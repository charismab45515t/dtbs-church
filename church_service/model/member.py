from openerp import models, fields, api

class Member(models.Model):
	_inherit = "dtbs.church.member"

	service_ids = fields.One2many(comodel_name="dtbs.church.service.line", inverse_name="member_id", string="Services", domain=[("state", "=", "active")])