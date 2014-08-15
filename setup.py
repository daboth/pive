try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
	name = 'pive',
	packages = ['pive'],
	version = '0.2.1',
	url = 'python-ive.org',
	license = 'BSD',
	description = 'Interactive visualization tool',
	long_description=open('README.txt').read(),
	author = 'David Bothe',
	author_email = 'davbothe@googlemail.com',
	classifiers = [
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Licence :: OSI Approved :: BSD Licence',
		'Operating System :: OS Independent',
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers,',
		'Environment :: Web Environment',		
		'Topic :: Scientific/Engineering :: Visualization',
		'Topic :: Software Development :: Libraries :: Python Modules'
	],
	install_requires = ['jinja2']

)