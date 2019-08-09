import subprocess
def checkprocess(processnames):

    for processname in processnames:
        p = subprocess.Popen('taskkill /F /IM %s' %processname,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        p.wait()
if __name__ == '__main__':
    checkprocess(['chromedriver.exe'])