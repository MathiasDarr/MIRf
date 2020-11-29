#!/bin/bash


if [[ -z $2 ]]
then
  stackname=librosa-flask-stack
else
  stackname=$2
fi

echo ${stackname}


if [[ $1 == 'aws' ]]
then
    aws cloudformation deploy \
      --template-file aws/cloudformation_core_stack_template.yaml \
      --stack-name ${stackname} \
      --capabilities CAPABILITY_NAMED_IAM

elif [[ $1 == 'local' ]]
then
  aws --endpoint-url=http://localhost:4566 s3 mb s3://dakobed-lach-orders
  python3 copy_sam_archive.py
#  awslocal apigateway create-rest-api --region ${REGION} --name ${API_NAME}

  aws  --endpoint-url=http://localhost:4566 cloudformation deploy \
      --template-file aws/cloudformation_core_stack_template.yaml \
      --stack-name ${stackname} \
      --capabilities CAPABILITY_NAMED_IAM
else
    echo "choose either local or aws"
fi
