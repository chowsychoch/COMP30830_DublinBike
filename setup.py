from setuptools import setup

setup(
    name='COMP30830_DublinBike',
    version='1.0',
    packages=['utilities','models'],
    url='https://github.com/chowsychoch/COMP30830_DublinBike.git',
    license='',
    author='3Sum',
    author_email='ming-ham.ta@ucdconnect.ie',
    description='data scraping and store data in RDS',
    install_require={
      'sqlalchemy',
        'datetime',
        'requests',
        'json',
        'dotenv',
    },
    entry_points={
        'console_scripts': ['tSum_dublinBike=main:main']
    }
)
