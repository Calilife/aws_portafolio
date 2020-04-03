import json
import boto3 
import StringIO
import zipfile
import mimetypes 

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:802992738993:CodeDeployTopic') 
    
    location = {
        "bucketName": 'portafoliobuild.vesgasebas.net',
        "objectKey": 'CodeBuild_Portafolio_VesgaSebas.zip'
    }
    
    try:
        job = event.get("CodePipeline.job")
        
        if job: 
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "BuildArtifact": 
                    location = artifact["location"]["s3Location"]
                    
        print('Building Portafolio from ' + str(location))            
        
        s3 = boto3.resource('s3', config=boto3.session.Config(signature_version='s3v4'))
        
        portafolio_bucket = s3.Bucket('portafolio.vesgasebas.net')
        portafoliobuild_bucket = s3.Bucket(location["bucketName"])
        
        portafolio_zip = StringIO.StringIO()
        portafoliobuild_bucket.download_fileobj(location["objectKey"], portafolio_zip)
    
        with zipfile.ZipFile(portafolio_zip) as myzip:  
            for nm in myzip.namelist(): 
                obj = myzip.open(nm) 
                portafolio_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portafolio_bucket.Object(nm).Acl().put(ACL='public-read')
        print('Job Completed')
        topic.publish(Subject="Deploy Portafolio Vesgasebas.Net - Completed", Message="Lambda was able to deploy the code to s3") 
        if job: 
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except: 
        topic.publish(Subject="Deploy Portafolio Vesgasebas.Net - Failed", Message="Lambda was UNABLE to deploy the code to s3") 
        raise
    return "Hello Lambda"
