"""
AWS Bedrock client for LLM generation.
Decoupled from retrieval layer.
"""
import boto3
import json
import logging
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class BedrockClient:
    """AWS Bedrock client for LLM inference."""
    
    def __init__(self):
        self.bedrock_runtime = boto3.client(
            'bedrock-runtime',
            region_name=settings.AWS_REGION
        )
        self.model_id = settings.BEDROCK_MODEL_ID
    
    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate text using AWS Bedrock.
        
        Args:
            prompt: Input prompt text
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional model-specific parameters
        
        Returns:
            Generated text and metadata
        """
        try:
            max_tokens = max_tokens or settings.BEDROCK_MAX_TOKENS
            temperature = temperature or settings.BEDROCK_TEMPERATURE
            
            # Model-specific request formatting
            if "claude" in self.model_id.lower():
                return self._generate_claude(prompt, max_tokens, temperature, **kwargs)
            elif "titan" in self.model_id.lower():
                return self._generate_titan(prompt, max_tokens, temperature, **kwargs)
            elif "llama" in self.model_id.lower():
                return self._generate_llama(prompt, max_tokens, temperature, **kwargs)
            else:
                raise ValueError(f"Unsupported model: {self.model_id}")
                
        except Exception as e:
            logger.error(f"Error generating with Bedrock: {e}")
            raise
    
    def _generate_claude(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate using Claude model."""
        body = {
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "max_tokens_to_sample": max_tokens,
            "temperature": temperature,
            **kwargs
        }
        
        response = self.bedrock_runtime.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        
        return {
            "text": response_body.get("completion", ""),
            "model": self.model_id,
            "stop_reason": response_body.get("stop_reason", "unknown")
        }
    
    def _generate_titan(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate using Amazon Titan model."""
        body = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": max_tokens,
                "temperature": temperature,
                **kwargs
            }
        }
        
        response = self.bedrock_runtime.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        
        return {
            "text": response_body.get("results", [{}])[0].get("outputText", ""),
            "model": self.model_id
        }
    
    def _generate_llama(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate using Llama model."""
        body = {
            "prompt": prompt,
            "max_gen_len": max_tokens,
            "temperature": temperature,
            **kwargs
        }
        
        response = self.bedrock_runtime.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        
        return {
            "text": response_body.get("generation", ""),
            "model": self.model_id
        }
    
    def list_available_models(self) -> list:
        """List available Bedrock models."""
        try:
            bedrock = boto3.client('bedrock', region_name=settings.AWS_REGION)
            response = bedrock.list_foundation_models()
            
            models = [
                model["modelId"]
                for model in response.get("modelSummaries", [])
                if model.get("modelId")
            ]
            
            return models
        except Exception as e:
            logger.error(f"Error listing Bedrock models: {e}")
            return []


# Global instance
bedrock_client = BedrockClient()

