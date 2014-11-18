from setuptools import setup, find_packages
import sys, os

setup(
    name='dip-ui',
    version=0.1,
    description="SWORDv2 command line deposit client",
    long_description="""\
dio-ui - Command line tool for deposit to SWORDv2-enabled repository""",
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="sword-app atom sword2 http cli",
    author="Graham Klyne",
    author_email='graham.klyne@oerc.ox.ac.uk',
    url="https://github.com/CottageLabs/dip-ui",
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=["sword2", "lxml", "dip"],
    entry_points =
        {
        'console_scripts':
            [ 'dip = dipcmd.dipmain:runMain',
            ]
        }
)

# For testing, also requires SSS:
#
#     $ pip freeze
#     SSS==2.0
#     dip==0.1
#     httplib2==0.9
#     lxml==2.3.4
#     nose==1.3.4
#     sword2==0.1
#     web.py==0.37
#     wsgiref==0.1.2
