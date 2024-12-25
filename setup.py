from setuptools import setup, find_packages

setup(
    name="next_innovation_realty",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask>=2.0.0',
        'SQLAlchemy>=1.4.0',
        'Flask-Login>=0.5.0',
        'Flask-WTF>=0.15.0',
        'email-validator>=1.1.3',
        'python-dotenv>=0.19.0',
        'gunicorn>=20.1.0'
    ]
) 