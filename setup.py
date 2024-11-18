from setuptools import setup, find_packages

setup(
    name="object-position-calculator",  # Unique name for the package
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for calculating the geographical position of detected objects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/object-position-calculator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
