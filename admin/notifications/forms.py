from html import parser

import nh3
from django import forms
from jinja2 import Environment

from notifications import contexts, enums, models


class TemplateAdminForm(forms.ModelForm):
    class Meta:
        model = models.Template
        exclude = ("body",)

    def clean_body_editable(self):
        template_str = str(self.cleaned_data["body_editable"])
        mime_type = self.cleaned_data["mime_type"]
        environment = Environment()
        template = environment.from_string(template_str)
        try:
            rendered_template = template.render(**contexts.CONTEXT_VARS_EXAMPLE)

            if mime_type == enums.MimeType.TEXT_HTML:
                rendered_html = nh3.clean(rendered_template)
                parser.HTMLParser().feed(rendered_html)
        except Exception as e:
            raise forms.ValidationError(str(e))
