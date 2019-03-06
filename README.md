# Synapse Storage Reports Notification Tool

Running this script will make calls to Synapse to

1. Generate a storage report
2. Upload the storage report to Synapse as new rows in a table
3. Send a notification to a user or team containing a link to the report in Synapse

## Running the script

The script can be run in Python (3.X) by using

`python GenerateAndSendStorageReport.py -e <synapseEmail> -k <synapseApiKey> -r <recipientSynapseId> -t <tableId>`

Where

* `<synapseEmail>` is the Synapse user name or registered email address of the account used to run the script.
* `<synapseApiKey>` is the API Key for the account specified by `<synapseEmail>`.
* `<recipientSynapseId>` is the Synapse principal ID of the user or team to which a notification is sent that the report is generated.
* `<tableId>` is the Synapse ID of the table where rows should be appended.

The table should already exist and have a schema. The schema of the table should match exactly as follows (in order):

|Column Name|Column Type|Size|
|---|---|---|
|projectId|Entity|NA|
|projectName|String|256|
|sizeInBytes|Integer|NA|
|Date|Date|NA|

Note that the account running the script must must be a member of this team, https://www.synapse.org/#!Team:5, and the notification recipient must have permission to view the contents of the parent folder (otherwise, they will encounter a 403 Unauthorized response when following the link in the notification).
