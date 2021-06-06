import csv
import threading
from queue import Queue
from getpass import getpass
from netmiko import ConnectHandler
import os



# username = getUsername()
# password = getPassword()
plateform = 'cisco_ios'

#open switch ip list
switches = open('/path/tp/switch/list')
#convert swith list into python list
switches_list = [switchip.rstrip() for switchip in switches]

#open the config file
config_file = open('/path/to/config/file')

#convert config file into python list
command_list = [line.rstrip() for line in config_file]

x=12
n = 1

def ssh_session(switch, output_q):
    # Place what you want each thread to do here, for example connect to SSH, run a command, get output
    output_dict = {}
    #hostname = switch
    ssh_session = ConnectHandler(device_type=plateform, ip=switch, username=getUsername(), password=getPassword(),
                                 global_delay_factor=5, session_log='output.log')
    print(ssh_session.find_prompt())
    ssh_session.write_channel('command to access switch')
    time.sleep(1)
    ssh_session.read_channel()
    redispatch(ssh_session, device_type='cisco_ios')

    print(50 * '*' + "\nConnecting to " + host.strip('\n') + ". Please wait ..." + "\n\n")
    output0 = ssh_session.send_config_set(command_list, cmd_verify=False)
    print(output0)
    print("\nConfiguration has been pushed successfully!\n" + 50 * '*')
    output_dict[switch] = output
    output_q.put(output_dict)
    ssh_session.disconnect()

def getUsername():
    sshUsername = input("Enter SSH username: ")
    return (sshUsername)

def getPassword():
    pwd = getpass.getpass(prompt='Enter SSH password: ')
    return (pwd)


    ###############


if __name__ == "__main__":

    output_q = Queue()

    # Start thread for each router in routers list
    for switch in switches_list:
        my_thread = threading.Thread(target=ssh_session, args=(switch, output_q))
        my_thread.start()

    # Wait for all threads to complete
    main_thread = threading.currentThread()
    for some_thread in threading.enumerate():
        if some_thread != main_thread:
            some_thread.join()

    # Retrieve everything off the queue - k is the router IP, v is output
    # You could also write this to a file, or create a file for each router

    while not output_q.empty():
        my_dict = output_q.get()
        for k, val in my_dict.iteritems():
            print
            k
            print
            val


