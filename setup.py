from distutils.core import setup

setup(
    name = "swtagger",
    version = "0.1",
    packages=["shotwelldb"],
    scripts=["bin/swtagger.py"],
    author='Russell Heilling',
    author_email='chewtoy@s8n.net',
    url='http://russell.heilling.net/scripts',
    license="MIT",
    long_description=open('README.txt').read())
