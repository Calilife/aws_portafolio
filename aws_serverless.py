import json
import boto3 
import StringIO
import zipfile
import mimetypes 

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:802992738993:CodeDeployTopic') 
    
    try:
        s3 = boto3.resource('s3')
        portafolio_bucket = s3.Bucket('portafolio.vesgasebas.net')
        portafoliobuild_bucket = s3.Bucket('portafoliobuild.vesgasebas.net')
        
        portafolio_zip = StringIO.StringIO()
        portafoliobuild_bucket.download_fileobj('CodeBuild_Portafolio_VesgaSebas.zip', portafolio_zip)
    
        with zipfile.ZipFile(portafolio_zip) as myzip:  
            for nm in myzip.namelist(): 
                obj = myzip.open(nm) 
                portafolio_bucket.upload_fileobj(obj, nm) 
                portafolio_bucket.Object(nm).Acl().put(ACL='public-read')
        print('Job Completed')
        topic.publish(Subject="Deploy Portafolio Vesgasebas.Net - Completed", Message="Lambda was able to deploy the code to s3") 
    except: 
        topic.publish(Subject="Deploy Portafolio Vesgasebas.Net - Failed", Message="Lambda was UNABLE to deploy the code to s3") 
        raise
    return "Hello Lambda"


""" import boto3 
from botocore.client import config
import io
import zipfile
import mimetypes 

s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

portafolio_bucket = s3.Bucket('portafolio.vesgasebas.net')
portafoliobuild_bucket = s3.Bucket('portafoliobuild.vesgasebas.net')

portafolio_zip = io.BytesIO()
portafoliobuild_bucket.download_fileobj('odeBuild_Portafolio_VesgaSebas.zip', portafolio_zip)

with zipfile.ZipFile(portafolio_zip) as myzip:  
    for nm in myzip.namelist(): 
        obj = myzip.open(nm) 
        portafolio_bucket.upload_fileobj(obj, nm, 
            ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]}) 
        portafolio_bucket.Object(nm).Acl().put(ACL='public-read') """

""" with zipfile.ZipFile(portafolio.zip) as myzip:
    for nm in myzip.namelist(): 
    print(nm)
with zipfile.ZipFile(portafolio_zip) as myzip:  
    for nm in myzip.namelist(): 
        obj = myzip.open(nm) 
        portafolio_bucket.upload_fileobj(obj, nm) 
        #This lines are just for my reference, as they help me to validate"""