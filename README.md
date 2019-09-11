# Media Insights Engine

Welcome to the preview of the Media Insights Engine (MIE) project!

Media Insights Engine is a framework that makes analyzing and transforming media in applications quick and easy. MIE lets builders: 

1. Create media analysis workflows from a library of base operations built on AWS Machine Learning and Media Services such as AWS Rekognition, AWS Transcribe, AWS Translate, AWS Cognito, AWS Polly, and AWS MediaConvert.
2. Execute workflows and persist the resulting media and analysis for later use.
3. Query analysis extracted from media.
4. Interatively explore some of the capabilities of MIE using the included content and analysis and search web application.
5. Extend MIE for new applications by adding custom operators and custom data stores.
   

# Architecture Overview

Media Insights Engine is a serverless architecture on AWS.  The following diagram is an overview of the major components of MIE and how they interact when an MIE workflow is executed.  

![](doc/images/MIE-execute-workflow-architecture.png)


**Workflow API** Trigger the execution of a workflow. Trigger creation of assets in the data plane (see below). Create, update and delete workflows and operators.  Monitor the status of workflows.

**Control plane** Executes the AWS Step Functions state machine for the workflow against the provided input.  Workflow state machines are generated from MIE operators.  As operators within the state machine are executed, the interact with the MIE dataplane to store and retrieve dervied asset and metadata generated from the workflow.  

**Data plane:** Storage, retrieval, and search functionality for assets and metadata derived by workflows.

**Data plane API:** 

MIE manages the following objects:

**Operators:** Transform or extract metadata from media.  

**Stages:** Group of operators that can be executed in parallel for increased workflow performance.

**Workflows:** Execution of a sequence of operators or stages in a pipeline.  

**Assets:** A media object that has been processed by a MIE workflow. Extracted metadata and derived assets can be retreived using an assetId.


# Installation / Deployment
Deploy the demo architecture and application in your AWS account and start exploring your media.

Region| Launch
------|-----
US East (Virgina) | [![Launch in us-east-1](doc/images/launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=mie&templateURL=https://rodeolabz-us-east-1.s3.amazonaws.com/media-insights-solution/v0.1.0/cf/media-insights-stack.template)

# Usage

###  Sample application

![](doc/images/MIEDemo.gif)

The Media Insights sample application lets you upload videos, images, audio and text files for content analysis and add the results to a collection that can be searched to find media that has attributes you are looking for.  It runs an MIE workflow that extracts insights using many of the ML content analysis services available on AWS and stores them in a search engine for easy exploration.  A web based GUI is used to search and visualize the resulting data along-side the input media.  The analysis and transformations included in MIE workflw for this application include:

* Proxy encode of videos and separation of video and audio tracks using **AWS MediaConvert**. 
* Object, scene, and activity detection in images and video using **AWS Rekognition**. 
* Celebrity detection in images and video using **AWS Rekognition**
* Face search from a collection of known faces in images and video using **AWS Rekognition**
* Facial analysis to detect facial features and faces in images and videos to determine things like happiness, age range, eyes open, glasses, facial hair, etc. In video, you can also measure how these things change over time, such as constructing a timeline of the emotions expressed by an actor.  From **AWS Rekognition**.
* Unsafe content detection using **AWS Rekognition**. Identify potentially unsafe or inappropriate content across both image and video assets. 
* Convert speech to text from audio and video assets using **AWS Transcribe**.
* Convert text from one language to another uing **AWS Translate**.
* Identify entities in text using **AWS Comprehend**. 
* Identify key phrases in text using **AWS Comprehend**

Data are stored in AWS Elasticsearch search engine and can be retrieved using Lucene queries in the Collection view search page.

### Example use cases for Media Insights Engine
 
MIE is a reusable architecture that can support many different applications.  Examples:
 
* **Content analysis analysis and search** - Detect objects, people, celebrities and sensitive content, transcribe audio and detect entities, relationships and sentiment.  Explore and analyze media using full featured search and advanced data visualization.  This use case is implemented in the included sample application.
* **Automatic Transcribe and Translate** - Generate captions for Video On Demand content using speech recognition.  
* **Content Moderation** - Detect and edit moderated content from videos.

# Developer Quickstart

The Media Analysis Engine is built to be extended for new use cases.  You can:

* Run existing workflows using custom runtime confgurations.
* Create new operators for new types of analysis or transformations of your media.
* Create new workflows using the existing operators and/or your own operators.
* Add new data consumers to provide data management that suits the needs of your application.

See the [Developer Guide](https://github.com/awslabs/aws-media-insights-engine/blob/master/DEVELOPER_QUICK_START.md) for more information on extending the application for a custom use case.

API Reference - Coming soon!

Builder's guide - Coming soon!

# Known Issues

Visit the Issue page in this repository for known issues and feature requests.

# Release History

# Contributing

See the [CONTRIBUTING](https://github.com/awslabs/aws-media-insights-engine/blob/master/CONTRIBUTING.md) file for how to contribute.

# License

See the [LICENSE](https://github.com/awslabs/aws-media-insights-engine/blob/master/LICENSE) file for our project's licensing.

Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
