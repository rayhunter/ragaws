"""
AWS S3 client for document storage.
Handles upload, download, and management of original documents.
"""
import boto3
import logging
from typing import Optional, BinaryIO
from botocore.exceptions import ClientError
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger(__name__)


class S3Client:
    """AWS S3 client for document storage operations."""

    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.AWS_S3_BUCKET

        if not self.bucket_name:
            logger.warning("AWS_S3_BUCKET not configured. S3 operations will fail.")

    def upload_document(
        self,
        file_content: bytes,
        document_id: str,
        filename: str,
        content_type: Optional[str] = None
    ) -> str:
        """
        Upload a document to S3.

        Args:
            file_content: Binary content of the file
            document_id: Unique document identifier
            filename: Original filename
            content_type: MIME type of the file

        Returns:
            S3 key (path) where the document was stored

        Raises:
            ValueError: If bucket name is not configured
            ClientError: If S3 upload fails
        """
        if not self.bucket_name:
            raise ValueError("AWS_S3_BUCKET not configured")

        try:
            # Create S3 key with organization structure: documents/{year}/{month}/{doc_id}/{filename}
            now = datetime.utcnow()
            s3_key = f"documents/{now.year}/{now.month:02d}/{document_id}/{filename}"

            # Prepare upload parameters
            upload_params = {
                'Bucket': self.bucket_name,
                'Key': s3_key,
                'Body': file_content,
                'Metadata': {
                    'document_id': document_id,
                    'original_filename': filename,
                    'uploaded_at': now.isoformat()
                }
            }

            # Add content type if provided
            if content_type:
                upload_params['ContentType'] = content_type

            # Upload to S3
            self.s3_client.put_object(**upload_params)

            logger.info(f"Successfully uploaded document to S3: {s3_key}")
            return s3_key

        except ClientError as e:
            logger.error(f"Error uploading document to S3: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error uploading to S3: {e}")
            raise

    def download_document(self, s3_key: str) -> bytes:
        """
        Download a document from S3.

        Args:
            s3_key: S3 key (path) of the document

        Returns:
            Binary content of the file

        Raises:
            ValueError: If bucket name is not configured
            ClientError: If S3 download fails
        """
        if not self.bucket_name:
            raise ValueError("AWS_S3_BUCKET not configured")

        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )

            content = response['Body'].read()
            logger.info(f"Successfully downloaded document from S3: {s3_key}")
            return content

        except ClientError as e:
            logger.error(f"Error downloading document from S3: {e}")
            raise

    def delete_document(self, s3_key: str) -> bool:
        """
        Delete a document from S3.

        Args:
            s3_key: S3 key (path) of the document

        Returns:
            True if deletion was successful

        Raises:
            ValueError: If bucket name is not configured
            ClientError: If S3 deletion fails
        """
        if not self.bucket_name:
            raise ValueError("AWS_S3_BUCKET not configured")

        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )

            logger.info(f"Successfully deleted document from S3: {s3_key}")
            return True

        except ClientError as e:
            logger.error(f"Error deleting document from S3: {e}")
            raise

    def document_exists(self, s3_key: str) -> bool:
        """
        Check if a document exists in S3.

        Args:
            s3_key: S3 key (path) of the document

        Returns:
            True if document exists, False otherwise
        """
        if not self.bucket_name:
            return False

        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                logger.error(f"Error checking document existence in S3: {e}")
                raise

    def get_document_metadata(self, s3_key: str) -> dict:
        """
        Get metadata for a document in S3.

        Args:
            s3_key: S3 key (path) of the document

        Returns:
            Dictionary containing document metadata

        Raises:
            ValueError: If bucket name is not configured
            ClientError: If S3 operation fails
        """
        if not self.bucket_name:
            raise ValueError("AWS_S3_BUCKET not configured")

        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )

            return {
                'size': response.get('ContentLength'),
                'last_modified': response.get('LastModified'),
                'content_type': response.get('ContentType'),
                'metadata': response.get('Metadata', {})
            }

        except ClientError as e:
            logger.error(f"Error getting document metadata from S3: {e}")
            raise

    def generate_presigned_url(
        self,
        s3_key: str,
        expiration: int = 3600
    ) -> str:
        """
        Generate a presigned URL for temporary access to a document.

        Args:
            s3_key: S3 key (path) of the document
            expiration: Time in seconds for the presigned URL to remain valid

        Returns:
            Presigned URL string

        Raises:
            ValueError: If bucket name is not configured
            ClientError: If S3 operation fails
        """
        if not self.bucket_name:
            raise ValueError("AWS_S3_BUCKET not configured")

        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': s3_key
                },
                ExpiresIn=expiration
            )

            logger.info(f"Generated presigned URL for: {s3_key}")
            return url

        except ClientError as e:
            logger.error(f"Error generating presigned URL: {e}")
            raise


# Global instance
s3_client = S3Client()
