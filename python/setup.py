from setuptools.command.test import test as TestCommand
import sys
from distutils.core import setup


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)

setup(name='RSS Catalog',
      version='0.1',
      description='Scripts for building RSS catalog',
      author='Paul Kernfeld',
      author_email='paulkernfeld@gmail.com',
      url='fill this in soon',
      tests_require=['tox'],
      packages=[],
      )
