from setuptools import setup
 
setup(
    name='studentresume',
    version='0.1.0',    
    description='Student Resume Generator Python package',
    url='https://github.com/open-uofa/studentresume',
    author='Diana',
    author_email='dble@ualberta.ca',
    license='MIT License',
    packages=['studentresume'],
    install_requires=[
                    'jsonschema==4.16.0',
                    'reportlab==3.6.11',         
                    ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.10',
    ],
)