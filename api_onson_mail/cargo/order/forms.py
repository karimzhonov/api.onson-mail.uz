from django import forms
from import_export.forms import ConfirmImportForm, ImportForm
from unfold.widgets import SELECT_CLASSES, UnfoldAdminFileFieldWidget

from .models import Part


class OrderImportForm(ImportForm):
    part = forms.ModelChoiceField(Part.objects)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["import_file"].widget = UnfoldAdminFileFieldWidget(
            attrs=self.fields["import_file"].widget.attrs
        )
        self.fields["input_format"].widget.attrs["class"] = " ".join(
            [self.fields["input_format"].widget.attrs.get("class", ""), *SELECT_CLASSES]
        )

        self.fields["part"].widget.attrs["class"] = " ".join(
            [self.fields["part"].widget.attrs.get("class", ""), *SELECT_CLASSES]
        )


class OrderConfirmImportForm(ConfirmImportForm):
    part = forms.ModelChoiceField(Part.objects)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["part"].widget.attrs["class"] = " ".join(
            [self.fields["part"].widget.attrs.get("class", ""), *SELECT_CLASSES]
        )
