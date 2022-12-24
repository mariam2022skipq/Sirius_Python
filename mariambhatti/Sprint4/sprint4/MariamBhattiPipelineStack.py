#Marimbhatti pipeline stack
import aws_cdk as cdk
from aws_cdk import Stack
from constructs import Construct
import aws_cdk.pipelines as pipelines_
from aws_cdk import aws_codepipeline_actions as actions_
import aws_cdk.pipelines as pipelines_
from aws_cdk import aws_codebuild as codebuild
from sprint4.MariamBhattiStage import MariamBhattiStage

class MariamBhattiPipelineStack(Stack):
    #initializing the stack
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #Accessing github credentials
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipelineSource.html
        source = pipelines_.CodePipelineSource.git_hub("mariam2022skipq/Sirius_Python", "main",
                                                       authentication=cdk.SecretValue.secrets_manager("MariamToken"),
                                                       trigger=actions_.GitHubTrigger('POLL'))

        #Add shell step to synthesize application
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/ShellStep.html
        synth=pipelines_.ShellStep("Synth",
                                   input=source,
                                   commands=["ls",
                                          "cd mariambhatti/Sprint4/",
                                          "npm install -g aws-cdk",
                                          "pip install -r requirements.txt",
                                          "cdk synth"],
                                    primary_output_directory="mariambhatti/Sprint4/cdk.out")
        #create a pipeline
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/ShellStep.html
        pipeline=pipelines_.CodePipeline(self, "MariamBhattiPipelineSprint4", synth=synth)

        ##Adding stages
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
        betaTesting=MariamBhattiStage(self, "Beta")  #have to pass self and I
        
        #https://docs.aws.com/codebuild/latest/userguide/sample-docker-custom-image.html
        pyresttest=pipelines_.CodeBuildStep("Mariam_API_tests", commands=[],build_environment=codebuild.BuildEnvironment(
            build_image=codebuild.LinuxBuildImage.from_asset(self, "Pyresttest-Image", directory="./pyrest").from_docker_registry(name="docker:dind"),privileged=True),
            partial_build_spec = codebuild.BuildSpec.from_object({
                "version": 0.2,
                "phases": {
                "install":{
                    "commands": [
                    "nohup /usr/local/bin/dockerd --host=unix:///var/run/docker.sock --host=tcp://127.0.0.1:2375 --storage-driver=overlay2 &",
                    "timeout 15 sh -c \"until docker info; do echo .; sleep 1; done\""
                    ]
                },
                "pre_build":{
                    "commands":["cd mariambhatti/Sprint4/pyrest", "docker build -t api-mar-7."]
                }, 
                "build":{
                    "commands":["docker run api-mar-7"]
                }
                } 
            }))
        
        pipeline.add_stage(betaTesting, pre =[
                                pipelines_.ShellStep("Synth", input=source, 
                                commands=[  'cd mariambhatti/Sprint4/',
                                            'npm install -g aws-cdk',
                                            "pip install -r requirements.txt",
                                            "pip install -r requirements-dev.txt",
                                             "python3 -m pytest",
                                             ],
                                        
                                            
                                )
                            ]
                           ,post=[pyresttest]
                        )
        
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
        # prod stage for pipeline
        prod=MariamBhattiStage(self, "Prod") #this is a prod stage ; it is not a testing stage
        pipeline.add_stage(prod, pre =[
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/ManualApprovalStep.html
        
            pipelines_.ManualApprovalStep("ManualProd") 
                                          
                                ]
                    )
    