from django.test.runner import DiscoverRunner
from django.conf import settings


class MyDiscoverRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)

        print('=' * 30)
        print('call setup_test_environment')
        print('-' * 20)
        print(f'{settings.TEST_RUNNER}')
        print('=' * 30)
