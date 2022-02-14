# -*- coding: utf-8 -*-

from flask_saml2.utils import certificate_from_file, private_key_from_file

from wgui.utils.saml_sp import sp


def apply_saml(config, app):
    crt_path = config.get("config.saml.saml_crt", mod="get_relative_path")
    key_path = config.get("config.saml.saml_key", mod="get_relative_path")

    app.config['SAML2_SP'] = {
        'certificate': certificate_from_file(crt_path),
        'private_key': private_key_from_file(key_path),
    }

    app.config['SAML2_IDENTITY_PROVIDERS'] = [
        {
            'CLASS': 'flask_saml2.sp.idphandler.IdPHandler',
            'OPTIONS':
                {
                    'display_name': saml.get("display_name"),
                    'entity_id': saml.get("entity_id"),
                    'sso_url': saml.get("sso_url"),
                    'slo_url': saml.get("slo_url"),
                    'certificate': certificate_from_file(saml.get("certificate_path")),
                },
        } for saml in config.get("config.saml.id_providers")
    ]
    app.register_blueprint(sp.create_blueprint(), url_prefix='/saml/')
    return app
