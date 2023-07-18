import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='lmco_email',
    version='0.1.2',
    author='Robert F1 King',
    author_email='Robert.F1.King@lmco.com',
    license='LICENSE.md',
    description='LMCO Email helper.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.us.lmco.com/apai/incubator/lmco_email",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'dnspython>=1.16.0'
    ],
)