#!/usr/bin/env python
import rospy
import subprocess, shlex
from time import sleep

if __name__ == '__main__':
    rospy.init_node('main_controller_installer')
    static_ip = rospy.get_param('~main_controller_ip', '0.0.0.0')
    robot_ip = rospy.get_param('~robot_ip', '0.0.0.0')
    port_number = rospy.get_param('~port_number', 4325)

    command = "sudo sed -i 's/\* \* \* \* \* \/usr\/bin\/screen -S reverse-ssh-tunnel -d -m autossh -p222 -M 65500 -i \/home\/pi\/.ssh\/id_rsa -o \"ServerAliveInterval 20\" -o \"ServerAliveCountMax 3\" -R .*\\:localhost:22 radio@mule.iit.demokritos.gr/\* \* \* \* \* \/usr\/bin\/screen -S reverse-ssh-tunnel -d -m autossh -p222 -M 65500 -i \/home\/pi\/.ssh\/id_rsa -o \"ServerAliveInterval 20\" -o \"ServerAliveCountMax 3\" -R "+str(port_number)+":localhost:22 radio@mule.iit.demokritos.gr/g' /var/spool/cron/crontabs/pi"
    command = shlex.split(command)
    subprocess.Popen(command)
    sleep(2)

    command = "sudo sed -ri 's/^ *[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+( +main-controller)/"+static_ip+"\\1/' /etc/hosts"
    command = shlex.split(command)
    subprocess.Popen(command)
    sleep(2)

    command = "sudo sed -ri 's/^ *[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+( +turtlebot-ncsr-2)/"+robot_ip+"\\1/' /etc/hosts"
    command = shlex.split(command)
    subprocess.Popen(command)
    sleep(2)

    broadcast_ip = static_ip.split('.')[0] + '.' + static_ip.split('.')[1] + '.' + static_ip.split('.')[2] + '.1'

    command = "sudo -i sed 's/static ip_address=.*\\/24/static ip_address="+static_ip+"\\/24/g' /etc/dhcpcd.conf"
    command = shlex.split(command)
    subprocess.Popen(command)
    sleep(2)

    command = "sudo sed -i 's/static routers=.*/static routers="+broadcast_ip+"/g' /etc/dhcpcd.conf"
    command = shlex.split(command)
    subprocess.Popen(command)
    sleep(2)

    command = "sudo sed -i 's/static domain_name_servers=.*\\, 208.67.220.220/static domain_name_servers="+broadcast_ip+"\\, 208.67.220.220/g' /etc/dhcpcd.conf"
    command = shlex.split(command)
    subprocess.Popen(command)
    sleep(2)

    command = "sed -i 's/ROS_IP=.*/ROS_IP="+static_ip+"/g' /home/pi/.bashrc"
    command = shlex.split(command)
    subprocess.Popen(command)
    sleep(2)

    command = "sed -i 's/ROS_IP=.*/ROS_IP="+static_ip+"/g' /home/pi/startup.sh"
    command = shlex.split(command)
    subprocess.Popen(command)
    sleep(2)
