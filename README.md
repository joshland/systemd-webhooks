# README.md

I needed to run a pipeline operation in an odd location, and I decided to use very basic methods for reacting to Github pushes.  You will probably be better served by a real CI pattern, but this fits my needs.

Two Major Components:
- webhook listener, configured to react to events by repo and branch, touching a file.
- systemd Path Unit monitors the for the files activity, running a systemd service when the file is touched.

It is expected that you will place the listener behind a proxy server of some kind.

Quick deployment overview:

 - Deploy waitress-based systemd run framework.
 - Defaults to /opt/webhooks
 - Runs as it's own user
 - Configure the repo-map. {ref}:{familiar name}
 - Use ngrok for troubleshooting.


 SystemD Units
  - <name>.path - Using the {familar name} for the update trigger.
  - <name>.service - OneShot based update service.  Should be configured with a user and the script for running the updates when a particular repo is pushed.
