#!/usr/bin/env python3

import boto3

ec2 = boto3.resource('ec2')

def info_ec2():
    print('')
    print('########## EC2 INSTANCE INFORMATION ##########')
    for instance in ec2.instances.all():
        print("Id: {0}\nPlatform: {1}\nType: {2}\nPublic IPv4: {3}\nAMI: {4}\nState: {5}\n".format(
         instance.id, instance.platform, instance.instance_type, instance.public_ip_address, instance.image.id, instance.state))
    print('########## END ##########')
    print('')

def start_ec2(ids):
    ec2.Instance(ids).start()

def stop_ec2(ids):
    ec2.Instance(ids).stop()

def reboot_ec2(ids):
    ec2.Instance(ids).reboot()

def main():

    while True:
        user_input = input("Enter 1 to start\nEnter 2 to stop\nEnter 3 to reboot the instance\nEnter 4 for Instance Information\nType q to quit:")
        if user_input == '1':
            while True:
                ids = input('Enter Instance ID :')
                start_ec2(ids)
                ask = input('Start Another Instance?[Y/n]')
                if ask.lower() != 'y':
                    break
        elif user_input == '2':
            while True:
                ids = input('Enter Instantce ID :')
                stop_ec2(ids)
                ask = input('Stop Another Instatnce?[Y/n]')
                if ask.lower() !='y':
                    break
        elif user_input =='3':
            while True:
                ids = input('Enter Instance ID :')
                reboot_ec2(ids)
                ask = input('Reboot Another Instance?[Y/n]')
                if ask.lower() != 'y':
                    break
        elif user_input == '4':
            info_ec2()
        elif user_input == 'q':
            break
    print('Good Bye')

if __name__ == "__main__":
    main()


