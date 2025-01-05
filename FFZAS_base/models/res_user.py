from email.policy import default

from odoo import fields, models, api


class ResUsers(models.Model):
    _inherit = "res.users"

    telephone = fields.Text(string="Telephone Number")
    surname = fields.Text(string="Last Name")
    type = fields.Selection(selection=[('c', "Customer"),
                                       ('e', "Employee"),
                                       ('s', "Super User")]
                            , default='c'
                            , string="User Type")

    def unlink(self):
        for rec in self:
            reservations = rec.env['reservation'].search(['customer', '=', rec.id])
            reservations.customer = rec.env['res.config.settings'].deleted_user_template

        return super(ResUsers, self).unlink()