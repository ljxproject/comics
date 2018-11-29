import os
import re
import subprocess

from django.conf import settings

db = settings.DATABASES
bf = settings.BACKUP_FILE


class BackupHandler(object):

    def __init__(self):
        self.user = db['default']["USER"]
        self.password = db['default']["PASSWORD"]
        self.backup_file = bf

    def backup(self, backup_type, basedir=None):
        if backup_type == 0:
            order = 'innobackupex --user=%s --password=%s %s' % (  # mac
                # order = 'sudo innobackupex --user=%s --password=%s %s' % (
                self.user, self.password, self.backup_file)
        elif backup_type == 1 or backup_type == 2:
            order = 'innobackupex --user=%s --password=%s --incremental --incremental-basedir=%s %s' % (  # mac
                # order = 'sudo innobackupex --user=%s --password=%s --incremental --incremental-basedir=%s %s' % (
                self.user, self.password, basedir, self.backup_file)
        else:
            return Exception("备份类型不合法")
        try:
            res = subprocess.Popen(order, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                                   encoding='utf-8').stderr.readlines()
            n = len(res)
            err = False
            for index, value in enumerate(res):
                if re.findall("completed OK!", res[-1]):
                    break
                elif re.findall("completed OK!", value) and index < n:
                    strs = ''
                    for line in res[index + 1::]:
                        strs += line
                        err = True
                    break
            if err:
                return Exception(strs)
            else:
                file_re = os.popen("cd %s && ls -lht " % self.backup_file).readlines()[1]  # todo
                file_name = re.findall('\d+-\d+-.+-\d+-\d+', file_re)[0]
                backup_file = '%s%s' % (self.backup_file, file_name)
                os.system("innobackupex --apply-log --export %s" % backup_file)  # mac
                # os.system("sudo innobackupex --apply-log --export %s" % backup_file)
                file_size = os.popen("du -sh %s |cut -d '/' -f 1" % backup_file).readlines()[0]  # mac
                # file_size = os.popen("sudo du -sh %s |cut -d '/' -f 1" % backup_file).readlines()[0]
                return (file_size, file_name, backup_file)
        except Exception as e:
            return e


backup = BackupHandler()
