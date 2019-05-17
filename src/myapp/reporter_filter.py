from django.views.debug import SafeExceptionReporterFilter


class MyReporterFilter(SafeExceptionReporterFilter):
    """ 自作のマスク機能 """
    def get_post_parameters(self, request):
        """ POSTデータをマスク """
        if request is None:
            return {}

        cleansed = request.POST.copy()
        cleansed['grape'] = '?' * 30

        return cleansed

    def get_traceback_frame_variables(self, request, tb_frame):
        """ トレースバック中のローカル変数をマスク """
        cleansed = {}
        for name, value in tb_frame.f_locals.items():
            if name == 'year':
                value = '?' * 30
            else:
                value = self.cleanse_special_types(request, value)
            cleansed[name] = value

        return cleansed.items()
