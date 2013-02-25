import subprocess
from provinet.settings import STATICFILES_DIRS
from provinet.dnsservers.models import DNSServer

KEY_DIR = STATICFILES_DIRS[0] + '/keys/'

def addSubdomain(subdomain, ip_list):
    """
    Add an entry at the /etc/bind/zones/provinet.local.db in the first DNSServer configured in the machine
    """
    dnsserver = DNSServer.objects.filter(status=True)[:1].get() # 1st with status True
    print "Creating subdomain..."+KEY_DIR
    for i in range(len(ip_list)):
        print "to aki"
        # ssh -i .provinet-key.rsa root@143.54.12.183 "echo 'userteste     IN    A    143.54.12.104' >> /etc/bind/zones/provinet.local.db"
        command = "ssh -i "+KEY_DIR+".provinet-key.rsa root@"+dnsserver.url+" 'echo '"+subdomain+"     IN    A    "+ip_list[i]+"' >> /etc/bind/zones/provinet.local.db'"
        
        print command
        subprocess.Popen(command, executable="/bin/bash", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    command2 = "ssh -i "+KEY_DIR+".provinet-key.rsa root@"+dnsserver.url+" 'service bind9 restart'"
    subprocess.Popen(command2, executable="/bin/bash", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return True
