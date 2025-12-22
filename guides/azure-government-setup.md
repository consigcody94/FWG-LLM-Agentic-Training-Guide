# Azure Government AI Setup Guide

<div align="center">

**Deploying AI Systems on Azure Government for Federal Workloads**

</div>

---

## Overview

Azure Government is a separate instance of Microsoft Azure designed for U.S. government agencies and their partners. It meets FedRAMP High, DoD IL2/4/5, and other federal compliance requirements.

This guide covers Azure OpenAI Service, Azure AI services, and integration patterns for federal AI deployments.

---

## Prerequisites

- Azure Government subscription
- Azure AD tenant in Azure Government
- Understanding of FedRAMP requirements
- Azure CLI or PowerShell

---

## Part 1: Account Setup

### 1.1 Azure Government Access

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  AZURE GOVERNMENT ACCESS REQUIREMENTS                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  □ U.S. government entity or authorized contractor                        │
│  □ Azure Government subscription provisioned                               │
│  □ Azure AD tenant in Azure Government cloud                              │
│  □ Appropriate RBAC roles assigned                                         │
│                                                                             │
│  REGIONS:                                                                   │
│  • USGov Virginia (usgovvirginia)                                          │
│  • USGov Arizona (usgovarizona)                                            │
│  • USGov Texas (usgovtexas)                                                │
│  • USDoD East/Central (for DoD workloads)                                  │
│                                                                             │
│  PORTAL: https://portal.azure.us                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Azure CLI Configuration

```bash
# Install Azure CLI (if needed)
# https://docs.microsoft.com/cli/azure/install-azure-cli

# Set cloud to Azure Government
az cloud set --name AzureUSGovernment

# Login to Azure Government
az login

# Verify subscription
az account show
```

---

## Part 2: Azure OpenAI Service Setup

### 2.1 Create Azure OpenAI Resource

```bash
# Create resource group
az group create \
  --name rg-ai-workloads \
  --location usgovvirginia

# Create Azure OpenAI resource
az cognitiveservices account create \
  --name myorg-openai \
  --resource-group rg-ai-workloads \
  --kind OpenAI \
  --sku S0 \
  --location usgovvirginia \
  --custom-domain myorg-openai
```

### 2.2 Deploy a Model

```bash
# List available models
az cognitiveservices account deployment list \
  --name myorg-openai \
  --resource-group rg-ai-workloads

# Deploy GPT-4
az cognitiveservices account deployment create \
  --name myorg-openai \
  --resource-group rg-ai-workloads \
  --deployment-name gpt-4-deployment \
  --model-name gpt-4 \
  --model-version "0613" \
  --model-format OpenAI \
  --sku-name "Standard" \
  --sku-capacity 10
```

### 2.3 Available Models (Azure Government)

| Model | Availability | Token Limit | Use Case |
|-------|--------------|-------------|----------|
| GPT-4 | ✅ | 8K/32K | Complex reasoning |
| GPT-4o | ✅ | 128K | General purpose |
| GPT-4o-mini | ✅ | 128K | Cost-effective |
| GPT-3.5-Turbo | ✅ | 16K | Fast responses |
| Text-Embedding-Ada | ✅ | 8K | Embeddings |

---

## Part 3: Python Integration

### 3.1 Basic Usage

```python
"""
Azure Government OpenAI Integration
"""

import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Configure for Azure Government
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    # e.g., "https://myorg-openai.openai.azure.us/"
)

def chat_completion(prompt: str, system_prompt: str = None) -> str:
    """
    Get chat completion from Azure OpenAI in Government cloud.
    """
    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4-deployment",  # Your deployment name
        messages=messages,
        max_tokens=1000,
        temperature=0.7
    )

    return response.choices[0].message.content


def streaming_completion(prompt: str):
    """
    Stream responses from Azure OpenAI.
    """
    stream = client.chat.completions.create(
        model="gpt-4-deployment",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


# Embeddings
def get_embedding(text: str) -> list:
    """
    Generate embeddings using Azure OpenAI.
    """
    response = client.embeddings.create(
        model="text-embedding-ada-002",  # Your embedding deployment
        input=text
    )
    return response.data[0].embedding


if __name__ == "__main__":
    response = chat_completion(
        "Explain FedRAMP in simple terms.",
        system_prompt="You are a helpful federal compliance assistant."
    )
    print(response)
```

### 3.2 With LangChain

```python
"""
LangChain with Azure Government OpenAI
"""

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain.schema import HumanMessage, SystemMessage
import os

# Chat model
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_deployment="gpt-4-deployment",
    temperature=0.7
)

# Embeddings
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_deployment="text-embedding-ada-002"
)

# Example usage
messages = [
    SystemMessage(content="You are a federal compliance expert."),
    HumanMessage(content="What are the key FedRAMP requirements?")
]

response = llm.invoke(messages)
print(response.content)
```

---

## Part 4: Network Security

### 4.1 Private Endpoint Configuration

```bash
# Create private endpoint for Azure OpenAI
az network private-endpoint create \
  --name pe-openai \
  --resource-group rg-ai-workloads \
  --vnet-name vnet-ai \
  --subnet subnet-private \
  --private-connection-resource-id $(az cognitiveservices account show \
    --name myorg-openai \
    --resource-group rg-ai-workloads \
    --query id -o tsv) \
  --group-id account \
  --connection-name openai-connection
```

### 4.2 Network Security Group Rules

```json
{
  "securityRules": [
    {
      "name": "AllowOpenAIPrivate",
      "properties": {
        "priority": 100,
        "direction": "Outbound",
        "access": "Allow",
        "protocol": "Tcp",
        "sourcePortRange": "*",
        "destinationPortRange": "443",
        "sourceAddressPrefix": "VirtualNetwork",
        "destinationAddressPrefix": "AzureCloud.usgovvirginia"
      }
    },
    {
      "name": "DenyInternet",
      "properties": {
        "priority": 4096,
        "direction": "Outbound",
        "access": "Deny",
        "protocol": "*",
        "sourcePortRange": "*",
        "destinationPortRange": "*",
        "sourceAddressPrefix": "*",
        "destinationAddressPrefix": "Internet"
      }
    }
  ]
}
```

### 4.3 Disable Public Access

```bash
# Disable public network access
az cognitiveservices account update \
  --name myorg-openai \
  --resource-group rg-ai-workloads \
  --public-network-access Disabled
```

---

## Part 5: Security & Compliance

### 5.1 Managed Identity

```python
"""
Using Managed Identity (no API keys in code)
"""

from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI

# Use managed identity
credential = DefaultAzureCredential()
token = credential.get_token("https://cognitiveservices.azure.us/.default")

client = AzureOpenAI(
    azure_endpoint="https://myorg-openai.openai.azure.us/",
    api_version="2024-02-01",
    azure_ad_token=token.token
)

# Now use client as normal - no API key needed!
```

### 5.2 Key Vault Integration

```bash
# Store API key in Key Vault
az keyvault secret set \
  --vault-name kv-ai-secrets \
  --name "OpenAI-API-Key" \
  --value "<your-api-key>"

# Grant access to application
az keyvault set-policy \
  --name kv-ai-secrets \
  --object-id <app-object-id> \
  --secret-permissions get
```

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Retrieve key from Key Vault
credential = DefaultAzureCredential()
client = SecretClient(
    vault_url="https://kv-ai-secrets.vault.usgovcloudapi.net/",
    credential=credential
)

api_key = client.get_secret("OpenAI-API-Key").value
```

### 5.3 Diagnostic Logging

```bash
# Enable diagnostic logs
az monitor diagnostic-settings create \
  --name "ai-diagnostics" \
  --resource $(az cognitiveservices account show \
    --name myorg-openai \
    --resource-group rg-ai-workloads \
    --query id -o tsv) \
  --logs '[
    {"category": "Audit", "enabled": true, "retentionPolicy": {"days": 365, "enabled": true}},
    {"category": "RequestResponse", "enabled": true, "retentionPolicy": {"days": 90, "enabled": true}}
  ]' \
  --workspace $(az monitor log-analytics workspace show \
    --workspace-name law-ai-logs \
    --resource-group rg-ai-workloads \
    --query id -o tsv)
```

---

## Part 6: Content Filtering

### 6.1 Default Filters

Azure OpenAI includes content filtering by default:

| Category | Severity Levels | Default Action |
|----------|-----------------|----------------|
| Hate | Low, Medium, High | Block Medium+ |
| Sexual | Low, Medium, High | Block Medium+ |
| Violence | Low, Medium, High | Block Medium+ |
| Self-harm | Low, Medium, High | Block Medium+ |

### 6.2 Custom Content Filter

```bash
# Create custom content filter policy
az cognitiveservices account create-filter \
  --name myorg-openai \
  --resource-group rg-ai-workloads \
  --filter-name "strict-filter" \
  --hate-severity-threshold "low" \
  --sexual-severity-threshold "low" \
  --violence-severity-threshold "medium" \
  --self-harm-severity-threshold "low"
```

---

## Part 7: Cost Management

### 7.1 Set Spending Limits

```bash
# Create budget alert
az consumption budget create \
  --budget-name "AI-Services-Budget" \
  --amount 5000 \
  --time-grain Monthly \
  --start-date 2025-01-01 \
  --end-date 2025-12-31 \
  --resource-group rg-ai-workloads
```

### 7.2 Token Monitoring

```python
def log_token_usage(response):
    """
    Log token usage for cost tracking.
    """
    usage = response.usage
    print(f"Prompt tokens: {usage.prompt_tokens}")
    print(f"Completion tokens: {usage.completion_tokens}")
    print(f"Total tokens: {usage.total_tokens}")

    # Estimate cost (adjust rates for current pricing)
    input_cost = (usage.prompt_tokens / 1000) * 0.03  # GPT-4 rates
    output_cost = (usage.completion_tokens / 1000) * 0.06
    print(f"Estimated cost: ${input_cost + output_cost:.4f}")
```

---

## Part 8: Compliance Checklist

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  AZURE GOVERNMENT AI COMPLIANCE CHECKLIST                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  □ FedRAMP Authorization                                                   │
│    □ Azure Government is FedRAMP High authorized                          │
│    □ Azure OpenAI inherits authorization                                   │
│    □ Customer responsibilities documented                                  │
│                                                                             │
│  □ Identity & Access                                                       │
│    □ Azure AD in Government cloud                                          │
│    □ Conditional Access policies configured                                │
│    □ MFA enforced for all users                                            │
│    □ Privileged Identity Management enabled                                │
│                                                                             │
│  □ Data Protection                                                         │
│    □ Private endpoints configured                                          │
│    □ Public access disabled                                                │
│    □ Customer-managed keys (optional)                                      │
│    □ Data residency in US confirmed                                        │
│                                                                             │
│  □ Monitoring & Audit                                                      │
│    □ Diagnostic logging enabled                                            │
│    □ Log Analytics workspace configured                                    │
│    □ Activity logs retained                                                │
│    □ Azure Defender enabled                                                │
│                                                                             │
│  □ Content Safety                                                          │
│    □ Content filtering enabled                                             │
│    □ Abuse monitoring active                                               │
│    □ Rate limits configured                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Troubleshooting

**Issue: DeploymentNotFound**
```bash
# List deployments
az cognitiveservices account deployment list \
  --name myorg-openai \
  --resource-group rg-ai-workloads \
  --output table

# Verify deployment name matches code
```

**Issue: PrivateEndpointNotConfigured**
```bash
# Check private endpoint status
az network private-endpoint show \
  --name pe-openai \
  --resource-group rg-ai-workloads

# Verify DNS resolution
nslookup myorg-openai.openai.azure.us
```

---

## Resources

- [Azure Government Documentation](https://docs.microsoft.com/azure/azure-government/)
- [Azure OpenAI Service](https://docs.microsoft.com/azure/cognitive-services/openai/)
- [Azure Government Compliance](https://docs.microsoft.com/azure/azure-government/compliance/)

---

<div align="center">

**Deploy with confidence in Azure Government**

</div>
