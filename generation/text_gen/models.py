from django.db import models

class Metrics(models.Model):
    text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)  # DateTimeField


class TextGen(models.Model):
    input = models.TextField(null=True)
    min_length = models.IntegerField(null=True)
    max_length = models.IntegerField(null=True)
    generation_text = models.TextField(null=True)
    translated_text = models.TextField(null=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)
        # ordering = ('date',)

    def __str__(self):
        return self.generation_text

    # def save(self, text_new, *args, **kwargs):
    #         self.text_new = text_new
    #         super(TextGen, self).save(*args, **kwargs)


class Translator(models.Model):
    input = models.TextField()
    translated_text = models.TextField()
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.translated_text








