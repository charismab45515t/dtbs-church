__author__ = "shamgar"

from openerp import models, fields, api
from ..text import DRAFT, ACTIVE, NONACTIVE

STATE = (
    ("draft", DRAFT),
    ("active", ACTIVE),
    ("nonactive", NONACTIVE)
)

class MemberAttachment(models.Model):
	"""
	Model untuk list attachment member.
	"""
	_name = "dtbs.church.member.attachment"
	_inherits = {"ir.attachment": "attachment_id"}

	member_id = fields.Many2one("dtbs.church.member", required=True, ondelete="cascade")
	attachment_id = fields.Many2one("ir.attachment")

	# override
	@api.multi
	def unlink(self):
		"""
		Hapus data attachment ketika data parent dihapus
		"""
		self.mapped("attachment_id").unlink()
		return super(MemberAttachment, self).unlink()


class ChurchMember(models.Model):
	"""
	Model untuk menyimpan data Jemaat
	"""
	_name = "dtbs.church.member"
	_inherits = {"dtbs.church.member.template": "template_id"}
	_description = "Church Member"

	template_id = fields.Many2one(comodel_name="dtbs.church.member.template", required=True, ondelete="cascade", auto_join=True)
	registration_no = fields.Char(string="Registration Number")
	company_id = fields.Many2one(comodel_name="res.company", string="Church")
	join_date = fields.Date(string="Join Date")
	state = fields.Selection(STATE, string="State")

	# attachment
	attachment_ids = fields.One2many(comodel_name="dtbs.church.member.attachment", inverse_name="member_id", string="Attachment", ondelete="cascade")

	# extra information
	active_uid = fields.Many2one("res.users", "Actived By", ondelete="restrict")
	nactive_uid = fields.Many2one("res.users", "Non Actived By", ondelete="restrict")
	dt_active = fields.Datetime(string="Actived Date")
	dt_nactive = fields.Datetime(string="Non Actived Date")

	_defaults = {
		"state": STATE[0][0]
	}

	@api.multi
	def to_active(self):
		"""
		Mengubah state.
		"""
		assert len(self.ids) == 1
		
		self.write({
			'state':STATE[1][0],
			'active_uid':self.env.uid,
			'dt_active':fields.Datetime.now()
		})

		return {}

	@api.multi
	def to_nactive(self):
		"""
		Mengubah state.
		"""
		assert len(self.ids) == 1
		
		self.write({
			'state':STATE[2][0],
			'nactive_uid':self.env.uid,
			'dt_nactive':fields.Datetime.now()
		})

		return {}

	# override
	@api.multi
	def unlink(self):
		"""
		Hapus data attachment ketika data dihapus
		"""
		self.mapped("attachment_ids").unlink()
		# self.template_id.mapped("image_medium_id").unlink()

		return super(ChurchMember, self).unlink()