from setuptools import setup, Extension


long_description = "This package provides you some utils I think are useful. The package follows the " \
                       "modular-principle, instead of rewriting fields, admin pages etc., you create a mixin and " \
                       "reuse it for your projects!\n\nPlease see the package homepage for the documentation."

current_version = "1.1.0"

setup(
    name="django-common-utils",
    packages=["django_common_utils"],
    version=str(current_version),
    license="MIT",
    description="This package provides you some utils I think are useful.",
    long_description=long_description,
    author="Myzel394",
    author_email="myzel394.xyllian@gmail.com",
    url="https://github.com/Myzel394/django-common-utils",
    download_url="https://github.com/Myzel394/django-common-utils/archieve/v_" + str(current_version) + ".tar.gz",
    keywords=["django", "django-utils", "django-common", "django-models", "django-admin"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools"
    ],
    
)
