#base routines for WIKIDpy

from os import path,listdir
from glob import glob
from socket import getfqdn
import configparser

conf=configparser.RawConfigParser(inline_comment_prefixes=('#',))

def readConfig(Name=None):
    """updates global configuration by reading from given configparser file"""
    conf.read(Name) #note this is WIKIDpy._conf
    #expand usernames (~ or ~user) 
    expUser()

def chkLocation():
    """test if computers domain name matches _conf setting"""
    dn='.'.join(getfqdn().split('.')[1:]) #get domain name
    cdn=(conf['general']['dn']).split(',')
    if  not dn in cdn :
        print('WARNING, it looks like you are not running this on a different network, default settings from WIKIDpy/defaults.conf may be wrong')
        print('Expected network=',cdn)
        print('Check default.conf or load your own custom version using readConf()')
        return -1
    return 0

def expUser():
    """Go through all configuration file entries and expand all ~ to user name
    will not expand non-existant users"""
    for ss in conf.sections() :
        for iii in conf.items(ss) :
            ii=iii[0]
            #print(ss,ii)
            if '~' in conf[ss][ii] : 
                if ii == 'user' :
                    conf[ss][ii]=path.basename(path.expanduser(conf[ss][ii]))
                else :
                    if conf[ss][ii][0] == '~' : #path relative to home area
                        conf[ss][ii]=path.expanduser(conf[ss][ii])
                    else :
                        parts=conf[ss][ii].split('/')
                        for n in range(len(parts)) : parts[n]=path.basename(path.expanduser(parts[n]))
                        conf[ss][ii]='/'.join(parts)
            #print(conf[ss][ii])
                    
def setProject(proj,projpath='',force=False):
    """Set the current project, will only choose existing projects with M2/WIKID data unless force is set to True, if path is not set to None will only search this pathname"""
    if proj[-1]=='/' : proj=proj[:-1]
    if proj=='current' :  #set to the most current project
        pass
    elif path.dirname(proj) != '' : # see if an absolute path has been given
        fullproj=proj
    elif projpath != '' :
        fullproj=projpath+'/'+proj
    else : #search everywhere for it
        p=glob(conf['data locations']['gbtdata']+'/'+proj)
        if len(p) == 0 :
            p=glob(conf['data locations']['archive']+'/'+proj)
            if len(p) == 0 :
                p=glob(conf['data locations']['tests']+'/'+proj)
        if len(p) == 0:
            print('WARNING Project ',proj,' Not found no action taken')
            return -1
        if len(p) > 1 :
            print('More than one project matching ',proj,' found no action taken')
            print(p)
        else : fullproj=p[0]
    proj_files=listdir(fullproj) 
    if conf['data locations']['M2dir'] in proj_files : 
        conf['general']['instrument']='M2'
    elif conf['data locations']['WIKIDdir'] in proj_files : 
        conf['general']['instrument']='WIKID'
    else :
        print('WARNING No Vaid WIKID or MUSTANG2 data directory found in project',projpath)
        if force == False :
            print('No action taken')
            return -1
    conf['general']['proj']=projpath+'/'
    return 0





 
