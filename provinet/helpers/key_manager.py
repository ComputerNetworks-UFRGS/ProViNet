import subprocess, os.path
from provinet.settings import STATICFILES_DIRS

KEY_DIR = STATICFILES_DIRS[0] + '/keys/'

def createKey(key_file_name):
    """
    Creates a key pair with no password. Then, the user need to download the privatekey to access the VM created
    """
    print "Creating key..."
    process = subprocess.Popen('ssh-keygen -t rsa -C ' + key_file_name + ' -f ' + KEY_DIR + key_file_name + '.rsa',
                                executable="/bin/bash", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    process.communicate('')
    return True
    
def deployKey(dst_user, dst_ip, key_file_name):
    """
    If createKey() succeed, the filename.rsa.pub exists and it will be copied to the remote VM 
    """
    print "Copying key to remote VM..."
    if os.path.exists(STATICFILES_DIRS[0] + '/keys/' + key_file_name + '.rsa.pub'):
        subprocess.Popen("cat "+KEY_DIR + key_file_name + ".rsa.pub | ssh -i "+KEY_DIR+".provinet-key.rsa "+dst_user+"@"+dst_ip+" 'cat - >> ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys'",
                          executable="/bin/bash", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return True
    else:
        return False
