#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')

def sg(gpname,des,vpcid):
    try:
        secgp = ec2.create_security_group(GroupName=gpname,Description=des,VpcId=vpcid)
        secgp_id = secgp['GroupId']
        print(f'Security Group of {secgp_id} is created in VPC : {vpcid}')
        
        ok = True
        while ok:
            fromport = int(input(" FromPort : "))
            toport = int(input(" ToPort :"))
            cidr = input("Allow CIDR :")

            data = ec2.authorize_security_group_ingress(
                GroupId=secgp_id,
                IpPermissions = [
                    {'IpProtocol':'tcp',
                        'FromPort':fromport,
                        'ToPort':toport,
                        'IpRanges':[{'CidrIp':cidr}]}
                    ])
            ask = input("Add Rule again? [Y/n] ")
            if ask.lower () != "y":
                ok = False

        return f'Ingress Successfully Set {data}'
    except ClientError as e:
        return e

def del_sg(sgid):
    try:
        deLsg = ec2.delete_security_group(GroupId=sgid)
        return f'Security Group:{sgid} is deleted'
    except ClientError as e:
        return e

def main():
    print('Enter 1 to Add Security Group')
    print('Enter 2 to Delete Security Group')
    user_ask = input()
    if user_ask == '1':
        gpname = input('Security Group Name :')
        des = input('Description about Security Group :')
        vpcid = input('VPC ID :')
        print(sg(gpname,des,vpcid))
    elif user_ask == '2':
        while True:
            sgid = input("Security Group ID :")
            print(del_sg(sgid))
            ask = input("Delete Another Security Group? [Y/n]")
            if ask.lower() != 'y':
                break
    else:
        print('Only 1 and 2 are allowed for input')

if __name__ == "__main__":
    main()
