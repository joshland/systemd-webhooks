# README.md

Two part system

 - Deploy waitress-based systemd run framework.
 - Defaults to /opt/webhooks
 - Runs as it's own user
 - Configure the repo-map. {ref}:{familiar name}
 - Use ngrok for troubleshooting.


 SystemD Units
  - <name>.path - Using the {familar name} for the update trigger.
  - <name>.service - OneShot based update service.  Should be configured with a user and the script for running the updates when a particular repo is pushed.


