# shared_code/secret_loader.py

import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import logging

logger = logging.getLogger(__name__)

def load_secrets():
    """Load secrets from Azure Key Vault and set them as environment variables."""
    try:
        # Get the Key Vault URL from environment variables
        key_vault_url = os.environ.get('AZURE_KEY_VAULT_URL')

        if not key_vault_url:
            raise Exception("Key Vault URL not found. Please set the AZURE_KEY_VAULT_URL environment variable.")

        # Authenticate using DefaultAzureCredential
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_url, credential=credential)

        # List of secrets to load
        secrets = ['OPENAI_API_KEY', 'SMTP_USERNAME', 'SMTP_PASSWORD', 'SMTP_SERVER', 'SMTP_PORT']

        for secret_id in secrets:
            secret = client.get_secret(secret_id)
            os.environ[secret_id] = secret.value
            logger.debug(f"Loaded secret: {secret_id}")

    except Exception as e:
        logger.error(f"Error loading secrets: {e}")

