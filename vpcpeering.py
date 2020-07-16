#!/usr/bin/env python3

import boto3

ec2 = boto3.resource('ec2')

#Requester VPC ID

def requester(req_id):
    vpc = ec2.Vpc(req_id)
    return vpc

def peering_conn(req_id,aws_id,accept_id,region_id):
    global vpc_peering_connection
    vpc_peering_connection = requester(req_id).request_vpc_peering_connection (
        PeerOwnerId=aws_id,
        PeerVpcId= accept_id,
        PeerRegion= region_id
        )
  
    return f'VPC Peering Connection {vpc_peering_connection.id} is created'

def accept():
    accepted = vpc_peering_connection.accept()

def main():
    req_id = input('VPC Id :')
    aws_id = input('AWS Account ID :')
    accept_id = input('Accepter VPC ID :')
    region_id = input('Region ID of Accepter :')
    print(peering_conn(req_id,aws_id,accept_id,region_id))
    accept()

if __name__ == "__main__":
    main()
