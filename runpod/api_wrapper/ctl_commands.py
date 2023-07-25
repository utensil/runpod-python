"""
RunPod | API Wrapper | CTL Commands
"""
# pylint: disable=too-many-arguments,too-many-locals

import os
from contextlib import contextmanager

from typing import Optional
from .queries import gpus, pod, user
from .graphql import run_graphql_query
from .mutations import pods

class APIContext:
    def __init__(self, api_name) -> None:
        self.api_name = api_name
        self.req = None
        self.res = None

    def __repr__(self) -> str:
        return f'API: {self.api_name}\nREQ: {self.req}\nRES: {self.res}\n'

class APIError(ValueError):
    def __init__(self, message, ctx, *args):
        self.message = message
        self.ctx = ctx         
        super(APIError, self).__init__(message, ctx, *args)

@contextmanager
def debug_error(api_name, *_args, **_kwds):
    ctx = APIContext(api_name)
    try:
        yield ctx
    except Exception as ex:
        raise APIError('RunPod API Error', ctx) from ex
    finally:
        if os.environ.get('RUNPOD_DEBUG', '').lower() == 'true':
            print(f'{ctx.api_name} REQ: {ctx.req}')
            print(f'{ctx.api_name} RES: {ctx.res}')

def get_gpus() -> dict:
    '''
    Get all GPU types
    '''
    with debug_error('get_gpus') as ctx:
        ctx.req = gpus.QUERY_GPU_TYPES
        ctx.res = run_graphql_query(ctx.req)
        cleaned_return = ctx.res["data"]["gpuTypes"]
        return cleaned_return


def get_gpu(gpu_id : str):
    '''
    Get a specific GPU type
    
    :param gpu_id: the id of the gpu
    '''
    with debug_error('get_gpu') as ctx:
        ctx.req = gpus.generate_gpu_query(gpu_id)
        ctx.res = run_graphql_query(ctx.req)
        cleaned_return = ctx.res["data"]["gpuTypes"][0]

        return cleaned_return


def create_pod(name : str, image_name : str, gpu_type_id : str, cloud_type : str="ALL",
               data_center_id : Optional[str]=None, country_code:Optional[str]=None,
               gpu_count:int=1, volume_in_gb:int=0, container_disk_in_gb:int=5,
               min_vcpu_count:int=1, min_memory_in_gb:int=1, docker_args:str="",
               ports:Optional[str]=None, volume_mount_path:str="/workspace",
               env:Optional[dict]=None, support_public_ip=None, min_download=None,
               min_upload=None, network_volume_id=None, template_id=None, stop_after=None, terminate_after=None):
    '''
    Create a pod

    :param name: the name of the pod
    :param image_name: the name of the docker image to be used by the pod
    :param gpu_type_id: the gpu type wanted by the pod (retrievable by get_gpus)
    :param cloud_type: if secure cloud, community cloud or all is wanted
    :param data_center_id: the id of the data center
    :param country_code: the code for country to start the pod in
    :param gpu_count: how many gpus should be attached to the pod
    :param volume_in_gb: how big should the pod volume be
    :param ports: the ports to open in the pod, example format - "8888/http,666/tcp"
    :param volume_mount_path: where to mount the volume?
    :param env: the environment variables to inject into the pod, 
                for example {EXAMPLE_VAR:"example_value", EXAMPLE_VAR2:"example_value 2"}, will
                inject EXAMPLE_VAR and EXAMPLE_VAR2 into the pod with the mentioned values

    :example:

    >>> pod_id = runpod.create_pod("test", "runpod/stack", "NVIDIA GeForce RTX 3070")
    '''

    with debug_error('create_pod') as ctx:
        ctx.req = pods.generate_pod_deployment_mutation(
            name, image_name, gpu_type_id, cloud_type, data_center_id, country_code, gpu_count, volume_in_gb,
            container_disk_in_gb, min_vcpu_count, min_memory_in_gb, docker_args,
            ports, volume_mount_path, env, support_public_ip, min_download, min_upload,
            network_volume_id, template_id, stop_after, terminate_after)
        ctx.res = run_graphql_query(ctx.req)
        if "errors" in ctx.res:
            raise ValueError(ctx.res["errors"][0]["message"])
        cleaned_response = ctx.res["data"]["podFindAndDeployOnDemand"]
    return cleaned_response

def create_spot_pod(name, image_name, gpu_type_id, bid_per_gpu, cloud_type="ALL", 
                data_center_id : Optional[str]=None, country_code:Optional[str]=None, gpu_count=1, volume_in_gb=0,
               container_disk_in_gb=5, min_vcpu_count=1, min_memory_in_gb=1, docker_args="",
               ports=None, volume_mount_path="/workspace", env=None, support_public_ip=None, min_download=None,
               min_upload=None, network_volume_id=None, template_id=None, stop_after=None, terminate_after=None):
    '''
    Create a pod
    '''

    with debug_error('create_spot_pod') as ctx:
        ctx.req = pods.generate_spot_pod_deployment_mutation(
            name, image_name, gpu_type_id, bid_per_gpu, cloud_type, data_center_id, country_code, gpu_count, volume_in_gb,
            container_disk_in_gb, min_vcpu_count, min_memory_in_gb, docker_args,
            ports, volume_mount_path, env, support_public_ip, min_download, min_upload,
            network_volume_id, template_id, stop_after, terminate_after)
        ctx.res = run_graphql_query(ctx.req)
        if "errors" in ctx.res:
            raise ValueError(ctx.res["errors"][0]["message"])
        cleaned_response = ctx.res["data"]["podRentInterruptable"]

        return cleaned_response

def stop_pod(pod_id: str):
    '''
    Stop a pod

    :param pod_id: the id of the pod

    :example:

    >>> pod_id = runpod.create_pod("test", "runpod/stack", "NVIDIA GeForce RTX 3070")
    >>> runpod.stop_pod(pod_id)
    '''
    raw_response = run_graphql_query(
        pods.generate_pod_stop_mutation(pod_id)
    )
    cleaned_response = raw_response["data"]["podStop"]
    return cleaned_response


def resume_pod(pod_id: str, gpu_count: int):
    '''
    Resume a pod

    :param pod_id: the id of the pod
    :param gpu_count: the number of GPUs to attach to the pod

    :example:

    >>> pod_id = runpod.create_pod("test", "runpod/stack", "NVIDIA GeForce RTX 3070")
    >>> runpod.stop_pod(pod_id)
    >>> runpod.resume_pod(pod_id)
    '''
    raw_response = run_graphql_query(
        pods.generate_pod_resume_mutation(pod_id, gpu_count)
    )

    cleaned_response = raw_response["data"]["podResume"]
    return cleaned_response


def terminate_pod(pod_id: str):
    '''
    Terminate a pod

    :param pod_id: the id of the pod

    :example:

    >>> pod_id = runpod.create_pod("test", "runpod/stack", "NVIDIA GeForce RTX 3070")
    >>> runpod.terminate_pod(pod_id)
    '''
    run_graphql_query(
        pods.generate_pod_terminate_mutation(pod_id)
    )

def get_pod(pod_id):
    '''
    Get a specific pod
    '''

    with debug_error('get_pod') as ctx:
        ctx.req = pod.generate_pod_query(pod_id)
        ctx.res = run_graphql_query(ctx.req)
        cleaned_return = ctx.res["data"]

        return cleaned_return

def get_myself():
    '''
    Get myself
    '''

    with debug_error('get_myself') as ctx:
        ctx.req = user.generate_myself_query()
        ctx.res = run_graphql_query(ctx.req)
        cleaned_return = ctx.res["data"]

        return cleaned_return
