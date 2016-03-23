__author__ = 'shamgar'
from openerp import models, fields, api
from openerp.tools import image_resize_image_big
from openerp.exceptions import ValidationError
from ..text import MALE, FEMALE, OTHER
from ..text import SINGLE, MARRIED, WIDOWER
from ..text import VALIDATE_UNIQUE_MEMBER

GENDER = (
    ("male", MALE),
    ("female", FEMALE),
    ("other", OTHER)
)

MARITAL_STATUS = (
    ('single', SINGLE),
    ('married', MARRIED),
    ('widower', WIDOWER)
)

BLOOD_TYPE_SELECTION = tuple((blood, blood) for blood in ("A", "B", "AB", "O"))


class MemberTemplate(models.Model):
    """
    Model untuk data2 member gereja (Template).
    """
    _name = "dtbs.church.member.template"


    # fields
    name = fields.Char("Name", required=True)
    tags = fields.Many2many("dtbs.church.tag", "dtbs_church_tag_rel", string="Tags")

    # public
    note = fields.Text("Other Information")

    # personal
    identification_id = fields.Char("Identification Number")

    birth_place = fields.Char("Birth Place")
    date_of_birth = fields.Date("Date of Birth", required=True)

    gender = fields.Selection(GENDER, "Gender")
    marital = fields.Selection(MARITAL_STATUS, 'Marital Status')

    religion_id = fields.Many2one("dtbs.church.religion", "Religion")
    blood_type = fields.Selection(BLOOD_TYPE_SELECTION, "Blood Type")
    hobby = fields.Char("Hobby")

    # contact
    email = fields.Char("E-Mail", size=255)

    # photo
    image_medium_id = fields.Many2one("ir.attachment")
    image_medium = fields.Binary(string="Medium-sized Photo", compute="_get_image_medium", inverse="_set_image_medium")


    # O2Ms
    contact_ids = fields.One2many("dtbs.church.member.contact", "member_id", "Contacts")
    address_ids = fields.One2many("dtbs.church.member.address", "member_id", "Addresses")
    family_ids = fields.One2many("dtbs.church.member.family", "member_id", "Families")
    education_ids = fields.One2many("dtbs.church.member.education", "member_id", "Last Educations")


    # constraint
    _constraints = [
        ("unique_member", "UNIQUE(name,date_of_birth)", VALIDATE_UNIQUE_MEMBER)
    ]


    @api.depends("image_medium_id")
    def _get_image_medium(self):
        """
        Mendapatkan image dari ``ir.attachment``.
        """
        for record in self:
            record.image_medium = record.image_medium_id.datas

    @api.multi
    def _set_image_medium(self):
        """
        Simpan gambar ke ``ir.attachment``.
        """
        att_env = self.env["ir.attachment"]
        for record in self:
            # kalo image_id ada, tapi image tidak di isi, maka image_id dihapus (udah create, dg berisi foto, trs foto.e d hapus lagi)
            if record.image_medium_id and not record.image_medium:
                record.image_medium_id.unlink()
                continue
            # kalo image_id ada, gambarnya di update
            if record.image_medium_id:
                record.image_medium_id.datas = image_resize_image_big(record.image_medium)
            else:
                # kalo belum punya image_id, dibuat.in (create baru)
                record.image_medium_id = att_env.create({
                    "name": "%s_Medium_%s" % (self._name, record.id),
                    "datas": image_resize_image_big(record.image_medium)
                })

    @api.multi
    def unlink(self):
        """
        Hapus data attachment ketika data ini di hapus.
        """
        self.mapped("image_medium_id").unlink()

        return super(MemberTemplate, self).unlink()
