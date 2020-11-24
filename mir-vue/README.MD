# Dakobed Vue Frontend
Front end web application developed using Vue, Vuex, Vuetify & AWS Cognito authentication

Run locally
npm install 
npm run serve

### This directory contains ###
* Single page application developed with Vue
* CloudFormation template for instantiating an AWS Cognito UserPool.  

Host the SPA in an S3 bucket.  

npm run build
serve ./dist

aws s3 sync ./dist s3://dakobed-bard.com





### Serve the distribution

serve ./dist