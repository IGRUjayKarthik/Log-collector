import paramiko
from paramiko import SSHException
import re
import time
import zipfile
import threading
import re
import sys,os
from threading import Thread
def get_files(ip,filepath,log_foldername):
    outlock=threading.Lock()
    try:
        print("IP started "+ ip)
        command_list=filepath
        ccm_ip=ip
        ccm_username = <Call manager Server User Name>
        ccm_pass = <Call manager Server Password>
        sshtoCCM = paramiko.SSHClient()
        sshtoCCM.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshtoCCM.connect(ccm_ip, username=ccm_username, password=ccm_pass, banner_timeout=60)
        chan = sshtoCCM.invoke_shell()
        print("Command shell started "+ ip)
        for cmd in command_list:
            time.sleep(3)
            out = ''
            flag = True
            proceed = None
            sftp_ip = None
            sftp_port = None
            userid = None
            passwd = None
            directry = None
            chan.send(cmd)
            out = ''
            while flag == True:
                temp = chan.recv(9999)
                out = out + str(temp)
                print(temp.decode('utf-8'))
                proceed = re.search('Would you like to proceed', out)
                sftp_ip = re.search('SFTP server IP: ', out)
                sftp_port = re.search('SFTP server port', out)
                userid = re.search('User ID: ', out)
                passwd = re.search('Password:', out)
                directory = re.search('Download directory: ', out)
                exitCheck = re.search('Transfer completed.', out)

                if proceed:
                    print('Starting sftp')
                    chan.send("y\n")
                    proceed = False
                    out = ''

                if sftp_ip:
                    print('SFTP IP entered')
                    chan.send('<SFTP server IP>\n')
                    sftp_ip = False
                    out = ''

                if sftp_port:
                    print('SFTP Port passed')
                    chan.send('\n')
                    sftp_port = False
                    out = ''

                if userid:
                    print('Userid is entered')
                    chan.send('<SFTP userid>\n')
                    userid = False
                    out = ''

                if passwd:
                    print('Password is entered')
                    chan.send('<SFTP server password>\n')
                    passwd = False
                    out = ''

                if exitCheck:
                    print('File transfer success'+ip)
                    #chan.send('exit\n')
                    chan.send("\n")
                    exitCheck = False
                    out = ''
                    flag = False
                    sshtoCCM.close()

                if directory:
                    print('Directory in SFTP server is mentioned')
                    print(log_foldername)
                    #chan.send("/home/magicuser\n")
                    chan.send("/home/magicuser/"+log_foldername+"\n")
                    chan.send("yes\n")
                    directory = False
                    time.sleep(10)
                    out = ''

    except Exception as e:
        print(str(e))

def main_thread():
    ip = [<list of server IP from which logs are to be collected>]
    threads=[]
    filepath = [<list of server log files to be collected>]
    try:
        sftp_ip = <SFTP server IP>
        sftp_username = <SFTP server Username>
        sftp_pass = <SFTP server Password>
        sshtosftp = paramiko.SSHClient()
        sshtosftp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshtosftp.connect(sftp_ip, username=sftp_username, password=sftp_pass, banner_timeout=60)
        chan_sftp = sshtosftp.invoke_shell()
        print("Sftp logged in")
        time.sleep(5)
        userid = "uig"    # User ID is used for creating a directory in the SFTP
        problem_type = "XYZ"
        ti = time.strftime("%d%b%Y-%H%M%S")
        log_foldername = userid + problem_type + ti
        chan_sftp.send("mkdir " + log_foldername + "\n")
        print("Folder created " + log_foldername)

        for i in ip:
            t=threading.Thread(target=get_files,args=(i,filepath,log_foldername))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        print("Thread execution completed")
             

    except Exception as e:
        print(str(e))

main_thread()
print("ThinkPad-Ujay")
print("Everything is success")