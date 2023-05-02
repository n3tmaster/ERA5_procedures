from setuptools import find_packages, setup
setup(
    name='dolibs',
    packages=find_packages(include=['dolibs']),
    version='0.1.0',
    url='https://github.com/n3tmaster/ERA5_procedures',
    description='Library for Drought Observatory',
    author='Leandro Rocchi - CNR',
    author_email='leandro.rocchi@cnr.it',
    license='MIT',
    install_requires=['cdsapi','numpy','xarray','SQLAlchemy','psycopg2-binary'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
