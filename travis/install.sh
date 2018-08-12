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
            conda create -n testenv python=3.4  geopandas libxml2 beautifulsoup4 -c ioos
            source activate testenv
            pip install pip -U
            pip install pandas==0.20.3
            pip install coveralls
            pip install pytest-cov
            pip install python-coveralls
            conda info -a
            ;;
        py35)
            # Install some custom Python 3.5 requirements on OS X
            conda create -n testenv python=3.5 pandas numpy beautifulsoup4 scipy gdal geos fiona shapely pyproj cython gcc jinja2 rtree libspatialindex -c conda-forge
            source activate testenv
            conda update --all -c conda-forge
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
    sudo apt-get update -q -y
    if [[ "$TRAVIS_PYTHON_VERSION" == "2.7" ]]; then
      wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda.sh;
    else
      wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
    fi
    bash miniconda.sh -b -p $HOME/miniconda;
    export PATH="$HOME/miniconda/bin:$PATH";
    hash -r;
    conda config --set always_yes yes --set changeps1 no;
    conda update -q conda
    conda info -a;
    conda config --add channels conda-forge
    conda create -n testenv python=$TRAVIS_PYTHON_VERSION pandas numpy beautifulsoup4 scipy gcc -c conda-forge
    source activate testenv
    if [[ "$TRAVIS_PYTHON_VERSION" == "3.4" ]]; then
      conda install geopandas beautifulsoup4 libxml2 -c ioos
      pip install pandas==0.20.3
    else
      conda update --all -c conda-forge
      conda install fiona shapely pyproj cython
      pip install geopandas
    fi
    conda install geopandas

fi

if [ "$TRAVIS_OS_NAME" == 'linux' ]; then
        pip install -r requirements.txt;
fi;
