from io import StringIO
from itertools import zip_longest

import pandas as pd
from django.contrib.auth.decorators import login_required
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
# from silk.profiling.profiler import silk_profile

# from .models import UserImage
from .forms import *
from .mixins import *
from .models import *
from .utils import one_field_to_array


@cache_page(60 * 2)
def home(request):
    return render(request, 'text_gen/home.html')


def about_me(request):
    return render(request, 'text_gen/about_me.html')

@method_decorator(login_required, name='dispatch')
class CsvReaderHome(View):
    form_class = FileListForm
    form_download_files = UploadFileForm
    template_name = "text_gen/csv_reader_home.html"
    files_set = None
    files_info = None

    on_bad_lines = "warn"
    na_filter = False

    def get(self, request, *args, **kwargs):
        print(f'request.GET ::: {request.GET}')

        user = request.user
        form = self.form_class(request.GET, user=user)

        # self.files_set =

        if '_info' in request.GET:

            print(f"form _info is_valid:: {form.is_valid()}")

            if form.is_valid():
                id_select_files = form.cleaned_data.get('select_file') #list

                if len(id_select_files) != 0:
                    print(f"id_select_files:: {id_select_files}")

                    queryset = form.queryset
                    query_names_of_columns = [[obj.file_id, obj.name] for obj in queryset["columns"] if str(obj.file_id) in id_select_files]
                    query_types_of_columns = [[obj.file_id, obj.type] for obj in queryset["columns"] if str(obj.file_id) in id_select_files]

                    names_of_columns = one_field_to_array(queryset_list=query_names_of_columns,
                                                          id_field=0,
                                                          to_arr_field=1)



                    types_of_columns = one_field_to_array(queryset_list=query_types_of_columns,
                                                          id_field=0,
                                                          to_arr_field=1)

                    if len(names_of_columns) == len(types_of_columns):
                        prepared_list = []

                        for key in names_of_columns:
                            prepared_list.append(names_of_columns[key])
                            prepared_list.append(types_of_columns[key])

                        filenames = [row[1] for row in queryset["files"] if str(row[0]) in id_select_files]

                        self.files_info = {'filenames': filenames,
                                           'data': list(zip_longest(*prepared_list, fillvalue=" "))}

        context = {
            'form': form,
            'files_set': self.files_set,
            'form_download_files': self.form_download_files,
            'files_info': self.files_info,
        }

        return render(request, 'text_gen/csv_reader_home.html', context)

    # Загрузка файлов
    # проверка csv на валидность содержимого
    # следать проверку на формат файла? проверка на размер
    def post(self, request, *args, **kwargs):
        print(f'request.POST ::: {request.POST}')

        user = request.user
        form = self.form_class(request.POST, user=user)

        if '_upload_file' in request.POST:
            self.form_download_files = UploadFileForm(request.POST, request.FILES)

            if self.form_download_files.is_valid():
                file = request.FILES['file']  # ЗДЕСЬ ЛУЧШЕ ВЗЯТЬ ОЧИЩЕННЫЕ ДАННЫЕ
                filename = file.name
                separator = self.form_download_files.cleaned_data.get('separator'),
                encoding = self.form_download_files.cleaned_data.get('encoding')
                decimal = self.form_download_files.cleaned_data.get('decimal')
                doublequote = self.form_download_files.cleaned_data.get('doublequote')

                encoding = Encodings.objects.get(id=encoding)
                separator = separator[0][0]

                # print(f"Tseparator:: {separator[0]}")
                print(f"separator:: {separator}")
                print(f"encoding:: {encoding}")
                print(f"decimal:: {decimal}")
                print(f"doublequote:: {doublequote}")

                content = ''
                for line in file:
                    content += line.decode('utf-8')

                csvStringIO = StringIO(content)

                try:
                    df = pd.read_csv(csvStringIO,
                                     sep=separator,
                                     encoding=encoding.name,
                                     decimal=decimal,
                                     doublequote=doublequote,
                                     na_filter=self.na_filter,
                                     on_bad_lines=self.on_bad_lines)
                except pd.errors.EmptyDataError:
                    return HttpResponse(f"{filename} is empty. We're can't load this file on server.")
                # except pd.errors.KeyError as key_error:
                #     return HttpResponse(f"For {filename}: {key_error}") # если мы видим эту ошибку, значит нет такой колонки в df


                is_exist = CsvFiles.objects.filter(user=user, filename=filename).exists()
                shape_df = df.shape

                if is_exist:
                    filename = HexFileName.get_available_name(name=filename,
                                                              max_length=100)  # должно получаться четко 100 символов

                answer = CsvFiles.objects.create(user=user,
                                                 content=content,
                                                 filename=filename,
                                                 n_rows=shape_df[0],
                                                 n_columns=shape_df[1],
                                                 separator=separator,
                                                 encoding=encoding,
                                                 decimal=decimal,
                                                 doublequote=doublequote)

                try:
                    id_filename = CsvFiles.objects.get(user=user, filename=filename)
                except CsvFiles.DoesNotExist:
                    raise Exception("This filename is not found.")

                dtypes = df.dtypes.to_list()

                for i in range(0, len(dtypes)):
                    if dtypes[i] == 'object':
                        dtypes[i] = 'string'

                columns = df.columns
                bulk_list = [ColumnsOfCsvFiles(file=id_filename,
                                               name=columns[idx],
                                               type=dtypes[idx]) for idx in range(0, len(columns))]

                bulk_msj = ColumnsOfCsvFiles.objects.bulk_create(bulk_list)

                return redirect('/file-reader/csv-reader-home')
                # return reverse('csv-reader-home') # сделать реверс с GET-запросом и удалить DRY код в данной фун-ции

            else:
                self.form_download_files = UploadFileForm()  # ВЕРНУТЬ ПУСТУЮ ФОРМУ С ОШИБКОЙ

        if '_remove' in request.POST:
            if form.is_valid():
                id_select_files = form.cleaned_data.get('select_file') #list

                if len(id_select_files) != 0:
                    CsvFiles.objects.filter(user=user, id__in=id_select_files).delete()

                return redirect('/file-reader/csv-reader-home')


# FormView
@method_decorator(login_required, name='dispatch')
class CsvReaderFilter(View):
    form_class = FilePropertiesFilterForm
    template_name = "text_gen/csv_reader_filter.html"
    table_html = None
    table_csv = None
    max_row = 500
    max_columns = 100
    # errors = []

    on_bad_lines = "warn"
    na_filter = False

    def get(self, request, *args, **kwargs):
        print(f'request.GET ::: {request.GET}\n')

        init_id_file = request.GET.get('select_file')
        print(f"init_id_file:: {init_id_file}")


        user = request.user
        print(f"user: {user}")

        if init_id_file:
            initial = {"select_file": str(init_id_file)}
            form = self.form_class(request.GET, user=user, initial=initial)
        else:
            form = self.form_class(request.GET, user=user)

        files_set = form.queryset["files"]
        data_of_file = [ColumnsOfCsvFiles.to_dict(obj)  for obj in form.queryset["columns"]]

        if '_generate' in request.GET:

            print(f"form.is_valid():: {form.is_valid()}\n")
            print(f"form.errors:: {form.errors}\n")


            if form.is_valid():
                file_id = form.cleaned_data.get("select_file")
                select_columns = form.cleaned_data.get("select_columns_of_file")
                sort_by = form.cleaned_data.get("sort_by")
                # separator = form.cleaned_data.get("separator")
                # encoding = form.cleaned_data.get("encoding")
                # decimal = form.cleaned_data.get("decimal")
                # doublequote = form.cleaned_data.get("doublequote")

                # if file_id and select_columns and sort_by and \
                #     separator and decimal:
                if file_id and select_columns and sort_by:
                    # pass

                    content = select_columns[0].file.content
                    encoding = select_columns[0].file.encoding.name
                    decimal = select_columns[0].file.decimal
                    separator = select_columns[0].file.separator
                    doublequote = select_columns[0].file.doublequote
                    sort_by = sort_by.name
                    select_columns = [obj.name for obj in select_columns]


                    columns = select_columns

                    print(f"select_columns :: {select_columns}")
                    print(f"sort_by :: {sort_by}")
                    print(f"columns:: {columns}")
                    print(f"encoding:: {encoding}")
                    print(f"separator:: {separator}")
                    print(f"decimal:: {decimal}")
                    print(f"doublequote:: {doublequote}")
                    print(f"sort_by:: {sort_by}")

                    csvStringIO = StringIO(content)

                    try:
                        df = pd.read_csv(csvStringIO,
                                         sep=separator,
                                         encoding=encoding,
                                         decimal=decimal,
                                         doublequote=doublequote,
                                         na_filter=self.na_filter,
                                         on_bad_lines=self.on_bad_lines)

                        sorted_df = df[columns].sort_values(by=[sort_by], ascending=True)

                        self.table_html = sorted_df[:self.max_row][:self.max_columns].to_html(classes=["table",
                                                                                                       "table-striped",
                                                                                                       "table-bordered",
                                                                                                       "table-sm",
                                                                                                       "table-hover"],
                                                                                              index=False,
                                                                                              table_id="dtHorizontalVerticalExample")

                        self.table_csv = sorted_df.to_csv(index=False,
                                                     sep=separator,
                                                     encoding=encoding,
                                                     decimal=decimal,
                                                     doublequote=doublequote)

                    except KeyError:
                        form.add_error('select_columns_of_file', "No column with that name found. Try changing csv file reading options (separator, decimal, doublequote, encodings).")

                    csvStringIO.close()




        context = {
            'form': form,
            'files_set': files_set,
            'data_of_file': data_of_file,
            'table_html': self.table_html,
            'table_csv': self.table_csv,
        }

        return render(request, self.template_name, context)
