# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import contextlib

from odoo.tests.common import TransactionCase, tagged
from odoo.tools import DotDict

from odoo.addons.website.tools import MockRequest


@tagged("-at_install", "post_install")
class CommonEndpoint(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_env()
        cls._setup_records()
        cls.route_handler = cls.env["endpoint.route.handler"]

    @classmethod
    def _setup_env(cls):
        cls.env = cls.env(context=cls._setup_context())

    @classmethod
    def _setup_context(cls):
        return dict(
            cls.env.context,
            tracking_disable=True,
        )

    @classmethod
    def _setup_records(cls):
        pass

    @contextlib.contextmanager
    def _get_mocked_request(
        self, env=None, httprequest=None, extra_headers=None, request_attrs=None
    ):
        current_website = self.env['website'].get_current_website()
        with MockRequest(env or self.env, website=current_website) as mocked_request:
            mocked_request.httprequest = (
                DotDict(httprequest) if httprequest else mocked_request.httprequest
            )
            headers = {}
            headers.update(extra_headers or {})
            mocked_request.httprequest.headers = headers
            request_attrs = request_attrs or {}
            for k, v in request_attrs.items():
                setattr(mocked_request, k, v)
            mocked_request.make_response = lambda data, **kw: data
            mocked_request.registry._init_modules.union(['website'])
            yield mocked_request
