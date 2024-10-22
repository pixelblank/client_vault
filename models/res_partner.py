from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vault_ids = fields.One2many('client.vault', 'client_id', string="Coffres-forts")
    document_ids = fields.One2many('client.document', 'client_id', string="Documents")
    vault_count = fields.Integer(string='Nombre de coffres-forts', compute='_compute_vault_count', store=True)

    @api.depends('vault_ids')
    def _compute_vault_count(self):
        for partner in self:
            partner.vault_count = len(partner.vault_ids)
            _logger.info(f"Partner {partner.name} (ID: {partner.id}) has {partner.vault_count} vaults")

    @api.model_create_multi
    def create(self, vals_list):
        partners = super(ResPartner, self).create(vals_list)
        # Ajoutez ici toute logique supplémentaire nécessaire lors de la création
        return partners

    def write(self, vals):
        _logger.info(f"Updating partner {self.name} (ID: {self.id}) with vals: {vals}")
        return super(ResPartner, self).write(vals)

    def action_view_vaults(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Coffres-forts',
            'view_mode': 'kanban,tree,form',
            'res_model': 'client.vault',
            'domain': [('id', 'in', self.vault_ids.ids)],
            'context': {'default_client_id': self.id}
        }

    def action_view_documents(self):
        self.ensure_one()
        return {
            'name': 'Documents du client',
            'type': 'ir.actions.act_window',
            'res_model': 'client.document',
            'view_mode': 'kanban,tree,form',
            'domain': [('client_id', '=', self.id)],
            'context': {'default_client_id': self.id, 'group_by': 'vault_id'},
        }