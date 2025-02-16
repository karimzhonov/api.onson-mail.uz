# coding: utf-8
from rest_framework.renderers import BaseRenderer


class XLSXRenderer(BaseRenderer):
    """ Renderer for PDF binary content. """

    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    format = 'xlsx'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Return the PDF data as it is
        """
        return data
