#!/usr/bin/python2.7
#-*- coding:utf-8 -*-
import paramiko 
import datetime
import codecs

def ssh_connect(_host,_username,_password):
    try:
        _ssh_fd=paramiko.SSHClient()
        _ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _ssh_fd.connect(_host,username=_username,password=_password)
    except Exception,e:
        print('ssh %s@%s:%s'%(_username,_host,e.message))
        exit()
    return _ssh_fd

def sftp_open(_ssh_fd):
    return _ssh_fd.open_sftp()

def sftp_put(_sftp_fd,_put_from_path,_put_to_path):
    return _sftp_fd.put(_put_from_path,_put_to_path)

def sftp_get(_sftp_fd,_get_from_path,_get_to_path):
    return _sftp_fd.get(_get_from_path,_get_to_path)

def ssh_exec_command(_ssh, command):
    return _ssh.exec_command(command)

def sftp_close(_sftp_fd):
    _sftp_fd.close()

def ssh_close(_ssh_fd):
    _ssh_fd.close()

if __name__=='__main__':
    try:
        ''' foreach host list  '''
        with codecs.open('/var/www/python/host.txt', 'r', 'utf8') as f:
            now_time = datetime.datetime.now() + datetime.timedelta()
            for line in f.readlines():
                if not line.strip():continue
                list_raw = line.split()
                host = list_raw[0]
                dbname = list_raw[1]
                username = list_raw[2]
                userpassword = list_raw[3]
                mysqlusername = list_raw[4]
                mysqlpassword = list_raw[5]
 
                sshd = ssh_connect(host, username, userpassword)
                sftpd = sftp_open(sshd)
                remote_path = local_path = '/tmp/' + dbname + '_' + now_time.strftime('%Y%m%d') + '.sql.zip'
                command1 = "mysqldump -h127.0.0.1" + " -u" + mysqlusername + " -p" + mysqlpassword +  " --lock-all-tables " + dbname + " | /bin/gzip > " + remote_path
                print(command1)
                
                ssh_exec_command(sshd, command1)
                sftp_get(sftpd, remote_path, local_path) 
                
                sftp_close(sftpd)
                ssh_close(sshd)
        ''' foreach host list end '''
    except Exception,e:
        print 'ERROR:sftp_get-%s'%e