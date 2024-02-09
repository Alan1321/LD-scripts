import boto3

def stop_ec2(instance_id):
    aws_management_console = boto3.session.Session()
    ec2_console = aws_management_console.client(service_name='ec2')
    response = ec2_console.stop_instances(
        InstanceIds=[instance_id]
    )