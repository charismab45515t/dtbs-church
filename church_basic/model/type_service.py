__author__ = 'shamgar'
from openerp import models, fields, api
from openerp.osv import expression
from openerp.exceptions import ValidationError

class TypeService(models.Model):
    """
    Model Jenis Pelayanan
    """
    _name = "dtbs.church.type.service"
    _description = "Type of Service"
    # _rec_name = "name_view"


    @api.multi
    def name_get(self):
        def get_names(cat):
            """ Return the list [cat.name, cat.parent_id.name, ...] """
            res = []
            while cat:
                res.append(cat.name)
                cat = cat.parent_id
            return res

        return [(cat.id, " / ".join(reversed(get_names(cat)))) for cat in self]

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            # Be sure name_search is symetric to name_get
            categories = name.split(' / ')
            parents = list(categories)
            child = parents.pop()
            domain = [('name', operator, child)]
            if parents:
                names_ids = self.name_search(cr, uid, ' / '.join(parents), args=args, operator='ilike', context=context, limit=limit)
                category_ids = [name_id[0] for name_id in names_ids]
                if operator in expression.NEGATIVE_TERM_OPERATORS:
                    category_ids = self.search(cr, uid, [('id', 'not in', category_ids)])
                    domain = expression.OR([[('parent_id', 'in', category_ids)], domain])
                else:
                    domain = expression.AND([[('parent_id', 'in', category_ids)], domain])
                for i in range(1, len(categories)):
                    domain = [[('name', operator, ' / '.join(categories[-1 - i:]))], domain]
                    if operator in expression.NEGATIVE_TERM_OPERATORS:
                        domain = expression.AND(domain)
                    else:
                        domain = expression.OR(domain)
            ids = self.search(cr, uid, expression.AND([domain, args]), limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)

    @api.depends("parent_id", "name")
    def _name_get_fnc(self):
        res = self.name_get()
        dic = dict(res)
        for record in self:
            record.complete_name = dic[record.id]




    name = fields.Char("Service Name", required=True, translate=True, select=True)
    parent_id = fields.Many2one(comodel_name="dtbs.church.type.service", string="Parent", select=True, ondelete='cascade')
    complete_name = fields.Char("Name", compute="_name_get_fnc")
    child_id = fields.One2many(comodel_name="dtbs.church.type.service", inverse_name="parent_id", string="Child Services")
    sequence = fields.Integer(string="Sequence", select=True)
    type = fields.Selection([("view","View"), ("normal","Normal")], string="Service Type", default="normal")
    parent_left = fields.Integer(string="Left Parent", select=1)
    parent_right = fields.Integer(string="Right Parent", select=1)

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = "sequence, name"
    _order = "parent_left"


    # # compute
    # @api.depends("parent_id","name")
    # def _get_name(self):
    #     """
    #     Mendapatkan nama sebagai tampilan.
    #     """
    #     for record in self:
    #         record.name_view = "{}{}".format("{} / ".format(record.parent_id.name) if record.parent_id else "", record.name)


    # @api.model
    # def _search_name(self, operator, value):
    #     """
    #     Method bantuan untuk pencarian nama.
    #     """
    #     return ["|", ("name", operator, value), ("parent_id", operator, value)]




