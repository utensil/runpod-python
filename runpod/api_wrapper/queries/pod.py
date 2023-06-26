
def generate_pod_query(pod_id):
    '''
    Generate a query for a specific pod
    '''

    return f"""
    query pod {{
      pod(input: {{podId: "{pod_id}"}}) {{
            id
            imageName
            machineId
            podType
            costPerHr
            desiredStatus
            lastStatusChange
            uptimeSeconds
            runtime {{ uptimeInSeconds }}
            machine {{ podHostId maxDownloadSpeedMbps maxUploadSpeedMbps diskMBps }}
            latestTelemetry {{
                cpuUtilization
                memoryUtilization
                averageGpuMetrics {{
                    percentUtilization
                    memoryUtilization
                }}
            }}
        }}
    }}
    """
