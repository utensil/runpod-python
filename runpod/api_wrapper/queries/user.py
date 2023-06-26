def generate_myself_query():
    '''
    Generate a query for myself
    '''

    return f"""
    query myself {{
      myself {{
        pods {{
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
        currentSpendPerHr
        spendLimit
        templateEarned
        spendDetails {{
          localStoragePerHour
          networkStoragePerHour
          gpuComputePerHour
        }}
        networkVolumes {{
          id
          name
          size
          dataCenterId
        }}
      }}
    }}
    """
