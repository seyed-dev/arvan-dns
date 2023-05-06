from setuptools import setup

setup(
    name='arvan_dns',
    version='1.0.0',
    description='Arvan DNS updater',
    py_modules=['arvan_dns'],
    install_requires=[
        'requests',
        'argparse'
    ],
    entry_points={
        'console_scripts': [
            'arvan-dns = arvan_dns:main'
        ]
    },
    author='SeYeD.DeV',
    author_email='me@seyed.dev',
    url='https://github.com/seyed-dev/arvan-dns'
)
