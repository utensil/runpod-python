
def generate_pod_query(pod_id):
    '''
    Generate a query for a specific pod
    '''

    return f"""
    query pod {{
      pod(input: {{podId: "{pod_id}"}}) {{
            id
            podType
            costPerHr
            desiredStatus
            lastStatusChange
            uptimeSeconds
            runtime {{ uptimeInSeconds }}
            machine {{ maxDownloadSpeedMbps maxUploadSpeedMbps }}
        }}
    }}
    """
