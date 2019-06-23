import subprocess


class SKFileSystem:
    '''Support File System Management.'''

    def checkFSUsageLocal(self, partition):
        df = subprocess.Popen(["df", "-k"], stdout=subprocess.PIPE)
        for line in df.stdout:
            splitline = line.decode().split()
            if splitline[5] == partition:
                return int(splitline[4][:-1])


fs = SKFileSystem()
print("Test From Lib Current Usage is :" + str(fs.checkFSUsageLocal("/")))
