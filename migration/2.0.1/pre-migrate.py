def migrate(cr, version):
    cr.execute("""
        UPDATE client_document cd
        SET client_id = cv.client_id
        FROM client_vault cv
        WHERE cd.vault_id = cv.id AND cd.client_id IS NULL
    """)