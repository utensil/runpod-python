"""
RunPod | API Wrapper | Mutations | Pods
"""
# pylint: disable=too-many-arguments, too-many-locals, too-many-branches


def generate_pod_deployment_mutation(
        name, image_name, gpu_type_id, cloud_type=None, data_center_id=None, country_code=None,
        gpu_count=None, volume_in_gb=None, container_disk_in_gb=None, min_vcpu_count=None,
        min_memory_in_gb=None, docker_args=None, ports=None, volume_mount_path=None,
        env=None, support_public_ip=None, min_download=None, min_upload=None,
        network_volume_id=None, template_id=None, stop_after=None, terminate_after=None):
    '''
    Generates a mutation to deploy a pod on demand.
    '''
    input_fields = []

    if cloud_type is not None:
        input_fields.append(f"cloudType: {cloud_type}")
    if data_center_id is not None:
        input_fields.append(f'dataCenterId: "{data_center_id}"')
    if country_code is not None:
        input_fields.append(f'countryCode: "{country_code}"')
    if gpu_count is not None:
        input_fields.append(f"gpuCount: {gpu_count}")
    if volume_in_gb is not None:
        input_fields.append(f"volumeInGb: {volume_in_gb}")
    if container_disk_in_gb is not None:
        input_fields.append(f"containerDiskInGb: {container_disk_in_gb}")
    if min_vcpu_count is not None:
        input_fields.append(f"minVcpuCount: {min_vcpu_count}")
    if min_memory_in_gb is not None:
        input_fields.append(f"minMemoryInGb: {min_memory_in_gb}")
    if gpu_type_id is not None:
        input_fields.append(f'gpuTypeId: "{gpu_type_id}"')
    if name is not None:
        input_fields.append(f'name: "{name}"')
    if image_name is not None:
        input_fields.append(f'imageName: "{image_name}"')
    if docker_args is not None:
        input_fields.append(f'dockerArgs: "{docker_args}"')
    if ports is not None:
        input_fields.append(f'ports: "{ports}"')
    if volume_mount_path is not None:
        input_fields.append(f'volumeMountPath: "{volume_mount_path}"')
    if env is not None:
        env_string = ", ".join(
            [f'{{ key: "{key}", value: "{value}" }}' for key, value in env.items()])
        input_fields.append(f"env: [{env_string}]")
    if support_public_ip is not None:
        input_fields.append(f"supportPublicIp: {support_public_ip}")

    if min_download is not None:
        input_fields.append(f"minDownload: {min_download}")
    if min_upload is not None:
        input_fields.append(f"minUpload: {min_upload}")
    if network_volume_id is not None:
        input_fields.append(f"networkVolumeId: {network_volume_id}")
    if template_id is not None:
        input_fields.append(f"templateId: {template_id}")
    if stop_after is not None:
        input_fields.append(f"stopAfter: {stop_after}")
    if terminate_after is not None:
        input_fields.append(f"terminateAfter: {terminate_after}")

    input_string = ", \n".join(input_fields)

    return f"""
    mutation {{
      podFindAndDeployOnDemand(
        input: {{
          {input_string}
        }}
      ) {{
        id
        imageName
        env
        machineId
        machine {{
          podHostId
        }}
      }}
    }}
    """


def generate_pod_stop_mutation(pod_id: str) -> str:
    '''
    Generates a mutation to stop a pod.
    '''
    return f"""
    mutation {{
        podStop(input: {{ podId: "{pod_id}" }}) {{
            id
            desiredStatus
        }}
    }}
    """


def generate_pod_resume_mutation(pod_id: str, gpu_count: int) -> str:
    '''
    Generates a mutation to resume a pod.
    '''
    return f"""
    mutation {{
        podResume(input: {{ podId: "{pod_id}", gpuCount: {gpu_count} }}) {{
            id
            desiredStatus
            imageName
            env
            machineId
            machine {{
                podHostId
            }}
        }}
    }}
    """


def generate_pod_terminate_mutation(pod_id: str) -> str:
    '''
    Generates a mutation to terminate a pod.
    '''
    return f"""
    mutation {{
        podTerminate(input: {{ podId: "{pod_id}" }})
    }}
    """
