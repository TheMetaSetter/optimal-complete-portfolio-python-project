from setuptools import setup, find_packages

setup(
    name = 'optimal_complete_portfolio',
    version = '0.1',
    description = 'This is a Python project on portfolio optimization.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author = 'TheMetaSetter',
    author_email = 'nguyenanhkhoi0608@gmail.com',
    url = 'https://github.com/TheMetaSetter/optimal-complete-portfolio-python-project',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages = find_packages(),
    install_requires = [
        'cmake >= 3.26.3',
        'pandas >= 1.0.1',
        'numpy >= 1.24.3',
        'scipy >= 1.10.1',
        'xlsxwriter >= 3.1.2',
    ],
)