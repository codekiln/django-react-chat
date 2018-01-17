#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace


celery -A django_react_chat_example_project.taskapp worker -l INFO
