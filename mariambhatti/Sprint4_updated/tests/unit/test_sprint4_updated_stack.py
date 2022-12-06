import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint4_updated.sprint4_updated_stack import Sprint4UpdatedStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint4_updated/sprint4_updated_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Sprint4UpdatedStack(app, "sprint4-updated")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
