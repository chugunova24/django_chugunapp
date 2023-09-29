from django.views.generic.base import ContextMixin


menu = [
        {'title': "Upload File", 'url_name': 'upload-file'},
        {'title': "Log-in", 'url_name': 'login'},
]



class DataMixin(ContextMixin):
        # extra_context = None
        # kwargs.setdefault('view', self)
        # if self.extra_context is not None:
        #         kwargs.update(self.extra_context)
        # return kwargs
        def get_user_context(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context = kwargs
                context['menu'] = menu

                if 'menu_selected' not in context:
                        context['menu_selected'] = 0

                return context