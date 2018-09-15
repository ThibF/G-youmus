#!/bin/bash
docker build -t=gyoumus .
docker run --rm -v $(pwd):/src/bin gyoumus
