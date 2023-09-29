from django.db import models
from django.contrib.auth.models import User

class Encodings(models.Model):
    name = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return str(self.name)

class CsvFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    content = models.TextField(blank=True, null=True)  # никуда не сохраняем
    filename = models.CharField(max_length=100, blank=False, null=True)
    n_rows = models.PositiveIntegerField(blank=False)
    n_columns = models.PositiveIntegerField(blank=False)

    separator = models.CharField(max_length=10, default=",", blank=False, null=True)
    encoding = models.ForeignKey(Encodings, default="1", on_delete=models.PROTECT, blank=False)
    decimal = models.CharField(max_length=10, default=".", blank=False, null=True)
    doublequote = models.BooleanField(default=True, blank=False, null=True)

    def __str__(self):
        return str(self.filename)


class ColumnsOfCsvFiles(models.Model):
    file = models.ForeignKey(CsvFiles, on_delete=models.CASCADE)
    name = models.TextField(blank=False) # проверка на размер файла
    type = models.CharField(max_length=30, blank=False, null=True)

    def __str__(self):
        return str(self.name)

    def to_dict(obj):
        if obj == None:
            return None

        dictionary = {}
        dictionary["id"] = obj.id
        dictionary["name"] = obj.name
        dictionary["file_id"] = obj.file_id
        dictionary["filename"] = obj.file.filename


        return dictionary





