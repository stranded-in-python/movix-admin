from django import forms
from jinja2 import Environment

from notifications import contexts, models


class TemplateAdminForm(forms.ModelForm):
    class Meta:
        model = models.Template
        exclude = ("body",)

    def clean_body_editable(self):
        template_str = str(self.cleaned_data["body_editable"])
        environment = Environment()
        template = environment.from_string(template_str)
        try:
            template.render(**contexts.CONTEXT_VARS_EXAMPLE)
        except Exception as e:
            raise forms.ValidationError(str(e))
