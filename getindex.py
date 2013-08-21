# Command to display status of indexes:
# - Index name
# - Retention time in days
# - Current size in MB
# - Is the index internal or not?
# - Local path of the index
# - Archive directory (if set)
# - First and last event time
#
# You need to install Splunk Python SDK into 
#   $SPLUNK_HOME/lib/python2.7/site-packages/splunklib

# (C) Bojan Zdrnja, INFIGO IS d.o.o. (http://www.infigo.hr/en)
# <bojan.zdrnja@infigo.hr>

import splunklib.client as client
import splunk.auth as auth
import splunk.Intersplunk as si
import splunklib.binding as binding
import sys
import logging
import splunk.entity as entity

settings = dict()
records = si.readResults(settings = settings, has_header = True)

logging.debug(settings)

sKey = settings['sessionKey']

service = client.Service(token=sKey)

results = []

for i in service.indexes:
    retention = (int)(i.frozenTimePeriodInSecs)/(60*60*24)
    if i.coldToFrozenDir is None:
        ArchiveDir = "Not Defined"
    currentSize = i.currentDBSizeMB
    indexPath = i.homePath_expanded
    if i.isInternal == '1':
        Internal = "Yes"
    else:
        Internal = "No"
    if i.minTime is None: 
	firstEvent = "None"
    else:
        firstEvent = i.minTime
    if i.maxTime is None:
	lastEvent = "None"
    else:
	lastEvent = i.maxTime

    results.append({'Index' : i.name, 'RetentionTime (Days)' : retention, 'CurrentSizeMB' : currentSize, 'IndexPath' : indexPath, 'ArchiveDirectory' : ArchiveDir, 'IsInternal' : Internal, 'FirstEvent' : firstEvent, 'LatestEvent' : lastEvent})

si.outputResults(results)
