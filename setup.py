from distutils import sysconfig
from distutils.command.build import build as DistutilsBuild
from setuptools import setup, Extension
import sys
import subprocess

def build_osx():
    subprocess.check_call(['cmake', '-DCMAKE_BUILD_TYPE=Release', '-DBUILD_PYTHON=ON', '-DBUILD_JAVA=OFF', '-DPYTHON_INCLUDE_DIR={}'.format(sysconfig.get_python_inc())], cwd='doom_py')
    subprocess.check_call(['make'], cwd='doom_py')
    subprocess.check_call(['rm', '-f', 'vizdoom.so'], cwd='doom_py')
    subprocess.check_call(['ln', '-s', 'bin/python/vizdoom.so', 'vizdoom.so'], cwd='doom_py')

    # Symlink to the correct vizdoom binary
    subprocess.check_call(['rm', '-f', 'bin/vizdoom'], cwd='doom_py')
    subprocess.check_call(['ln', '-s', 'vizdoom.app/Contents/MacOS/vizdoom', 'bin/vizdoom'], cwd='doom_py')

def build_linux():
    subprocess.check_call(['cmake', '-DCMAKE_BUILD_TYPE=Release', '-DBUILD_PYTHON=ON', '-DBUILD_JAVA=OFF', '-DPYTHON_INCLUDE_DIR={}'.format(sysconfig.get_python_inc())], cwd='doom_py')
    subprocess.check_call(['make'], cwd='doom_py')
    subprocess.check_call(['rm', '-f', 'vizdoom.so'], cwd='doom_py')
    subprocess.check_call(['ln', '-s', 'bin/python/vizdoom.so', 'vizdoom.so'], cwd='doom_py')

def build_windows():
    # THIS IS UNTESTED
    subprocess.check_call(['cmake', '-DCMAKE_BUILD_TYPE=Release', '-DBUILD_PYTHON=ON', '-DBUILD_JAVA=OFF', '-DPYTHON_INCLUDE_DIR={}'.format(sysconfig.get_python_inc())], cwd='doom_py')
    subprocess.check_call(['make'], cwd='doom_py')
    subprocess.check_call(['rm', '-f', 'vizdoom.so'], cwd='doom_py')
    subprocess.check_call(['ln', '-s', 'bin/python/vizdoom.so', 'vizdoom.so'], cwd='doom_py')

if sys.platform.startswith("darwin"):
    platname = "osx"
    build_func = build_osx
elif sys.platform.startswith("linux"):
    platname = "linux"
    build_func = build_linux
elif sys.platform.startswith("windows"):
    platname = "win"
    build_func = build_windows

# For building Doom
class BuildDoom(DistutilsBuild):
    def run(self):
        try:
            build_func()
        except subprocess.CalledProcessError as e:
            print("Could not build doom-py: %s" % e)
            raise
        DistutilsBuild.run(self)

setup(name='doom-py',
      version='0.0.1',
      description='Python bindings to ViZDoom',
      url='https://github.com/openai/doom-py',
      author='OpenAI Community',
      author_email='gym@openai.com',
      packages=['doom_py'],
      cmdclass={'build': BuildDoom},
      setup_requires=['numpy'],
      install_requires=['numpy'],
      tests_require=['nose2'],
      classifiers=['License :: OSI Approved :: MIT License'],
      include_package_data=True,
)
