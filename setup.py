import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
 long_description = fh.read()

setuptools.setup(
 name="selfTracking",
 version="0.0.1",
 author="Jan Skorupski",
 author_email="janskorupski9@gmail.com",
 description="A small package for self-tracking activity",
 long_description=long_description,
 long_description_content_type="text/markdown",
 url="https://github.com/janskorupski/selfTracking",
 package_dir={'': 'src'},
 packages=setuptools.find_packages(where='src'),
 classifiers=[
 "Programming Language :: Python :: 3",
 "License :: OSI Approved :: MIT License",
 "Operating System :: Windows",
 ],
 install_requires=["pandas", "mouse", "keyboard", "pywin32"],
 python_requires='>=3.6',
)