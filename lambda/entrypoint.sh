#!/bin/bash

set -o errexit
set -o nounset

source /ve/bin/activate

exec "$@"
