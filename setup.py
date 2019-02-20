from setuptools import setup

setup(name='py_midicsv',
    version='1.8.1',
    description='A library for converting MIDI files from and to CSV format.',
    long_description='''
        py_midicsv is a Python port of the tools midicsv and csvmidi (http://www.fourmilab.ch/webtools/midicsv/),
        which enable the conversion of MIDI files from and to CSV files, making them easier to work with.
        The main advantage to representing MIDI events as text is the easy application
        of text processing to these events, making MIDI files easy to work with and quick to modify.
        ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Multimedia :: Sound/Audio :: MIDI',
        ],
    keywords='midi converter csv',
    url='https://github.com/timwedde/py_midicsv',
    author='Tim Wedde',
    author_email='timwedde@icloud.com',
    license='MIT',
    packages=['py_midicsv', 'py_midicsv.midi'],
    # install_requires=[],
    include_package_data=True,
    zip_safe=False
)
