import aws_cdk as cdk

from app_prova.app_prova_stack import AppProvaStack

app = cdk.App()
stack = AppProvaStack(app, "app-prova1")

app.synth()

