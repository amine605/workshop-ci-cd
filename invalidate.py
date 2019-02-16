import json
import boto3
from datetime import datetime
def lambda_handler(event, context):
    try :
        files = ["*"]
        cloudfront = boto3.client('cloudfront')
        s3 = boto3.resource('s3')
        codepipeline_client = boto3.client('codepipeline')
        bucket = s3.Bucket('bucket-name')
        cloudfront.create_invalidation(
            DistributionId='destribution-id',
            InvalidationBatch={
                'Paths': {
                    'Quantity': 1,
                    'Items': ['/**/*']
                },
                'CallerReference': 'my-references-{}'.format(datetime.now())
            }
        )

        return codepipeline_client.put_job_success_result(
            jobId=event["CodePipeline.job"]["id"]
        ) 
    except Exception as e:
        return codepipeline_client.put_job_failure_result(
            jobId=event["CodePipeline.job"]["id"],
            failureDetails={
                'type':'JobFailed',
                'message':str(e)
                
            }
            
        ) 
