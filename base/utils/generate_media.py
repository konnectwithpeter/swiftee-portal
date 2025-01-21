from django.core.signing import Signer, BadSignature
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
import os

def generate_temporary_file_url(document, expires_in=300):  # expires_in is in seconds (5 minutes default)
    signer = Signer()
    signature = signer.sign(f"{document.id}:{expires_in}")
    return f"/api/documents/{document.id}/secure-download/{urlsafe_base64_encode(signature.encode())}"
