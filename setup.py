import pathlib

from setuptools import setup

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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='NTHU, iLMS',
    packages=['ilmsdump', 'ilmsdump.gui', 'ilmsserve'],
    package_data={
        'ilmsdump': ['gui/ilmsdump.ui'],
        'ilmsserve': ['templates/*.j2'],
    },
    python_requires='>=3.8, <4',
    install_requires=[
        'aiohttp',
        'yarl',
        'lxml',
        'click',
        'wcwidth',
        'pillow',
        'aiohttp-jinja2',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-asyncio',
            'pytest-cov',
        ],
        'gui': [
            'pyside6',
        ],
    },
    entry_points={
        'console_scripts': [
            'ilmsdump=ilmsdump:main',
            'ilmsserve=ilmsserve:main',
        ],
    },
)
