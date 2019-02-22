# Synapse Storage Reports Notification Tool

Running this script will make calls to Synapse to

1. Generate a storage report
2. Associate the storage report file handle with a file entity
3. Send a notification to a user or team containing a link to the report in Synapse

## Running the script

The script can be run in Python (3.X) by using

`python GenerateAndSendStorageReport.py -e <synapseEmail> -k <synapseApiKey> -r <recipientSynapseId> -p <parentFolder>`

Note that the user running the script must have authorization to generate storage reports in Synapse, and the notification recipient must have permission to view the contents of the parent folder (otherwise, they will hit a 403 when following the link in the notification).
