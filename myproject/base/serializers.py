import io

from drf_extra_fields.fields import Base64FileField

from pypdf import PdfReader
from pypdf.errors import PdfReadError
from rest_framework.exceptions import ValidationError


class DynamicFieldsSerializerMixin:

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            not_allowed = set(exclude)
            for field_name in not_allowed:
                self.fields.pop(field_name)


class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']

    def get_file_extension(self, filename, decoded_file):
        try:
            PdfReader(io.BytesIO(decoded_file))
        except PdfReadError as e:
            raise ValidationError("Некорректный PDF файл.")
        else:
            return 'pdf'