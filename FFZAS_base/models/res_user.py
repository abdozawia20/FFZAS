from email.policy import default

from odoo import fields, models, api

# inheriting res.users class to add more functionalities
class ResUsers(models.Model):
    _inherit = "res.users"

    # adding variables
    telephone = fields.Text(string="Telephone Number")
    surname = fields.Text(string="Last Name")
    type = fields.Selection(selection=[('c', "Customer"),
                                       ('e', "Employee"),
                                       ('s', "Super User")]
                            , default='c'
                            , string="User Type")

    # overriding delete function to extend its functionality
    def unlink(self):
        for rec in self:
            reservations = rec.env['reservation'].search(['customer', '=', rec.id])
            reservations.customer = rec.env['res.config.settings'].deleted_user_template

        return super(ResUsers, self).unlink()