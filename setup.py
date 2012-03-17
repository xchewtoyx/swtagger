from distutils.core import setup

setup(
    name = "swtagger",
    version = "0.1",
    packages=["shotwelldb"],
    scripts=["bin/swtagger.py"],
    license="MIT",
    long_description=open('README.txt').read())
