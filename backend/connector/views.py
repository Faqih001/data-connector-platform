from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from .models import DatabaseConnection, StoredFile, ExtractedData
from .serializers import DatabaseConnectionSerializer, StoredFileSerializer, ExtractedDataSerializer
from .services import extract_data_in_batches, json_to_csv
from .permissions import IsFileOwnerOrAdmin, IsFileOwnerOrAdminForWrite
import json
import os
from django.conf import settings
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q

class DatabaseConnectionViewSet(viewsets.ModelViewSet):
    queryset = DatabaseConnection.objects.all()
    serializer_class = DatabaseConnectionSerializer

    @action(detail=True, methods=['post'])
    def extract_data(self, request, pk=None):
        """Extract data with configurable batch_size and format"""
        connection = self.get_object()
        table_name = request.data.get('table_name')
        batch_size = request.data.get('batch_size', 1000)
        format_type = request.data.get('format', 'json')  # 'json' or 'csv'
        
        if not table_name:
            return Response({"error": "table_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if format_type not in ['json', 'csv']:
            return Response({"error": "format must be 'json' or 'csv'"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # In a real app, this would be a background task
            for batch in extract_data_in_batches(connection, table_name, batch_size=batch_size):
                # Store the first batch as a file
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                file_ext = 'csv' if format_type == 'csv' else 'json'
                filename = f"extraction_{connection.name}_{table_name}_{timestamp}.{file_ext}"
                filepath = os.path.join(settings.MEDIA_ROOT, filename)
                
                os.makedirs(os.path.dirname(filepath), exist_ok=True)

                # Save file in requested format
                with open(filepath, 'w') as f:
                    if format_type == 'csv':
                        csv_data = json_to_csv(batch)
                        f.write(csv_data)
                    else:
                        json.dump(batch, f, default=str)

                # Create ExtractedData record (always store JSON in DB)
                extracted_data = ExtractedData.objects.create(
                    connection=connection,
                    data=batch
                )

                # Create StoredFile record linked to ExtractedData
                user = request.user if request.user.is_authenticated else None
                StoredFile.objects.create(
                    user=user,
                    extracted_data=extracted_data,
                    filepath=filepath,
                    format_type=format_type
                )
                return Response({
                    "data": batch,
                    "extracted_data_id": extracted_data.id,
                    "format": format_type,
                    "batch_size": batch_size
                }, status=status.HTTP_200_OK)
            
            return Response({"message": "Extraction complete, but no data found."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StoredFileViewSet(viewsets.ModelViewSet):
    queryset = StoredFile.objects.all()
    serializer_class = StoredFileSerializer

    def get_queryset(self):
        user = self.request.user
        # For unauthenticated users or development, return all files
        if not user.is_authenticated:
            return StoredFile.objects.all()
        # Admin users see all files
        if user.is_staff or (hasattr(user, 'role') and user.role == 'admin'):
            return StoredFile.objects.all()
        # Regular users see their own files + shared files
        return (StoredFile.objects.filter(user=user) | StoredFile.objects.filter(shared_with=user)).distinct()

    @action(detail=True, methods=['post'])
    def submit_data(self, request, pk=None):
        """Submit modified data with DRF validation and model updates"""
        file = self.get_object()
        self.check_object_permissions(request, file)
        
        # Only owner or admin can modify
        is_owner = file.user == request.user
        is_admin = request.user.is_staff or (hasattr(request.user, 'role') and request.user.role == 'admin')
        
        if not (is_owner or is_admin):
            return Response(
                {"error": "❌ Permission denied. You can only modify files you own."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        data = request.data.get('data')

        if not data:
            return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # ✅ Update ExtractedData model with new data
            if file.extracted_data:
                extracted_data = file.extracted_data
                extracted_data.data = data
                extracted_data.save()
                
                # ✅ Validate via serializer
                serializer = ExtractedDataSerializer(extracted_data)
                validated_data = serializer.data
            else:
                # Fallback: create new ExtractedData if not linked
                extracted_data = ExtractedData.objects.create(
                    connection=file.extracted_data.connection if file.extracted_data else None,
                    data=data
                )
                file.extracted_data = extracted_data
                file.save()
                serializer = ExtractedDataSerializer(extracted_data)
                validated_data = serializer.data

            # Save to disk file (backup)
            file_ext = 'csv' if file.format_type == 'csv' else 'json'
            with open(file.filepath, 'w') as f:
                if file.format_type == 'csv':
                    csv_data = json_to_csv(data)
                    f.write(csv_data)
                else:
                    json.dump(data, f, default=str)
            
            # ✅ Return validated data and success
            return Response({
                "message": "✅ Data updated successfully",
                "extracted_data": validated_data,
                "updated_at": extracted_data.updated_at
            }, status=status.HTTP_200_OK)
        
        except ExtractedData.DoesNotExist:
            return Response({"error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download file data as JSON."""
        file = self.get_object()
        
        try:
            if not os.path.exists(file.filepath):
                return Response(
                    {"error": "File not found on disk"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            with open(file.filepath, 'r') as f:
                data = json.load(f)
            
            return Response(data, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON file"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """Share file with other users"""
        try:
            file = self.get_object()
        except Exception as e:
            return Response(
                {"error": f"Failed to get file: {str(e)}"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Only owner or admin can share
        is_owner = file.user == request.user
        is_admin = request.user.is_staff or (hasattr(request.user, 'role') and request.user.role == 'admin')
        
        if not (is_owner or is_admin):
            return Response(
                {"error": f"❌ Permission denied. User: {request.user.username}, is_staff: {request.user.is_staff}, Owner: {file.user}"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_ids = request.data.get('user_ids', [])
        if not user_ids:
            return Response(
                {"error": "user_ids list is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            users = User.objects.filter(id__in=user_ids)
            if users.count() != len(user_ids):
                return Response(
                    {"error": "Some users not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            file.shared_with.add(*users)
            
            # Return updated file with all shared_with users
            from .serializers import StoredFileSerializer
            updated_file = StoredFile.objects.get(id=file.id)
            serializer = StoredFileSerializer(updated_file)
            
            return Response({
                "message": "✅ File shared successfully",
                "file": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def unshare(self, request, pk=None):
        """Revoke file sharing with specific users"""
        file = self.get_object()
        
        # Only owner or admin can unshare
        is_owner = file.user == request.user
        is_admin = request.user.is_staff or (hasattr(request.user, 'role') and request.user.role == 'admin')
        
        if not (is_owner or is_admin):
            return Response(
                {"error": "❌ Permission denied. Only the file owner can modify sharing."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_ids = request.data.get('user_ids', [])
        if not user_ids:
            return Response(
                {"error": "user_ids list is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            users = User.objects.filter(id__in=user_ids)
            file.shared_with.remove(*users)
            
            return Response({
                "message": "✅ File sharing revoked",
                "file_id": file.id,
                "revoked_count": users.count()
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def permissions(self, request, pk=None):
        """Get current access information for a file"""
        file = self.get_object()
        
        # Check if user has access
        is_owner = file.user == request.user
        is_admin = request.user.is_staff or (hasattr(request.user, 'role') and request.user.role == 'admin')
        is_shared = file.shared_with.filter(id=request.user.id).exists()
        
        if not (is_owner or is_admin or is_shared):
            return Response(
                {"error": "❌ Access denied"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        shared_users = [
            {"id": u.id, "username": u.username} 
            for u in file.shared_with.all()
        ]
        
        return Response({
            "file_id": file.id,
            "owner": {
                "id": file.user.id,
                "username": file.user.username
            } if file.user else None,
            "is_owner": is_owner,
            "is_admin": is_admin,
            "is_shared_with_me": is_shared,
            "shared_with": shared_users,
            "can_modify": is_owner or is_admin,
            "can_share": is_owner or is_admin,
            "access_level": "admin" if is_admin else ("owner" if is_owner else ("shared" if is_shared else "none"))
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
def extract_data_endpoint(request):
    """Extract data from a database connection with batch_size and format support."""
    connection_id = request.data.get('connection_id')
    table_name = request.data.get('table_name')
    batch_size = request.data.get('batch_size', 1000)
    format_type = request.data.get('format', 'json')
    
    if not connection_id:
        return Response({"error": "connection_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not table_name:
        return Response({"error": "table_name is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if format_type not in ['json', 'csv']:
        return Response({"error": "format must be 'json' or 'csv'"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        connection = DatabaseConnection.objects.get(id=connection_id)
        
        for batch in extract_data_in_batches(connection, table_name, batch_size=batch_size):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_ext = 'csv' if format_type == 'csv' else 'json'
            filename = f"extraction_{connection.name}_{table_name}_{timestamp}.{file_ext}"
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            # Save file in requested format
            with open(filepath, 'w') as f:
                if format_type == 'csv':
                    csv_data = json_to_csv(batch)
                    f.write(csv_data)
                else:
                    json.dump(batch, f, default=str)

            # Create ExtractedData record
            extracted_data = ExtractedData.objects.create(
                connection=connection,
                data=batch
            )

            # Create StoredFile record linked to ExtractedData
            user = request.user if request.user.is_authenticated else None
            StoredFile.objects.create(
                user=user,
                extracted_data=extracted_data,
                filepath=filepath,
                format_type=format_type
            )
            return Response({
                "data": batch,
                "extracted_data_id": extracted_data.id,
                "format": format_type,
                "batch_size": batch_size
            }, status=status.HTTP_200_OK)
        
        return Response({"message": "Extraction complete, but no data found."}, status=status.HTTP_200_OK)

    except DatabaseConnection.DoesNotExist:
        return Response({"error": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def welcome(request):
    """Welcome page with admin credentials"""
    admin_user = User.objects.filter(is_superuser=True).first()
    context = {
        'admin_username': admin_user.username if admin_user else 'admin',
        'admin_password': 'admin123',
    }
    return render(request, 'welcome.html', context)


@api_view(['POST'])
@csrf_exempt
def login_view(request):
    """Login endpoint for session-based authentication"""
    from django.contrib.auth import authenticate, login
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {"error": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({
            "message": "✅ Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "is_staff": user.is_staff
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "❌ Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@csrf_exempt
def logout_view(request):
    """Logout endpoint"""
    from django.contrib.auth import logout
    
    logout(request)
    return Response(
        {"message": "✅ Logout successful"},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@csrf_exempt
def csrf_token_view(request):
    """Get CSRF token for login"""
    from django.middleware.csrf import get_token
    token = get_token(request)
    return Response({"csrfToken": token}, status=status.HTTP_200_OK)


@api_view(['GET'])
def current_user(request):
    """Get current logged-in user info"""
    if request.user.is_authenticated:
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "is_staff": request.user.is_staff
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Not authenticated"},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
def search_users(request):
    """Search for users by email or username"""
    query = request.query_params.get('q', '').strip()
    
    if not query or len(query) < 2:
        return Response(
            {"error": "Search query must be at least 2 characters"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Search by username or email
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        ).exclude(id=request.user.id).values('id', 'username', 'email')[:10]
        
        return Response({
            "results": list(users)
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
