from setuptools import setup, find_packages

setup(
    name="tracor",
    version="0.1.1",  # Ensure this is the updated version
    packages=find_packages(),
    install_requires=[
        "colorama",
    ],
    entry_points={
        'console_scripts': [
            'tracor = tracor.core:main',
        ],
    },
    author="Jae Arlin",
    author_email="jairelan.2005@gmail.com",
    description="A tool for running Python scripts line by line with error handling and reporting.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/ArlinJae/Tracor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
