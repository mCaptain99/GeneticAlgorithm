import time

from oe.tests import test_config
from oe.tests.test import make_test

start = time.time()
make_test(**test_config.default)
end = time.time()

print('time: {}'.format(end - start))

