import setuptools

PACKAGE_NAME = 'camxes_py'
PACKAGE_DIR = 'camxes_py'


packages = setuptools.find_packages(PACKAGE_DIR)
packages.append('')
packages = list(map(lambda n: PACKAGE_NAME+"."+n, packages))


with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name=PACKAGE_NAME,
    version="0.8.1",
    author="Robin Lee Powell",
    author_email="rlpowell@digitalkingdom.org",
    description="A pure Python implementation of the lojban 'camxes' PEG parser.",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="https://github.com/lojban/camxes-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Text Processing :: Linguistic",
    ],
    package_dir={PACKAGE_NAME: PACKAGE_DIR},
    packages=packages,
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["parsimonious==0.8.1"],
    scripts=["camxes.py", "vlatai.py", "vlatai-bot.py"],
)
