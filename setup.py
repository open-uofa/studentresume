from setuptools import setup

setup(
    name='studentresume',
    version='0.1.0',    
    description='Student Resume Generator Python package',
    url='https://github.com/open-uofa/studentresume',
    author='Diana, Ivan, Curtis, Yijing, Jason, Mohammed',
    author_email='dble@ualberta.ca, yzhang24@ualberta.ca, jrobock@ualberta.ca, ckennedy@ualberta.ca, qu8@ualberta.ca, alzafara@ualberta.ca',
    license='MIT License',
    license='MIT License',
    packages=['studentresume'],
    install_requires=[
                    'jsonschema==4.16.0',
                    'reportlab==3.6.11',         
                    ],
    package_data={'studentresume': ['requiredFields.json', 
                                    'sample.resume.json',
                                    'schema.json',
                                    'testonepage.resume.json',
                                    'themes/*',
                                    'fonts/*',]},
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.10',
    ],
)
