#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then

    # Install some custom requirements on OS X
    wget https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh -O miniconda.sh;
    bash miniconda.sh -b -p $HOME/miniconda;
    export PATH="$HOME/miniconda/bin:$PATH";
    hash -r;
    conda config --set always_yes yes --set changeps1 no;
    conda update -q conda
    conda info -a;
    conda config --add channels conda-forge


    case "${GDELT}" in
        py27)
            # Install some custom Python 2.7 requirements on OS X
            conda create -n testenv python=2.7 geopandas pandas numpy beautifulsoup4 futures scipy gdal geos fiona shapely pyproj cython gcc jinja2 rtree libspatialindex -c conda-forge
            source activate testenv
            pip install pip -U
            pip install coveralls
            pip install pytest-cov
            pip install python-coveralls
            conda info -a
            ;;
        py34)
            # Install some custom Python 3.4 requirements on OS X
            conda create -n testenv python=3.4 geopandas pandas numpy beautifulsoup4 scipy gdal geos fiona shapely pyproj cython gcc jinja2 rtree libspatialindex -c conda-forge
            source activate testenv
            pip install pip -U
            pip install coveralls
            pip install pytest-cov
            pip install python-coveralls
            conda info -a
            ;;
        py35)
            # Install some custom Python 3.5 requirements on OS X
            conda create -n testenv python=3.5 geopandas pandas numpy beautifulsoup4 scipy gdal geos fiona shapely pyproj cython gcc jinja2 rtree libspatialindex -c conda-forge
            source activate testenv
            pip install pip -U
            pip install coveralls
            pip install pytest-cov
            pip install python-coveralls
            conda info -a
            ;;
        py36)
            # Install some custom Python 3.6 requirements on OS X
            conda create -n testenv python=3.6 geopandas pandas numpy beautifulsoup4 scipy gdal geos fiona shapely pyproj cython gcc jinja2 rtree libspatialindex -c conda-forge
            source activate testenv
            pip install pip -U
            pip install coveralls
            pip install pytest-cov
            pip install python-coveralls
            conda info -a
            ;;
    esac
else
    # Install some custom requirements on Linux

    sudo add-apt-repository ppa:ubuntu-toolchain-r/test -y
    sudo apt-get update -q -y
    sudo add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable -y
    sudo apt-get install python-dev -y
    sudo apt-get install gcc-4.8 -y
    sudo apt-get clean	-y
fi

if [ "$TRAVIS_OS_NAME" == 'linux' ]; then
        pip install -r requirements.txt;
fi;