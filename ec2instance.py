#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError

ec2_sg = boto3.client('ec2')
ec2 = boto3.resource('ec2')

#Creating KeyPair

def keypair_name(keyname):
    return keyname+".pem"

def create_keypair(keyname):
    with open(keypair_name(keyname),'w') as outfile:
        key_pair = ec2.create_key_pair(KeyName=keyname)
        KeyPairOut = str(key_pair.key_material)
        outfile.write(KeyPairOut)
        return KeyPairOut

#Creating Instances

def instance(imageid,mincount,maxcount,instancetype,kname,subnetid,groupid):
    instances = ec2.create_instances(
            ImageId=imageid,
            MinCount=int(mincount),
            MaxCount=int(maxcount),
            InstanceType=instancetype,
            KeyName=kname,
            NetworkInterfaces = [{
                'SubnetId':subnetid,
                'DeviceIndex':0,
                'AssociatePublicIpAddress':True,
                'Groups':[groupid]
                }],
        )
    return instances

###Creating Security Group###

#1.Create Security Group

def create_sg(gpname,des,vpcid):
    try:
        vpc_create = ec2_sg.create_security_group(GroupName=gpname,
                                               Description=des,
                                               VpcId=vpcid)
        
        global security_gp_id
        security_gp_id = vpc_create['GroupId']
        return f'Security Group Created {security_gp_id} in vpc {vpcid}'

    except ClientError as e:
        return e

#2.Rule into Security Group

def rule_to_sg(fromport,toport,allow):
    data = ec2_sg.authorize_security_group_ingress(
            GroupId = security_gp_id,
            IpPermissions = [
                {'IpProtocol' : 'tcp',
                 'FromPort' : fromport,
                 'ToPort' : toport,
                 'IpRanges' : [{'CidrIp' : allow}]}])
    return f'Ingress Successfully Set {data}'

#Main Function Call

def main():
    ok = True
    no_of_keypair = 0
    create_or_not = input("Create New KeyPair? [Y/n] ") #1.Creating KeyPair
    if create_or_not.lower() == 'y':
        while ok:
            keyname = input("Create KeyPair Name :")
            print(create_keypair(keyname))
            no_of_keypair += 1
            ask = input("Create another one? [Y/n]")
            if ask.lower() == "n":
                ok = False

        print("+++++Number of KeyPairs Created+++++ :", no_of_keypair,"keypairs")
    else:
        gpname = input("Security Group Name :") #2.Creating Security Group
        des = input("Any Description about Security Group :")
        vpcid=input("Enter VPC ID :")
        print(create_sg(gpname,des,vpcid))

        ok_sg = True
        while ok_sg:
            fromport = int(input("From Port :"))
            toport = int(input("To Port :"))
            allow = input("Allow CIDR ?")
            print(rule_to_sg(fromport,toport,allow))
            ask = input("Add Rules again? [Y/n]")
            if ask.lower() != 'y':
                ok_sg = False
        
        imageid=input("AMI ID :") #3.Creating Instances
        mincount = input("Mininum EC2 Instance :")
        maxcount = input("Maximum EC2 Instance :")
        instancetype = input("Instance Type :")
        kname = input("Key Name :")
        subnetid = input("Enter Subnet ID :")
        groupid = input("Security Group ID :")

        print(instance(imageid,mincount,maxcount,instancetype,kname,subnetid,groupid))


if __name__ == "__main__":
    main()

