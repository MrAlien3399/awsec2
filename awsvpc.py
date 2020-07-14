#!/usr/bin/env python3

import boto3

ec2 = boto3.resource('ec2')

#Create VPC 
def create_vpc(vpc_cidr,tag_value):
    
    global vpc
    vpc = ec2.create_vpc(CidrBlock=vpc_cidr)
    vpc.create_tags(Tags = [{'Key':'Name','Value':tag_value}])
    vpc.wait_until_available()

    return f'VPC Created {vpc.id}'

#Create Internet Gateway

def create_igw():
    
    global igw
    igw = ec2.create_internet_gateway()
    vpc.attach_internet_gateway(InternetGatewayId=igw.id)
    
    return f'Internet Gateway Created {igw.id}'

#Create Subnet

def create_subnet(subnet_cidr,azid,tag_value):

    global subnet
    subnet = ec2.create_subnet(CidrBlock=subnet_cidr,VpcId=vpc.id,AvailabilityZoneId=azid)
    subnet.create_tags(Tags = [{'Key':'Name','Value':tag_value}])
    
    return f'Subnet Created {subnet.id}'

#Create Route Table

def create_rt(tag_value,descidrblock,subnetid):
    rt = vpc.create_route_table(VpcId=vpc.id)
    rt.create_tags(Tags = [{'Key':'Name','Value':tag_value}])
    rt.create_route(DestinationCidrBlock=descidrblock,GatewayId=igw.id)
    rt.associate_with_subnet(SubnetId=subnetid)

    return f'Route Table Created {rt.id}'

#Create Security Groups

def create_sg(gpname,des):

    sg = ec2.create_security_group(GroupName=gpname,Description=des,VpcId=vpc.id)

    while True:
        cidr = input('Allow CIDR :')
        fromport = input('FromPort :')
        toport = input('ToPort :')
        sg.authorize_ingress(CidrIp=cidr,IpProtocol='tcp',FromPort=int(fromport),ToPort=int(toport))
        ask = input('Add Rule Again? [Y/n]')
        if ask.lower() != 'y':
            break

    return f'Security Group Created {sg.id}'

def main():
    vpc_cidr = input('VPC CIDR Block :')
    tag_value = input('Tag Value for VPC :')
    print(create_vpc(vpc_cidr,tag_value))
    
    print(create_igw())

    while True:
        subnet_cidr = input('Subnet CIDR :')
        azid = input('Availability Zone ID :')
        tag_value = input('Tag Value for Subnet :')
        print(create_subnet(subnet_cidr,azid,tag_value))
        ask = input('Create Subnet Again?[Y/n]')
        if ask.lower() != 'y':
            break
    
    while True:
        tag_value = input('Tag Value for Route Table :')
        descidrblock = input('Destination Route :')
        subnetid = input('Associate Subnet ID :')
        print(create_rt(tag_value,descidrblock,subnetid))
        ask = input('Create Route Table Again?[Y/n]')
        if ask.lower() != 'y':
            break

    gpname = input('Security Group Name :')
    des = input('Security Group Description :')
    print(create_sg(gpname,des))

if __name__ == "__main__":
    main()
