from setuptools import setup

entry_point = (
    "command = studentresume.run:main"
)

setup(
    name='studentresume',
    version='0.1.0',    
    description='Student Resume Generator Python package',
    url='https://github.com/open-uofa/studentresume',
    author='Diana, Ivan, Curtis, Yijing, Jason, Mohammed',
    author_email='dble@ualberta.ca, yzhang24@ualberta.ca, jrobock@ualberta.ca, ckennedy@ualberta.ca, qu8@ualberta.ca, alzafara@ualberta.ca',
    license='MIT License',
    packages=['studentresume'],
    entry_points={"console_scripts": [entry_point]},
    install_requires=[
                    'jsonschema==4.17.3',
                    'reportlab==3.6.12',         
                    ],
    package_data={'studentresume': ['requiredFields.json', 
                                    'sample.resume.json',
                                    'schema.json',
                                    'theme-schema.json',
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
