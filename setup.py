from setuptools import setup, find_packages

version = "1.0"

description = """

"""

long_description = "" 
    

setup(name='yc1304',
      author="Andrea Censi",
      author_email="andrea@cds.caltech.edu",
      url='http://github.com/AndreaCensi/boot_servo_demo',
      
      description=description,
      long_description=long_description,
      keywords="robotics, learning, bootstrapping",
      license="LGPL",
      
      classifiers=[
        'Development Status :: 4 - Beta',
        # 'Intended Audience :: Developers',
        # 'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        # 'Topic :: Software Development :: Quality Assurance',
        # 'Topic :: Software Development :: Documentation',
        # 'Topic :: Software Development :: Testing'
      ],
      
      install_requires=[
        'ConfTools>=1.0,<2',
        'PyContracts>=1.2,<2',
        'PyYAML',
        'python-cjson',
        'PyGeometry',
        'quickapp',
        'BootOlympics'
      ],
      entry_points={
     'console_scripts': [
       'yc = yc1304.campaign:main',
       'servo_field = yc1304.s10_servo_field.go:main'
      ]
      },
      version=version,
      # download_url='http://github.com/AndreaCensi/boot_servo_demo/tarball/%s' % version,
      package_dir={'': 'src'},
      packages=find_packages('src'),
      tests_require=['nose']
)

