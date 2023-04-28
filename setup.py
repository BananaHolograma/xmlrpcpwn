from setuptools import find_packages, setup


def dependencies(imported_file):
    """ __Doc__ Handles dependencies """
    with open(imported_file) as file:
        return file.read().splitlines()


with open("README.md") as file:
    setup(
        name="xmlrpcpwn",
        license="MIT",
        description="Interact with xmlrpc.php file on Wordpress sites",
        long_description=file.read(),
        author="s3r0s4pi3ns",
        version="1.0.0",
        author_email="",
        url="https://github.com/s3r0s4pi3ns/xmlrpcpwn",
        packages=find_packages(exclude=('tests')),
        package_data={'xmlrpcpwn': ['*.txt']},
        entry_points={
            'console_scripts': [
                'xmlrpcpwn = scripts.xmlrpcpwn:main'
            ]
        },
        install_requires=dependencies('requirements.txt'),
        include_package_data=True)
