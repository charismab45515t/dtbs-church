from openerp import models, fields, api
from openerp.exceptions import ValidationError
from ..text import DRAFT, CONFIRM, ACTIVE, NACTIVE
from ..text import VALIDATE_FOUND_SERV

STATE = (
	("draft", DRAFT),
	("confirm", CONFIRM)
)

STATE_SERV = (
	("draft", DRAFT),
	("active", ACTIVE),
	("nactive", NACTIVE)
)

class ServiceLine(models.Model):
	"""
	Model untuk menyimpan data pelayanan
	"""
	_name = "dtbs.church.service.line"
	_description = "Service Line"
	_rec_name = "name_view"

	reg_id = fields.Many2one(comodel_name="dtbs.church.service.reg", string="Registration", ondelete="cascade")
	member_id = fields.Many2one(comodel_name="dtbs.church.member", string="Member", required=True, ondelete="restrict")
	type_service_id = fields.Many2one(comodel_name="dtbs.church.type.service", string="Service")
	state = fields.Selection(STATE_SERV, string="State")
	name_view = fields.Char(string="Name", compute="_get_name", search="_search_name")
	reason = fields.Text(string="Reason")
	dt_active = fields.Date(string="Active Date")
	dt_nactive = fields.Date(string="Non Active Date")

	_defaults = {
		"state": STATE_SERV[0][0]
	}

	@api.constrains("member_id","type_service_id")
	def constraint_duplicate_service(self):
		for record in self:
			serv_ids = self.env["dtbs.church.service.line"].search([
										("id", "!=", record.id),
										("member_id", "=", record.member_id.id),
										("type_service_id", "=", record.type_service_id.id),
										("state", "=", "active")
									]).mapped("member_id.name")
			if serv_ids:
				err_msg = "{} - {}".format(VALIDATE_FOUND_SERV, list(serv_ids))
				raise ValidationError(err_msg)

	# compute
	@api.depends("member_id", "type_service_id")
	def _get_name(self):
		"""
		Mendapatkan nama sebagai tampilan.
		"""
		for record in self:
			record.name_view = "{} - {}".format(record.member_id.name, record.type_service_id.complete_name)

	@api.model
	def _search_name(self, operator, value):
		"""
		Method bantuan untuk pencarian nama.
		"""
		return ["|", ("member_id", operator, value), ("type_service_id", operator, value)]

	# public method
	@api.model
	def update_service_line(self):
		"""
		Mengubah status service line jika sudah waktu nya.

		:return: List id service yang di update.
		"""
		service = self.env["dtbs.church.service.line"]
		service.search([
			"&", ("state", "=", STATE_SERV[0][0]), ("dt_active", "<=", fields.Date.today())
		]).sudo().write({"state": STATE[1][0]})

		service.search([
			"&", ("state", "=", STATE_SERV[1][0]), ("dt_nactive", "<=", fields.Date.today())
		]).sudo().write({"state": STATE[2][0]})

		return service.ids

	@api.multi
	def _default_serv_id(self, obj):
		"""
		Mendapatkan default service parent.

		:param obj: Object
		:return: serv_id
		"""
		return obj.reg_id.type_service_id.id


	@api.model
	@api.returns('self',lambda value:value.id)
	def create(self, vals):
		"""
		Overrite method ``create`` untuk default.
		"""
		obj = super(ServiceLine, self).create(vals) 

		serv_id = self._default_serv_id(obj)
		obj.write({"type_service_id": serv_id})
		return obj



class ServiceRegistration(models.Model):
	"""
	Model untuk menyimpan registrasi pelayanan
	"""
	_name = "dtbs.church.service.reg"
	_description = "Service Registration"

	name = fields.Char(string="Reference Number")
	effective_date = fields.Date(string="Effective Date", required=True)
	type_service_id = fields.Many2one(comodel_name="dtbs.church.type.service", string="Service", required=True, ondelete="restrict")
	service_ids = fields.One2many(comodel_name="dtbs.church.service.line", inverse_name="reg_id", string="Member", ondelete="cascade")
	state = fields.Selection(STATE, string="State")

	# other
	confirm_uid = fields.Many2one("res.users", "Confirmed By", ondelete="restrict")
	dt_confirm = fields.Datetime(string="Confirmed Date")

	_defaults = {
		"state": STATE[0][0]
	}


	@api.multi
	def to_confirm(self):
		"""
		Mengubah state.
		"""
		assert len(self.ids) == 1

		self.service_ids.write({'dt_active':self.effective_date})
		self.write({
			'state':STATE[1][0],
			'confirm_uid':self.env.uid,
			'dt_confirm':fields.Datetime.now()
		})

		return {}

	@api.model
	def create(self, vals):
		# auto number
		if vals.get('name','/')=='/':
			vals['name'] = self.env['ir.sequence'].get('dtbs.church.service.reg') or '/'

		obj =  super(ServiceRegistration, self).create(vals)
		return obj