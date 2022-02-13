# -*- coding: utf-8 -*-

from flask_saml2.utils import certificate_from_file, private_key_from_file

from wgui.utils.saml_sp import sp


def apply_saml(config, app):
    crt_path = config.get_config("saml").get("saml_crt")
    key_path = config.get_config("saml").get("saml_key")

    app.config['SAML2_SP'] = {
        'certificate': certificate_from_file(config.get_path_config(crt_path)),
        'private_key': private_key_from_file(config.get_path_config(key_path)),
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
        } for saml in config.get_all_saml_idps()
    ]
    app.register_blueprint(sp.create_blueprint(), url_prefix='/saml/')
    return app
