# AWS GovCloud AI Setup Guide

<div align="center">

**Deploying AI Systems on AWS GovCloud for Federal Workloads**

</div>

---

## Overview

AWS GovCloud (US) is an isolated AWS region designed to host sensitive data and regulated workloads, including FedRAMP High and DoD Impact Level 4/5 requirements.

This guide covers setting up AI services including Amazon Bedrock, SageMaker, and integration with external LLM providers.

---

## Prerequisites

- AWS GovCloud account (requires vetting process)
- IAM permissions for AI services
- Understanding of FedRAMP requirements
- VPC and networking basics

---

## Part 1: Account Setup

### 1.1 GovCloud Account Access

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  AWS GOVCLOUD ACCESS REQUIREMENTS                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  □ U.S. citizenship or legal permanent residency verification              │
│  □ Company registration and validation                                     │
│  □ Compliance attestation signed                                           │
│  □ GovCloud-specific IAM users (not linked to commercial AWS)             │
│                                                                             │
│  REGIONS:                                                                   │
│  • us-gov-west-1 (Oregon)                                                  │
│  • us-gov-east-1 (Ohio)                                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 IAM Configuration

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "BedrockAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:GetFoundationModel",
        "bedrock:ListFoundationModels"
      ],
      "Resource": "*"
    },
    {
      "Sid": "SageMakerEndpoint",
      "Effect": "Allow",
      "Action": [
        "sagemaker:InvokeEndpoint",
        "sagemaker:DescribeEndpoint"
      ],
      "Resource": "arn:aws-us-gov:sagemaker:*:*:endpoint/*"
    }
  ]
}
```

---

## Part 2: Amazon Bedrock Setup

### 2.1 Enable Bedrock Access

```bash
# AWS CLI configuration for GovCloud
aws configure

# Set GovCloud region
export AWS_DEFAULT_REGION=us-gov-west-1

# List available foundation models
aws bedrock list-foundation-models \
  --region us-gov-west-1 \
  --output table
```

### 2.2 Available Models (GovCloud)

| Model | Provider | Availability | Use Case |
|-------|----------|--------------|----------|
| Claude 3 | Anthropic | ✅ Available | General, Code, Analysis |
| Claude 3.5 | Anthropic | ✅ Available | Advanced reasoning |
| Titan Text | Amazon | ✅ Available | General purpose |
| Titan Embeddings | Amazon | ✅ Available | Vector search |
| Llama 2 | Meta | ✅ Available | Open source option |

### 2.3 Python Integration

```python
"""
AWS GovCloud Bedrock Integration
"""

import boto3
import json

# Configure for GovCloud
session = boto3.Session(
    region_name='us-gov-west-1',
    profile_name='govcloud'  # Your GovCloud profile
)

bedrock_runtime = session.client('bedrock-runtime')

def invoke_claude(prompt: str, max_tokens: int = 1000) -> str:
    """
    Invoke Claude on AWS GovCloud Bedrock.
    """
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    response = bedrock_runtime.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=body,
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']

def invoke_claude_streaming(prompt: str):
    """
    Streaming response from Claude on GovCloud.
    """
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    })

    response = bedrock_runtime.invoke_model_with_response_stream(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=body,
        contentType="application/json"
    )

    for event in response['body']:
        chunk = json.loads(event['chunk']['bytes'].decode())
        if chunk['type'] == 'content_block_delta':
            yield chunk['delta'].get('text', '')


# Example usage
if __name__ == "__main__":
    response = invoke_claude("Explain FedRAMP compliance in 3 sentences.")
    print(response)
```

---

## Part 3: Network Configuration

### 3.1 VPC Setup for AI Workloads

```yaml
# CloudFormation template for AI VPC
AWSTemplateFormatVersion: '2010-09-09'
Description: VPC for AI workloads in GovCloud

Resources:
  AIVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: ai-workload-vpc

  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref AIVPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      Tags:
        - Key: Name
          Value: ai-private-subnet-1

  BedrockEndpoint:
    Type: AWS::EC2::VPCEndpoint
    Properties:
      VpcId: !Ref AIVPC
      ServiceName: !Sub com.amazonaws.${AWS::Region}.bedrock-runtime
      VpcEndpointType: Interface
      SubnetIds:
        - !Ref PrivateSubnet1
      SecurityGroupIds:
        - !Ref BedrockSecurityGroup

  BedrockSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for Bedrock endpoint
      VpcId: !Ref AIVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 10.0.0.0/16
```

### 3.2 VPC Endpoints for Private Access

```bash
# Create VPC endpoint for Bedrock (no internet required)
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-12345678 \
  --service-name com.amazonaws.us-gov-west-1.bedrock-runtime \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-12345678 \
  --security-group-ids sg-12345678 \
  --region us-gov-west-1
```

---

## Part 4: Security Configuration

### 4.1 KMS Encryption

```bash
# Create CMK for AI data encryption
aws kms create-key \
  --description "AI Workload Encryption Key" \
  --key-usage ENCRYPT_DECRYPT \
  --region us-gov-west-1

# Create alias
aws kms create-alias \
  --alias-name alias/ai-workload-key \
  --target-key-id <key-id> \
  --region us-gov-west-1
```

### 4.2 CloudTrail Logging

```json
{
  "TrailName": "ai-audit-trail",
  "S3BucketName": "ai-audit-logs-bucket",
  "IncludeGlobalServiceEvents": true,
  "IsMultiRegionTrail": false,
  "EnableLogFileValidation": true,
  "EventSelectors": [
    {
      "ReadWriteType": "All",
      "IncludeManagementEvents": true,
      "DataResources": [
        {
          "Type": "AWS::Bedrock::Model",
          "Values": ["arn:aws-us-gov:bedrock:*:*:model/*"]
        }
      ]
    }
  ]
}
```

### 4.3 Service Control Policies

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNonGovCloudRegions",
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": [
            "us-gov-west-1",
            "us-gov-east-1"
          ]
        }
      }
    },
    {
      "Sid": "RequireEncryption",
      "Effect": "Deny",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": "*",
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

---

## Part 5: Cost Management

### 5.1 Budget Alerts

```bash
# Create budget for AI services
aws budgets create-budget \
  --account-id 123456789012 \
  --budget '{
    "BudgetName": "AI-Services-Monthly",
    "BudgetLimit": {"Amount": "5000", "Unit": "USD"},
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST",
    "CostFilters": {
      "Service": ["Amazon Bedrock", "Amazon SageMaker"]
    }
  }' \
  --notifications-with-subscribers '[
    {
      "Notification": {
        "NotificationType": "ACTUAL",
        "ComparisonOperator": "GREATER_THAN",
        "Threshold": 80
      },
      "Subscribers": [{"SubscriptionType": "EMAIL", "Address": "admin@agency.gov"}]
    }
  ]' \
  --region us-gov-west-1
```

### 5.2 Cost Estimation

| Service | Unit | Approx. Cost (GovCloud) |
|---------|------|-------------------------|
| Claude 3 Sonnet | 1M input tokens | $3.00 |
| Claude 3 Sonnet | 1M output tokens | $15.00 |
| Titan Text | 1M input tokens | $0.30 |
| Titan Embeddings | 1M tokens | $0.10 |
| SageMaker Endpoint | ml.g5.xlarge/hr | $1.50 |

---

## Part 6: Compliance Checklist

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  AWS GOVCLOUD AI COMPLIANCE CHECKLIST                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  □ FedRAMP Authorization                                                   │
│    □ AWS GovCloud is FedRAMP High authorized                              │
│    □ Bedrock inherits GovCloud authorization                               │
│    □ Customer responsibility matrix reviewed                               │
│                                                                             │
│  □ Data Protection                                                         │
│    □ Data classification completed                                         │
│    □ Encryption at rest enabled (KMS)                                      │
│    □ Encryption in transit (TLS 1.2+)                                      │
│    □ VPC endpoints for private access                                      │
│                                                                             │
│  □ Access Control                                                          │
│    □ IAM roles with least privilege                                        │
│    □ MFA required for console access                                       │
│    □ Service accounts use roles (not keys)                                 │
│    □ Regular access reviews scheduled                                      │
│                                                                             │
│  □ Audit & Monitoring                                                      │
│    □ CloudTrail enabled for all API calls                                  │
│    □ CloudWatch logs configured                                            │
│    □ GuardDuty enabled                                                     │
│    □ Log retention meets requirements                                       │
│                                                                             │
│  □ Network Security                                                        │
│    □ VPC with private subnets                                              │
│    □ Security groups properly scoped                                       │
│    □ No public endpoints for AI services                                   │
│    □ VPC flow logs enabled                                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Troubleshooting

### Common Issues

**Issue: AccessDeniedException for Bedrock**
```bash
# Check model access is enabled
aws bedrock list-foundation-models --region us-gov-west-1

# Request model access if needed (some require approval)
aws bedrock put-model-access \
  --model-identifier anthropic.claude-3-sonnet-20240229-v1:0 \
  --region us-gov-west-1
```

**Issue: VPC Endpoint Not Resolving**
```bash
# Verify endpoint DNS
aws ec2 describe-vpc-endpoints \
  --filters Name=service-name,Values=com.amazonaws.us-gov-west-1.bedrock-runtime \
  --region us-gov-west-1

# Check DNS resolution from EC2 instance
nslookup bedrock-runtime.us-gov-west-1.amazonaws.com
```

---

## Resources

- [AWS GovCloud Documentation](https://docs.aws.amazon.com/govcloud-us/)
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/)
- [FedRAMP Marketplace - AWS](https://marketplace.fedramp.gov/)

---

<div align="center">

**Deploy with confidence in AWS GovCloud**

</div>
