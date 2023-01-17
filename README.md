[![Python version](https://badgen.net/badge/python/3.10/green)](Pipfile)
[![License](https://img.shields.io/github/license/octopusinvitro/image-pipeline)](https://github.com/octopusinvitro/image-pipeline/blob/main/LICENSE.md)


# README

This project is a data pipeline that consumes two single-band images from Sentinel 1 and converts them to the COG format, as well as generating overview and thumbnail images.

It uses [this python scafold](https://github.com/octopusinvitro/python-scafold) as a very simple starter that includes some development best practices and software industry standards, including:

* a README with instructions
* Using `pipenv` for automatic dependency management and deterministic builds
* Tests, with `unittest` as a testing framework.
* Linting, using `flake8`
* Debugging with `ipdb`
* A `bin` folder to place bash scripts for basic commands and automation.
* A CI configuration (this one is not used in the current project, for simplification)

Dependencies particular to the project:
* python 3.10
* GDAL >=3.1 as it is needed for `rasterio`.
* ImageMagick for the `wand` package used in asset creation.
* Dependencies at pinned versions listed in `Pipefile` (they include numpy, which is also needed by `rasterio`).

## Setup

### Docker

It is strongly recommended to use the provided Docker image, as then **there is no need to install anything**.  It is based on [the `osgeo/gdal:ubuntu-small-3.6.2` image](https://hub.docker.com/layers/osgeo/gdal/ubuntu-small-3.6.2/images/sha256-f168d11d3afdbe48f7bd99004439d6692f8ad47fa936155d93b54dd04000eb0f?context=explore) that contains GDAL and all the needed dependencies, since GDAL is needed in order to use the `rasterio` package. You can check Docker installation instructions for your system [in the docker website](https://docs.docker.com/get-docker/).

Note that the provided Docker image is for local development, and not intended to be used in an production environment.

To start the container:

```bash
docker compose up -d --build
```

Jump into the container and work normally:

```bash
docker compose exec app bash
```

When you are done, stop the container with:

```bash
docker compose down
```

The project's root directory is mounted so any changes you do to files inside the container will also happen locally and viceversa.

### Local

If you do not want to use the Docker image provided, then you should:

* Install GDAL in your system (the `rasterio` package's website has [instructions for several platforms](https://rasterio.readthedocs.io/en/latest/installation.html) or you could also check [GDAL's download page](https://gdal.org/download.html)).
* Install ImageMagick following [the intructions in their website](https://imagemagick.org/script/download.php).
* Install `pipenv` (`pip install -U pip && pip install pipenv`).
* Install the project's dependencies (`pipenv install`).
* prepend `pipenv run` in front of python related commands.


## To run

Download a zip for your area of interest from [the Sentinel data download page](https://scihub.copernicus.eu/dhus/#/home) (free but you need to sign up for an account), containing two single-band images of the red and green channel (VV and VH). Then unzip it in the `data` folder.

Jump into the Docker container and run the project providing the VV polarization tiff (used for the red channel) and the VH polarization tiff (used for the green channel) as arguments:

```sh
. bin/run data/path/to/VV.tiff data/path/to/VH.tiff
```

For lack of time the code has only been tested against this particular set: `S1A_IW_GRDH_1SDV_20220810T182833_20220810T182858_044494_054F43_5CD6.SAFE`

To obtain the same results as me, download it and try:

```sh
. bin/run \
  ./data/S1A_IW_GRDH_1SDV_20220810T182833_20220810T182858_044494_054F43_5CD6.SAFE/measurement/s1a-iw-grd-vv-20220810t182833-20220810t182858-044494-054f43-001.tiff \
  ./data/S1A_IW_GRDH_1SDV_20220810T182833_20220810T182858_044494_054F43_5CD6.SAFE/measurement/s1a-iw-grd-vh-20220810t182833-20220810t182858-044494-054f43-002.tiff
```

The processed images will be created in the `output` folder.

## To test

Jump into the Docker container and run:

```sh
. bin/test                    # all tests
. bin/test tests.test_file    # single test file
```

## To lint

Jump into the Docker container and run:

```sh
. bin/lint
```

## To debug

Throw `import ipdb; ipdb.set_trace()` in the part of the code you want to debug and run the relevant test. You can type `interact` in the prompt for a better user experience.

# LICENSE

This code: MIT

[Terms of the Copernicus Data Hub portals and Data supply conditions](https://scihub.copernicus.eu/twiki/do/view/SciHubWebPortal/TermsConditions)
