# -*- coding: utf-8 -*-
from flask import url_for
from flask_saml2.sp import ServiceProvider
from flask_saml2.utils import certificate_from_file, private_key_from_file


class ExampleServiceProvider(ServiceProvider):
    entity_id = "https://vpn.eneka.xyz/saml/metadata.xml"

    def get_acs_url(self) -> str:
        return "https://vpn.eneka.xyz/saml/acs/"

    def get_sls_url(self) -> str:
        return "https://vpn.eneka.xyz/saml/sls/"

    def get_logout_return_url(self):
        return url_for('index')

    def get_default_login_return_url(self):
        return url_for("dashboard")

    # def should_sign_requests(self) -> bool:
    #     return False

    def get_auth_data_in_session(self):
        s = super().get_auth_data_in_session()
        print(s)
        return s


sp = ExampleServiceProvider()


def apply_saml(config, app):
    app.config['SAML2_SP'] = {
        'certificate': certificate_from_file(config.get_path_config("saml_crt")),
        'private_key': private_key_from_file(config.get_path_config("saml_key")),
    }

    app.config['SAML2_IDENTITY_PROVIDERS'] = [
        {
            'CLASS': 'flask_saml2.sp.idphandler.IdPHandler',
            # 'CLASS': 'wgui.utils.flasksaml2patch.PatchedIdPHandler',
            'OPTIONS':
                {
                    'display_name': 'Google IDP',
                    'entity_id': 'https://accounts.google.com/o/saml2?idpid=C02hme6u2',
                    # config.config("idp_meta_url"),
                    'sso_url': 'https://accounts.google.com/o/saml2/idp?idpid=C02hme6u2',
                    # 'slo_url': 'http://localhost:8000/saml/logout/',
                    'certificate': certificate_from_file("/etc/wgui/google.pem"),
                },
        },
    ]
    app.register_blueprint(sp.create_blueprint(), url_prefix='/saml/')
    return app
