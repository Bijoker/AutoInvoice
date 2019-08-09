import os, shutil
import time

from tools.log_init import Log

log = Log()


def verifyDownload(downloadDir):
    for i in range(10):
        if len(os.listdir(downloadDir)):
            log.info('检测到下载文件')
            for j in range(3600):
                downloadingFileName, filesuffix = os.path.splitext(os.listdir(downloadDir)[0])
                if filesuffix in ['.crdownload', '.tmp']:
                    log.info('文件下载中....')
                    time.sleep(0.1)
                else:
                    log.info('%s文件下载完成' % os.listdir(downloadDir)[0])
                    return os.listdir(downloadDir)[0]
            return log.warning('文件下载中断')
            # return log.warning('文件下载中断')
        time.sleep(1)
    return log.warning('文件请求下载失败')



if __name__ == '__main__':
    downloadDir = r'D:\Desktop\download'
    a = verifyDownload(downloadDir)
    print(os.path.dirname(os.path.realpath(__file__)))
    print(a)