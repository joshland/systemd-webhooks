from flask import Flask,request,json
from . import config

from loguru import logger
import yaml

import os
import hmac
import hashlib
import base64
import logging
from pathlib import Path

# create a custom handler
class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


def commit_stats(commit: list):
    """ take a commit list, return stats"""
    added = 0
    modified = 0
    removed = 0

    for c in commit:
        added    += len(c.get('added', []))
        removed  += len(c.get('removed', []))
        modified += len(c.get('modified', []))
        continue

    return added, modified, removed

def verify_payload(key: str, signature: str, payload: str):
    ''' key is the shared secret
        signature is the contents of the X-Hub-Signature-256 field
        Payload is the raw json reply
    '''
    if key.strip() == '':
        logger.error(f'Empty Key Passed to Payload Verification.')
        pass

    hmac_id, hmac_sig = signature.split('=')

    digest = hmac.new(key.encode(), payload, hashlib.sha256).hexdigest()

    if digest != hmac_sig:
        logger.warning(f'{hmac_sig}: GitHub.')
        logger.warning(f'{digest}: Calculated.')
        logger.error(f'INVALID MESSAGE! {hmac_sig} {digest}')
        pass

    return digest == hmac_sig

def make_notice(repo_xref, notice_path, repo, branch):
    """ uses the RepoMap from the config.yaml to lookup file names, touches the file.
    Properly configure SystemD Path files will be watching for the filename, which will trigger the pipeline actions.
    make a notice in notice_path for repo"""
    logger.debug(f'{notice_path} {repo} {branch}')

    target = repo_xref.get(repo,{}).get(branch,'')
    if not target:
        logger.error(f'No match could be found for repo {repo} and branch {branch}.  Please check RepoMap.')
        return False

    fname = os.path.join(notice_path, target)
    
    Path(fname).touch(mode=0o644, exist_ok=True)
    return True


# application factory pattern 
def create_app(config_name='development'):
    """ flask app factory for answering github notices """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config.config[config_name])               # Load static app config, configure loguru.
    yamldata = yaml.safe_load(open(app.config['CONFIG_FILE'], 'r')) # update from yaml config
    app.config.update(yamldata)

    logger.start(app.config['LOGFILE'], level=app.config['LOG_LEVEL'], format="{time} {level} {message}", backtrace=app.config['LOG_BACKTRACE'], rotation='25 MB')
    app.logger.addHandler(InterceptHandler()) # Add's loguru

    @app.route('/githubPush',methods=['POST'])
    def githubPush():
        ''' flask route request, main handler.  This is built purely for push and ping, but you can extend it is needed.'''

        data = request.json
        eventType = request.headers.get('X-Github-Event')  # push/ping/issue, etc
        signature = request.headers.get('X-Hub-Signature-256')

        if not verify_payload(app.config.get('SECRET_KEY',''),signature, request.data):  # if this doesn't match, verify your SECRET_KEY
            return "Record not found", 400

        if eventType == 'push': # Primary Event trigger.
            repo = data["repository"]["full_name"]
            branch = data['ref']
            added, modified, removed = commit_stats(data['commits'])
            logger.info(f'Push Event {branch} [{repo}][a:{added}/m:{modified}/d:{removed}]')
            make_notice(app.config['RepoMap'],app.config['NOTICE_PATH'], repo, branch)
        elif eventType == 'ping':
            repo = data["repository"]["full_name"]
            logger.info(f"Ping {data['repository']['id']}[{repo}]")
        elif eventType == 'issue':
            logger.info(f'Issue {data["issue"]["title"]} {data["action"]}')
            logger.info(f'{data["issue"]["body"]}')
            logger.info(f'{data["issue"]["url"]}')
            logger.warn(f'No handler for this event type.')
        else:
            logger.warn(f'No handler for this event type: {eventType}')
            pass
        
        return data


    return app
