from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()


long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='ilmsdump',
    version='0',
    description='Dump NTHU iLMS data before it is shut down',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/afq984/ilmsdump',
    author='Yu, Li-Yu',
    author_email='afq984@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='NTHU, iLMS',
    py_modules=['ilmsdump'],
    python_requires='>=3.7, <4',
    install_requires=[
        'aiohttp[speedups]',
        'yarl',
        'lxml',
        'click',
    ],
    entry_points={  # Optional
        'console_scripts': [
            'ilmsdump=ilmsdump:main',
        ],
    },
)
