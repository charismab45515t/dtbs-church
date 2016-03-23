from openerp import models, fields, api

class ServiceLine(models.TransientModel):
	"""
	Model wizard detail service yang akan dinonaktifkan
	"""
	_name = "dtbs.church.service.line.nonactive.wizard"

	wizard_id = fields.Many2one(comodel_name="dtbs.church.service.nonactive.wizard", string="Wizard", ondelete="cascade", required=True)
	service_line_id = fields.Many2one(comodel_name="dtbs.church.service.line", string="Service", required=True, ondelete="restrict", domain=[("state", "=", "active"), ("dt_nactive", "=", False)])
	reason = fields.Text(string="Reason")
	effective_date = fields.Date(string="Effective Date", required=True)

class ServiceNonActiveWizard(models.TransientModel):
	"""
	Model untuk wizard penonaktifan pelayanan.
	"""
	_name = "dtbs.church.service.nonactive.wizard"

	service_ids = fields.One2many(comodel_name="dtbs.church.service.line.nonactive.wizard", inverse_name="wizard_id", string="Service", ondelete="cascade")

	@api.multi
	def action_nonactive_service(self):
		"""
		Method untuk non active service.

		:return: {}
		"""
		self.ensure_one()

		for line in self.service_ids:
			line.service_line_id.sudo().write({"dt_nactive": line.effective_date})

		return {}




