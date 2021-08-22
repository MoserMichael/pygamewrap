import os
import setuptools 

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setuptools.setup(
    name = "PygameWrap", 
    version = "0.0.1",
    author = "Michael Moser",
    author_email = "moser.michael@gmail.com",
    description = ("small wrapper/toolkit for writing games with pygame"),
    license = "MIT",                                                               
    keywords = "games; pygame; toolkit fo games",
    url = "https://github.com/MoserMichael/pygamewrap",
    packages=setuptools.find_packages(),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education"
    ],
    python_requires='>=3.6',
)
