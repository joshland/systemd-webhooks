#!/bin/bash

# Update the blog
git pull -r

build-cmd.sh

deploy.sh

