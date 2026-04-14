"""Custom authentication classes for the API"""
import logging
from rest_framework.authentication import SessionAuthentication

logger = logging.getLogger(__name__)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """Session authentication that bypasses CSRF checks for API endpoints"""
    
    def authenticate(self, request):
        """Override authenticate to bypass CSRF checks completely"""
        logger.debug(f"Authenticating request to {request.path}")
        # Call parent authenticate but bypass CSRF using the method below
        return super().authenticate(request)
    
    def enforce_csrf_checks(self, request):
        """Disable CSRF checks for all requests"""
        logger.debug(f"enforce_csrf_checks called for {request.path} - returning False")
        return False
    
    def authenticate_credentials(self, userid):
        """Override to work with DRF"""
        return super().authenticate_credentials(userid)
