from setuptools import setup

setup(name='pydicsv',
    version='1.0.0',
    description='A library for converting MIDI files from and to CSV format.',
    long_description='''
        pydicsv is a Python port of the tools midicsv and csvmidi, which enable
        the conversion of MIDI files from and to CSV files, making them easier to work with.
        The main advantage to representing MIDI events as text is the easy application
        of text processing to these events, making MIDI files easy to work with and quick to modify.
        ''',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Multimedia :: Sound/Audio :: MIDI',
        ],
    keywords='midi converter csv',
    url='https://github.com/timwedde/pydicsv',
    author='Tim Wedde',
    author_email='timwedde@icloud.com',
    license='MIT',
    packages=['pydicsv'],
    # install_requires=[],
    include_package_data=True,
    zip_safe=False
)
