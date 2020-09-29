from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from ..db import models, schemas
from ..utils import *

from datetime import datetime
import docker


def get_running_apps():
    apps_list = []
    dclient = docker.from_env()
    apps = dclient.containers.list()
    for app in apps:
        attrs = app.attrs
        attrs.update(conv2dict('name', app.name))
        attrs.update(conv2dict('ports', app.ports))
        attrs.update(conv2dict('short_id', app.short_id))
        apps_list.append(attrs)

    return apps_list

def get_apps():
    apps_list = []
    dclient = docker.from_env()
    apps = dclient.containers.list(all=True)
    for app in apps:
        attrs = app.attrs
        attrs.update(conv2dict('name', app.name))
        attrs.update(conv2dict('ports', app.ports))
        attrs.update(conv2dict('short_id', app.short_id))
        apps_list.append(attrs)

    return apps_list


def get_app(app_name):
    dclient = docker.from_env()
    app = dclient.containers.get(app_name)
    attrs = app.attrs

    attrs.update(conv2dict('ports', app.ports))
    attrs.update(conv2dict('short_id', app.short_id))
    attrs.update(conv2dict('name', app.name))

    return attrs


def get_app_processes(app_name):
    dclient = docker.from_env()
    app = dclient.containers.get(app_name)
    if app.status == 'running':
        processes = app.top()
        return schemas.Processes(Processes=processes['Processes'], Titles=processes['Titles'])
    else:
        return None


def get_app_logs(app_name):
    dclient = docker.from_env()
    app = dclient.containers.get(app_name)
    if app.status == 'running':
        return schemas.AppLogs(logs=app.logs())
    else:
        return None


def deploy_app(template: schemas.DeployForm):
    try:
        launch = launch_app(
            template.name,
            conv_image2data(template.image),
            conv_restart2data(template.restart_policy),
            conv_ports2data(template.ports),
            conv_portlabels2data(template.ports),
            conv_volumes2data(template.volumes),
            conv_env2data(template.env),
            conv_devices2data(template.devices),
            conv_labels2data(template.labels),
            conv_sysctls2data(template.sysctls),
            conv_caps2data(template.cap_add)
        )

    except Exception as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.explanation)
    print('done deploying')

    return schemas.DeployLogs(logs=launch.logs())

def Merge(dict1, dict2): 
    if dict1 and dict2:
        return(dict2.update(dict1))
    elif dict1:
        return dict1
    elif dict2:
        return dict2
    else:
        return None

def launch_app(name, image, restart_policy, ports, portlabels, volumes, env, devices, labels, sysctls, caps):
    dclient = docker.from_env()
    combined_labels = Merge(portlabels, labels)
    try:
        lauch = dclient.containers.run(
            name=name,
            image=image,
            restart_policy=restart_policy,
            ports=ports,
            volumes=volumes,
            environment=env,
            sysctls=sysctls,
            labels=combined_labels,
            devices=devices,
            cap_add=caps,
            detach=True
        )
    except Exception as e:
        if e.status_code == 500:
            failed_app = dclient.containers.get(name)
            failed_app.remove()
        raise e

    print(f'''Container started successfully.
       Name: {name},
      Image: {image},
      Ports: {ports},
    Volumes: {volumes},
        Env: {env}''')
    return lauch


def app_action(app_name, action):
    err = None
    dclient = docker.from_env()
    app = dclient.containers.get(app_name)
    _action = getattr(app, action)
    if action == 'remove':
        try:
            _action(force=True)
        except Exception as exc:
            err = f"{exc}"
    else:
        try:
            _action()
        except Exception as exc:
            err = exc.explination
    apps_list = get_apps()
    return apps_list

def prune_images():
    dclient = docker.from_env()
    deleted_everything = {}
    deleted_volumes = dclient.volumes.prune()
    deleted_images = dclient.images.prune()
    deleted_networks = dclient.networks.prune()

<<<<<<< HEAD
    deleted_everything.update(deleted_volumes)
    deleted_everything.update(deleted_images)
    deleted_everything.update(deleted_networks)
    return deleted_everything
=======
    deleted_everything.update(deleted_networks)
    deleted_everything.update(deleted_volumes)
    deleted_everything.update(deleted_images)
    
    return deleted_everything
def prune_resources(resource):
    dclient = docker.from_env()
    action = getattr(dclient, resource)
    deleted_resource = action.prune()
    return deleted_resource
>>>>>>> ff5cde45e70a3c82a1e2f714da6e769b5bee580a
