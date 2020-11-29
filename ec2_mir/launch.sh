#!/bin/bash
aws ec2 run-instances --image-id ami-003634241a8fcdec0 --security-group-ids sg-09c4618f69b2e5910\
 --user-data file://userdata.sh --instance-type t2.micro --key-name corwin  --iam-instance-profile Name=S3fullaccess
