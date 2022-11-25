#Marimbhatti pipeline stack
import aws_cdk as cdk
from aws_cdk import Stack
from constructs import Construct
import aws_cdk.pipelines as pipelines_
import aws_codepipeline_actions as actions_
import aws_cdk.pipelines as pipelines_
from sprint3.MariamBhattiStage import MariamBhattiStage

class MariamBhattiPipelineStack(Stack):
    #initializing the stack
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        #accessing github credentials
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipelineSource.html
        source = pipelines_.CodePipelineSource.git_hub("mariam2022skipq/Sirius_Python", "main",
                                                       authentication=cdk.SecretValue.secrets_manager("PipelineTokenMariam"),
                                                       trigger=actions_.GitHubTrigger('POLL'))

        #Add shell step to synthesize application
        synth=pipelines_.ShellStep("Synth",
                                   input=source,
                                   commands=["ls",
                                          "cd mariambhatti/Sprint3/",
                                          "npm install -g aws-cdk",
                                          "pip install -r requirements.txt",
                                          "cdk-synth"],
                                    primary_output_directory="mariambhatti/Sprint3/cdk.out")
        #create a pipeline
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/ShellStep.html
        pipeline=pipelines_.CodePipeline(self, "MariamBhattiPipelineSprint3", synth=synth)
    