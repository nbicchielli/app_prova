from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_kinesis as kinesis,
    aws_kinesisanalytics as kda,
    RemovalPolicy,
    aws_s3 as s3, aws_glue, aws_iam
)

class AppProvaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        data_stream = kinesis.Stream(
            self,
            'SensorStream',
            stream_name='SensorStream',
            retention_period=Duration.hours(24),
        )
        data_bucket = s3.Bucket(self, 'sensordatabucket-trial-1234214321',
                                removal_policy=RemovalPolicy.DESTROY,
                                auto_delete_objects=True)

        kda_app = kda.CfnApplicationV2(self, 'SensorDataAnalytics',
                                       runtime_environment='FLINK-1_15',
                                       service_execution_role="arn:aws:iam::286658983203:role/kinesis_role")
