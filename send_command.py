from pexpect import pxssh
import getpass
from pip._vendor.distlib.compat import raw_input
import ipaddress

try:
    s = pxssh.pxssh()
    # hostname = raw_input('hostname: ')
    # username = raw_input('username: ')
    # password = getpass.getpass('password: ')
    ip_list = open('/home/switches/ip_list', 'r')
    for hostname in ip_list:
        if not s.login(hostname, 'melsayeh', 'Ma1ri2am', auto_prompt_reset=False):
            print("SSH session failed on login")
        else:
            s.interact()
            s.prompt()
            s.sendline('conf t')
            print(s.before)
            s.sendline('default-gateway 10.251.223.129')  # run a command
            s.prompt()  # match the prompt
            print(s.before)  # print everything before the prompt.
            s.sendline('no ip route 0.0.0.0 0.0.0.0 10.251.223.129')
            s.prompt()
            print(s.before)
            s.sendline('wr mem')
            s.prompt()
            print(s.before)
            s.logout()
except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(str(e))
