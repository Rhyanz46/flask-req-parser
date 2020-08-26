from setuptools import setup


setup(
    name='flask_req_parser',
    version='0.1.4',
    url='https://github.com/Rhyanz46/flask-req-parser',
    license='BSD',
    author='Arian Saputra',
    author_email='rianariansaputra@gmail.com',
    description='Simple Request parser for flask',
    long_description=__doc__,
    # packages=find_packages(),
    # py_modules=['flask_req_parser'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    packages=['flask_req_parser'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)