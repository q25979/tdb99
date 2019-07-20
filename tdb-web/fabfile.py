# -*- coding: utf-8 -*-
from fabric.api import run, env, cd, prefix, sudo

def deploy_online(branch="master"):
    env.host_string = 'root@38.27.99.219'
    env.password = 'tymmgg1+'
    with cd('/root/lebo-web'):
        # update
        run('git reset --hard HEAD')
        run('git checkout %s' % branch)
        run('git pull')

        # build
        run('npm i')
        run('rm -rf dist')
        run('npm run production_build')

        run('cd dist/final && npm install --only=production')
        run('pm2 restart lebo-qrcode')
        # run('cd dist/final && pm2 start pm2.config.json --env production')