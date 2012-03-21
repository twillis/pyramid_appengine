from setuptools import setup, find_packages

version = "0.5"
requires = ["pyramid<=1.2", "webob==1.1.1"]
setup(name='pyramid_appengine',
      version=version,
      description="Scaffold + Tools for creating/developing pyramid applications on Google App Engine",
      long_description="""\
""",
      classifiers=[],
      keywords='',
      author='Tom Willis',
      author_email='tom@batterii.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""
      # -*- Entry points: -*-
      [paste.paster_create_template]
      appengine_starter=pyramid_appengine.scaffolds:PyramidAppEngineStarterTemplate
      [pyramid.scaffold]
      appengine_starter=pyramid_appengine.scaffolds:PyramidAppEngineStarterTemplate
      """,
      )
