import os
import sys
import argparse
import datetime
import synapseclient
import synapseutils
import tempfile
import pandas as pd
from synapseclient import File, Folder, Table
from time import sleep

currentYear = datetime.datetime.now().isoformat()[:4]  # YYYY
currentDate = datetime.datetime.now().isoformat()[:10]  # YYYY-MM-DD
currentTime = datetime.datetime.now().isoformat()[:19]

def createAndSendReport(email, token, recipientIds, tableId):
    syn = synapseclient.Synapse()
    syn.login(email=email, authToken=token)

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

    print("Job complete. Uploading data to the specified table in Synapse.")

    url = syn.restGET("/fileHandle/" + str(status['resultsFileHandleId']) + "/url?redirect=false", endpoint=syn.fileHandleEndpoint)
    df = pd.read_csv(url)
    # Add a date column to the csv
    df['Date'] = pd.to_datetime(currentTime)
    # Create a temp file and save the CSV to that file
    fd, path = tempfile.mkstemp()
    df.to_csv(path)
    table = syn.get(tableId)
    syn.store(Table(table, path))

    os.remove(path)  # Delete temp file
    print("Sending notification to the specified recipients.")
    syn.sendMessage(recipientIds, "Synapse Storage Report for " + currentDate, "<a href=\"https://www.synapse.org/#!Synapse:" + 
        tableId + "\">Click here to view the table with the new data</a>.  You can filter by date to see the report for the current period or filter by project to see how its usage has changed over time.", contentType="text/html")
    print("Job complete. Exiting!")
    exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email", required=True, help="Synapse email address")
    parser.add_argument("-k", "--token", required=True, help="Synapse Personal Access Token")
    parser.add_argument("-r", "--recipient", required=True, help="Synapse user ID to receive the report")
    parser.add_argument("-t", "--tableId", required=True, help="The table in Synapse where new rows should be appended")
    args = parser.parse_args()
    createAndSendReport(args.email, args.token, [args.recipient], args.tableId)
