from django import forms

from .models import *
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from django.db.models import Prefetch

# Custom things
class MyModelChoiceIterator(forms.models.ModelChoiceIterator):
    """Variant of Django's ModelChoiceIterator to prevent it from always re-fetching the
    given queryset from database.
    """

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset
        for obj in queryset:
            yield self.choice(obj)

class MyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """Variant of Django's ModelMultipleChoiceField to prevent it from always
    re-fetching the given queryset from database.
    """

    iterator = MyModelChoiceIterator

    def _get_queryset(self):
        return self._queryset

    def _set_queryset(self, queryset):
        self._queryset = queryset
        self.widget.choices = self.choices

    queryset = property(_get_queryset, _set_queryset)



class MyModelChoiceField(forms.ModelChoiceField):
    """Variant of Django's ModelMultipleChoiceField to prevent it from always
    re-fetching the given queryset from database.
    """

    iterator = MyModelChoiceIterator

    def _get_queryset(self):
        return self._queryset

    def _set_queryset(self, queryset):
        self._queryset = queryset
        self.widget.choices = self.choices

    queryset = property(_get_queryset, _set_queryset)

# Forms

class UploadFileForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ENCODING_CHOICES = Encodings.objects.all().values_list()  # queryset

        SEPARATOR_CHOICES = (
            (",", ","),
            (";", ";"),
        )

        DECIMAL_CHOICES = (
            (".", "."),
            (",", ","),
        )

        self.fields['file'] = forms.FileField()
        self.fields['separator'] = forms.ChoiceField(choices=SEPARATOR_CHOICES, initial=1)
        self.fields['encoding'] = forms.ChoiceField(choices=ENCODING_CHOICES, initial=1)
        self.fields['decimal'] = forms.ChoiceField(choices=DECIMAL_CHOICES, initial=2)
        self.fields['doublequote'] = forms.BooleanField(initial=True, required=False)




        self.fields['file'].widget.attrs.update({
            "class": "form-control",
        })
        self.fields['separator'].widget.attrs.update({
            "class": "form-control",
        })
        self.fields['encoding'].widget.attrs.update({
            "class": "form-control",
        })
        self.fields['decimal'].widget.attrs.update({
            "class": "form-control",
        })
        self.fields['doublequote'].widget.attrs.update({
            "class": "form-check form-switch form-check-input",
        })




class FileFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.queryset = self.get_queryset(self.user)

        self.fields['select_file'] = forms.ChoiceField(choices=self.queryset["files"])
        self.fields['select_columns_of_file'] = MyModelMultipleChoiceField(queryset=self.queryset["columns"])

        self.fields["select_file"].widget.attrs.update({"id": "idSelectFile",
                                                        "class": "form-control",
                                                        })
        self.fields["select_columns_of_file"].widget.attrs.update({"id": "idSelectColumnsOfFile",
                                                                   "class": "form-control",
                                                                   })

    def get_queryset(self, user):
        columns_list = ColumnsOfCsvFiles.objects.select_related("file").filter(file_id__user=user)

        files_list = [[i.file_id, i.file.filename] for i in list(columns_list)]
        files_list = [i for n, i in enumerate(files_list) if i not in files_list[:n]]



        # print(f"files_list:: {files_list}")


        # columns_list = ColumnsOfCsvFiles.objects.filter(file_id__user=user).values_list("id", "name")
        # files_list = columns_list.values_list("file_id__id", "file_id__filename").distinct()

        return {"files": files_list, "columns": columns_list}

    def clean_file(self):
        file = self.cleaned_data.get("select_file",  False)
        if file is False:
            raise ValidationError("Fill in file field.")

        return file

    def clean_columns(self):
        columns = self.cleaned_data.get("select_columns_of_file",  False)
        if columns is False:
            raise ValidationError("Fill in columns field.")

        return columns




class FileListForm(FileFilterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('select_columns_of_file', None)
        # self.queryset = self.get_queryset(self.user)

        self.fields['select_file'] = forms.MultipleChoiceField(choices=self.queryset["files"], required=False)
        self.fields['select_file'].widget.attrs.update({
                                                        # "id": "idSelectFile",
                                                        "class": "form-control h-100",
                                                        })

    def get_queryset(self, user):
        columns_list = ColumnsOfCsvFiles.objects.select_related("file"
                                                                ).filter(file_id__user=user
                                                                         ).only("id", "file_id", "name", "type",
                                                                                "file__filename")

        files_list = [[i.file_id, i.file.filename] for i in list(columns_list)]
        files_list = [i for n, i in enumerate(files_list) if i not in files_list[:n]]

        return {"files": files_list, "columns": columns_list}




class FilePropertiesFilterForm(FileFilterForm):
# class FilePropertiesFilterForm(FileFilterForm, UploadFileForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sort_by'] = MyModelChoiceField(queryset=self.queryset["columns"])
        self.fields['sort_by'].widget.attrs.update({"id": "idSelectSortBy",
                                                    "class": "form-control",
        })

        self.order_fields(self.Meta.fields)


    def get_queryset(self, user):
        columns_list = ColumnsOfCsvFiles.objects.select_related("file", "file__encoding"
                                                                ).filter(file_id__user=user)

        files_list = [[i.file_id, i.file.filename] for i in list(columns_list)]
        files_list = [i for n, i in enumerate(files_list) if i not in files_list[:n]]

        return {"files": files_list, "columns": columns_list}


    class Meta:
        fields = ('select_file', 'select_columns_of_file', 'sort_by',)
        # fields = ('select_file', 'select_columns_of_file', 'sort_by', 'separator', 'encoding', 'decimal', 'doublequote',)
