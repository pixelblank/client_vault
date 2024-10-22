from odoo import models, fields, api, http, _
import os
import logging
_logger = logging.getLogger(__name__)

class ClientVault(models.Model):
    _name = 'client.vault'
    _description = 'Coffre fort pour les document clients'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom', required=True)
    client_id = fields.Many2one('res.partner', string='Client')
    client_avatar = fields.Binary(related='client_id.image_128', string='Client Avatar', readonly=True)
    create_date = fields.Datetime(string='Creation Date')
    write_date = fields.Datetime(string='Modification Date')
    document_ids = fields.One2many('client.document', 'vault_id', string='Documents')
    color = fields.Integer(string='Color Index')
    document_count = fields.Integer(string='Nombre de documents', compute='_compute_document_count', store=True)
    _logger.debug('ClientVault')

    @api.model_create_multi
    def create(self, vals_list):
        vaults = super(ClientVault, self).create(vals_list)
        _logger.debug('ClientVault Create a vault')
        for vault in vaults:
            if vault.document_ids:
                vault.document_ids.write({'client_id': vault.client_id.id})
        return vaults

    def write(self, vals):
        res = super(ClientVault, self).write(vals)
        _logger.debug('ClientVault write')
        if 'client_id' in vals:
            self.document_ids.write({'client_id': vals['client_id']})
        return res

    @api.depends('document_ids')
    def _compute_document_count(self):
        _logger.debug('ClientVault _compute_document_count')
        for record in self:
            record.document_count = len(record.document_ids)


class ClientDocument(models.Model):
    _name = 'client.document'
    _description = 'Document des client'

    file_extension = fields.Char(string='Extension de fichier', compute='_compute_file_extension', store=True)
    name = fields.Char(string='nom du document', required=True)
    document_type = fields.Selection([
        ('server_sheet', 'données serveur'),
        ('specifications', 'cahier des charges'),
        ('graphic_charter', 'charte graphic'),
        ('other', 'autres')
    ], string='Type de document', required=True)
    client_id = fields.Many2one('res.partner', string='Client', related='vault_id.client_id', store=True)
    file = fields.Binary(string='Fichier', attachment=True)
    vault_id = fields.Many2one('client.vault', string='Coffre-fort')
    preview_action = fields.Char(string='Action de prévisualisation', compute='_compute_preview_action')
    data_display = fields.Char(string="wesh")
    _logger.debug('ClientDocument')

    @api.depends('name', 'file')
    def _compute_preview_action(self):
        for record in self:
            record.preview_action = 'Prévisualiser' if record.file else ''

    @api.depends('name')
    def _compute_file_extension(self):
        for record in self:
            _logger.debug('Create a log')
            _logger.info('FYI: This is happening')
            _logger.warning('WARNING: **************')
            _logger.error('ERROR: Something really bad happened!')
            if record.name:
                _, extension = os.path.splitext(record.name)
                record.file_extension = extension.lower()[1:] if extension else ''
            else:
                record.file_extension = ''

    def action_preview_document(self):
        self.ensure_one()
        _logger.debug('Create a previsualisation')
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'client.document',
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': self.env.ref('client_vault.view_client_document_form').id,
            'target': 'new',
            'flags': {'mode': 'readonly'},
        }

    @api.model
    def create(self, vals):
        _logger.debug('ClientDocument create')
        if 'vault_id' in vals and 'client_id' not in vals:
            vault = self.env['client.vault'].browse(vals['vault_id'])
            vals['client_id'] = vault.client_id.id
        return super(ClientDocument, self).create(vals)

    @api.depends('vault_id', 'vault_id.client_id')
    def _compute_client_id(self):
        for record in self:
            record.client_id = record.vault_id.client_id