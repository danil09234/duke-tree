docker build -t unittests -f Dockerfile.unittests .
docker run unittests "$@"