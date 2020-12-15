import setuptools

setuptools.setup(
    name='betfair_api_client',
    packages=setuptools.find_packages(),
    version='0.2',
    description='Client for connecting to the Betfair Odds API and fetch betting market info',
    author='Michael Doran',
    author_email='mikrdoran@gmail.com',
    url='https://github.com/miksyr/betfair_api_client',
    download_url='https://github.com/miksyr/betfair_api_client/archive/v_02.tar.gz',
    keywords=['betfair', 'betfair odds api', 'sports betting'],
    install_requires=['requests==2.24.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
