"""
author  :   leo
comment :   Tag all instances by ip
version :   1.0
"""

import boto3
import sys
import getopt


def help():
    print("TagBy.py -p <profile> -f <file contains list of ips> -t [{'<key>','<value>'},...]")
    print("TagBy.py --profile <profile> --file <file contains list of ips> --tags [{'<key>','<value>'},...]")

def tagByIp(tag, prof):
    ec2 = prof.resource('ec2')
    print("Reading all ips...")
    ip_list = [line.rstrip('\n')  for line in open("iplist.txt",'r')]
    print("Getting all instance ids releted to list of ips...")
    ins_ids= [ line.id for line in ec2.instances.filter(Filters = [{'Name':'private-ip-address','Values':ip_list}])]
    print("Tagging all instances...")

    response = ec2.create_tags(
    DryRun=False,
    Resources=ins_ids,
    Tags=[
            {
                'Key': 'Project',
                'Value': 'Optimus'
            },
        ]
    )
    print(response)


def main():
    options, remainder = getopt.getopt(sys.argv[1:], 'p:f:t:', ['profile=', 'file=', 'tags='])
    for opt, arg in options:
        if opt in ('-p', '--profile'):
            prof = arg
        elif opt in ('-f', '--file'):
            file = arg
        elif opt in ('-t', '--tags'):
            tags = arg.split(":")
        else:
            help()
    prof = boto3.session.Session(profile_name=prof)
    tagByIp(file, prof)


if __name__ == "__main__":
    main()
    