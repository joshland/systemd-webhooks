# README.md - Blog Updates

### Overview

In our theoretical case, we have a shared blog server where we're going to run some pipeline commands when we get a push event from Github.  

We have a local user: "webhooks" that receives the push events.  We have a local user per-user with their blog packages in their home directories:

### Users

Each users home directory is /blog/[username]

fred
cara
doug
chuck
user1


## Setup 

### Waitressd
First, deploy the application in /srv/webhooks/waitressd.

use the provided 'dev.yaml' in that folder.

### NGINX

Next, complete your linkage to reach the running instance.  In my case, I added a file to the nginx config:
  blogs.conf - conf.d file
  github.conf - conf file which blogs.conf will include.
  ssl.conf - common ssl config, shared by site definitions. (Example uses ACME certs)

### SystemD

I setup the .path and .service files with the correct working directory, and a simple Pipeline invocation script. 

It runs the pipeline as the individual user.

### Pipeline

I stored the pipeline in /srv/pipelines, which all call, but it expects the user and working directory to be set.


### GitHub

for each Repo, go to Settings -> WebHooks.

 - New Webhooks:
   - URL, in the default code, pushes should be sent to /githubPush, aka https://blogs.company.com/githubPush
   - Content Type: application/json
   - Set the secret-key, use the same value for both Github and in your config Yaml file.


### Testing

Setup ngrok for effective testing.  It provides the most seamless way to ensure that each piece is fully functional, allows replay, and lets you work with properly signed messages.