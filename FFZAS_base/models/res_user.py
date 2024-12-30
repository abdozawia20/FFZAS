from email.policy import default

from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    telephone = fields.Text(string="Telephone Number")
    surname = fields.Text(string="Last Name")
    type = fields.Selection(selection=[('c', "Customer"),
                                       ('e', "Employee"),
                                       ('s', "Super User")]
                            , default='c'
                            , string="User Type")