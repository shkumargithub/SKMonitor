from SKLibPY.FileSystem.FileSystem import SKFileSystem
from SKLibPY.WebLogic.WLS import WLS
time = 10


fs = SKFileSystem()
print("Test Current Usage is :" + str(fs.checkFSUsageLocal("/")))

wls = WLS("http://skmachine:7001", "weblogic", "weblogic#127")
print(wls)
#result = wls.get("http://skmachine:7001/console")
dir(wls.edit.batchConfig)
['canonical', 'dynamicallyCreated', 'id', 'identity', 'name', 'notes','parent',
'schemaName', 'self', 'tags', 'type']
adminServer = wls.edit.adminServerName
running_jobs = []
for server in wls.domainRuntime.serverLifeCycleRuntimes:
    if server.name != adminServer:
        #running_jobs.append(server.start(prefer_async=True))
        print(server.name + " is " + server.state)
    if server.name == adminServer:
        print(server.name + " is " + server.state)

while running_jobs:
    for job in running_jobs:
        print(job)
        if job.completed:
            print(job)
            running_jobs.remove(job)
    time.sleep(10)