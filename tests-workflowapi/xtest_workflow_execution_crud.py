# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

##############################################################################
# Integration testing for the MIE workflow API
#
# PRECONDITIONS:
# MIE base stack must be deployed in your AWS account
#
# Boto3 will raise a deprecation warning (known issue). It's safe to ignore.
#
# USAGE:
#   cd tests/
#   pytest -s -W ignore::DeprecationWarning -p no:cacheprovider
#
###############################################################################

import pytest
import boto3
import json
import time
import math
import requests
import urllib3
import logging
from botocore.exceptions import ClientError
import re
import os
from jsonschema import validate

# local imports
import api 
import validation

REGION = os.environ['REGION']
BUCKET_NAME = os.environ['BUCKET_NAME']
MIE_STACK_NAME = os.environ['MIE_STACK_NAME']
VIDEO_FILENAME = os.environ['VIDEO_FILENAME']
IMAGE_FILENAME = os.environ['IMAGE_FILENAME']
AUDIO_FILENAME = os.environ['AUDIO_FILENAME']
TEXT_FILENAME = os.environ['TEXT_FILENAME']



def test_workflow_execution_api(operations, stages, workflow_configs, stack_resources, api_schema):

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print("Running /workflow/execution API tests")
    for config in workflow_configs:
        
        print("----------------------------------------")
        print("\nTEST WORKFLOW EXECUTION CONFIGURATION: {}".format(config))

        # Create the workflow
        create_workflow_response = api.create_workflow_request(config, stack_resources)
        workflow = create_workflow_response.json()
        
        assert create_workflow_response.status_code == 200
        validation.schema(workflow, api_schema["create_workflow_response"])

        get_workflow_response = api.get_workflow_request(workflow, stack_resources)
        workflow = get_workflow_response.json()
        assert get_workflow_response.status_code == 200
        validation.schema(workflow, api_schema["create_workflow_response"])

        # Execute the workflow and wait for it to complete
        create_workflow_execution_response = api.create_workflow_execution_request(workflow, config, stack_resources)
        workflow_execution = create_workflow_execution_response.json()
        assert create_workflow_execution_response.status_code == 200
        assert workflow_execution['Status'] == 'Queued'
        
        #FIXME - validate create_workflow_response
        #validation.schema(workflow_execution, api_schema["create_workflow_execution_response"])
        workflow_execution = api.wait_for_workflow_execution(workflow_execution, stack_resources, 120)
        if config["Status"] == "OK":
            assert workflow_execution["Status"] == "Complete"
            
            # Check output media for expected types
            for outputType in config["Outputs"]:
                if outputType != "None":
                    assert outputType in workflow_execution["Globals"]["Media"]
                     
        else:
            assert workflow_execution["Status"] == "Error"

        # validation.stage_execution(workflow_execution, config, stack_resources, api_schema)

        # Delete the workflow
        delete_workflow_response = api.delete_stage_workflow_request(workflow, stack_resources)
        assert delete_workflow_response.status_code == 200
        
        #Delete the workflow
        delete_stage_response = api.delete_stage_request(workflow, stack_resources)
        assert delete_stage_response.status_code == 200




#TODO: dynamoDB remove asset