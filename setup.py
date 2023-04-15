import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='econdata',
    version = '1.0',
    authors = [
        'Mauricio Alvarado',
        'Andrei Romero'
    ],
    description = 'Extracción de series de tiempo de las cinco principales instituciones económicas para el Perú',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mauricioalvaradoo/econdata',
    classifier = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ], 
    package_dir={'':'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6',
    install_requires = [
        'pandas',
        'numpy',
        'yfinance',
        'requests'
    ]
)


