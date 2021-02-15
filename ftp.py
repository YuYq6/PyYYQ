from ftplib import FTP
import ftplib
import os
import time
from tqdm import tqdm

def getftpfilename(ftpadress, remotedir, pattern):
    """
    get filenames include pattern from ftpserver + remoterdir
    """
    # ftp = FTP('ftp.cdc.noaa.gov')
    ftp = FTP(ftpadress)
    # print(ftp.getwelcome())
    # get direction info
    try:
        ftp.login()
        # ftp.cwd('/Datasets/ncep.reanalysis/pressure')
        ftp.cwd(remotedir)
        files = []
        ftp.dir(files.append)    
        # # print(files)
    except ftplib.all_errors as e:
        print('FTP error:', e)
    # decode filename or dirname
    re_files = []
    for file in files:
        # print(file)
        if file.find(pattern) > 0:
            ss = file.split(' ')
            re_files.append(ss[-1])       
    return re_files


def downfile(ftpadress, remotedir, filenames, localdir):
    ftp = FTP(ftpadress)
    # print(ftp.getwelcome())
    # get direction info

    try:
        ftp.login()
        # ftp.cwd(remotedir)
        for file in filenames:
            remotefile = remotedir + '/' + file
            localfile = localdir +"/" + file
            size = ftp.size(remotefile)
            print('Begin downloading', localfile, size, time.ctime())
            pbar = tqdm(total=size)
            fp = open(localfile, 'wb')
            size_down = 0
            
            def file_write(data):
                fp.write(data)
                pbar.update(len(data))
            
            res = ftp.retrbinary('RETR %s' % remotefile, file_write)  
            pbar.close()              
            fp.close()

            if not res.startswith('226 Transfer complete'):
                print('Download failed')
                if os.path.isfile(localfile):
                    os.remove(localfile)
                else:
                    print("%s downloaded" % localfile)
    except ftplib.all_errors as e:
        print('FTP error:', e)


def down_ncep_reanalysis(year):
    ftpserver = 'ftp.cdc.noaa.gov'
    includeword = '.' + str(year) + '.nc'

    remotedir = '/Datasets/ncep.reanalysis2/' #pressure, surface, gaussian_grid
    sub_dir = ['gaussian_grid', 'pressure', 'surface']
    loacaldir = '/mnt/f/noaa/reanalysis2/' + str(year)
    for dir in sub_dir:
        files = getftpfilename(ftpserver, remotedir + dir, includeword)
        downfile(ftpserver, remotedir + dir, files, loacaldir)
        
    remotedir = '/Datasets/ncep.reanalysis/'
    sub_dir = ['surface_gauss','pressure', 'surface']
    loacaldir = '/mnt/f/noaa/reanalysis/' + str(year)
    for dir in sub_dir:
        files = getftpfilename(ftpserver, remotedir + dir, includeword)
        downfile(ftpserver, remotedir + dir, files, loacaldir)
    