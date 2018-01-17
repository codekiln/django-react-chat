#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


celery -A django_react_chat_example_project.taskapp beat -l INFO
