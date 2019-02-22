import sys
import argparse
import datetime
import synapseclient
import synapseutils
from synapseclient import File, Folder
from time import sleep

currentYear = datetime.datetime.now().isoformat()[:4]  # YYYY
currentDate = datetime.datetime.now().isoformat()[:10] # YYYY-MM-DD

def createAndSendReport(email, apiKey, recipientIds, parentFolder):
    syn = synapseclient.Synapse()
    syn.login(email=email, apiKey=apiKey)

    print("Making call to Synapse to generate a storage report")
    response = syn.restPOST("/storageReport/async/start", body="{\n\t\"reportType\":\"ALL_PROJECTS\"\n}")
    status = syn.restGET("/storageReport/async/get/" + response['token'])

    sleepDuration = 1
    while ('jobState' in status):
        if (status['jobState'] == 'FAILED'):
            sys.exit("Job failed. More info:\n" + status.errorMessage + "\n" + status.errorDetails)
        else:
            print("Job is still processing. Sleeping for " + str(sleepDuration) + " seconds...")
            sleep(sleepDuration)
            sleepDuration = sleepDuration * 2
            status = syn.restGET("/storageReport/async/get/" + response['token'])

    print("Job complete. Creating an entity in Synapse with the report file handle.")

    # Put the report in a folder named the current year, 'YYYY'. Create the folder if it doesn't exist.
    childFolder = syn.findEntityId(currentYear, parent=parentFolder)
    if (childFolder is None):
        childFolder = Folder(currentYear, parent=parentFolder)
        childFolder = syn.store(childFolder)

    reportName = "synapse-storage-stats_" + currentDate + ".csv"
    report = File(path=None, name=reportName, parent=childFolder, dataFileHandleId=status['resultsFileHandleId'])
    report = syn.store(report)

    # Change the "downloadAs" name for convenience. Otherwise it will be Job-<job-id>.csv
    synapseutils.changeFileMetaData(syn, report['id'], downloadAs=reportName, contentType="text/csv")
    
    print("Sending notification to the specified recipients.")
    syn.sendMessage(recipientIds, "Synapse Storage Report for " + currentDate, "<a href=\"https://www.synapse.org/#!Synapse:" + report['id'] + "\">Click here to view the report.</a>", contentType="text/html")
    print("Job complete. Exiting!")
    exit(0)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email", required=True, help="Synapse email address")
    parser.add_argument("-k", "--apiKey", required=True, help="Synapse API key")
    parser.add_argument("-r", "--recipient", required=True, help="Synapse user ID to receive the report")
    parser.add_argument("-p", "--parentFolderId", required=True, help="The folder in Synapse where the report should be stored")
    args = parser.parse_args()
    createAndSendReport(args.email, args.apiKey, [args.recipient], args.parentFolderId)