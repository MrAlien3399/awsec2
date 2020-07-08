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

gpname = input('Security Group Name :')
des = input('Description about Security Group :')
vpcid = input('VPC ID :')
print(sg(gpname,des,vpcid))

