# Synapse Storage Reports Notification Tool

Running this script will make calls to Synapse to

1. Generate a storage report
2. Upload the storage report to Synapse as a file entity
3. Send a notification to a user or team containing a link to the report in Synapse

## Running the script

The script can be run in Python (3.X) by using

`python GenerateAndSendStorageReport.py -e <synapseEmail> -k <synapseApiKey> -r <recipientSynapseId> -p <parentFolder>`

Where

* `<synapseEmail>` is the Synapse user name or registered email address of the account used to run the script.
* `<synapseApiKey>` is the API Key for the account specified by `<synapseEmail>`.
* `<recipientSynapseId>` is the Synapse principal ID of the user or team to which a notification is sent that the report is generated.
* `<parentFolder>` is the Synapse ID of the folder or project within which the report is placed.

Note that the account running the script must must be a member of this team, https://www.synapse.org/#!Team:5, and the notification recipient must have permission to view the contents of the parent folder (otherwise, they will encounter a 403 Unauthorized response when following the link in the notification).
