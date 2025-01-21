# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from base.models import Service, ServicePackage
from base.serializers.packages import (
    ServiceSerializer,
    ServicePackageSerializer,
    ServiceWithPackagesSerializer,
)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ServiceWithPackagesSerializer
        return ServiceSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Check if service with this name already exists
        existing_service = Service.objects.filter(name=request.data["name"]).first()

        if existing_service:
            # Update existing service
            service_serializer = ServiceSerializer(
                existing_service,
                data={
                    "name": request.data["name"],
                    "description": request.data["description"],
                    "base_price": request.data["base_price"],
                    "is_active": request.data["is_active"],
                },
            )
            if service_serializer.is_valid():
                service = service_serializer.save()
            else:
                return Response(
                    service_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Create new service
            service_serializer = ServiceSerializer(data=request.data)
            if service_serializer.is_valid():
                service = service_serializer.save()
            else:
                return Response(
                    service_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        def parse_packages(data):
            """
            Extract packages from the QueryDict and convert them into a usable structure.
            """
            packages = []
            index = 0

            while True:
                # Check if the current package exists
                package_prefix = f"packages[{index}]"
                if not any(key.startswith(package_prefix) for key in data.keys()):
                    break

                # Extract individual package fields
                package = {
                    "name": data.get(f"{package_prefix}[name]"),
                    "package_type": data.get(f"{package_prefix}[package_type]"),
                    "price": data.get(f"{package_prefix}[price]"),
                    "features": data.get(f"{package_prefix}[features]"),
                    "is_active": data.get(f"{package_prefix}[is_active]") == "true",
                }
                packages.append(package)
                index += 1

            return packages

        parsed_data = dict(request.data)
        parsed_data['packages'] = parse_packages(request.data)

        # Handle packages
        if len(parsed_data["packages"])>0:

            for package_data in parsed_data['packages']:
                existing_package = None

                # If package has an ID, try to find it
                if "id" in package_data and isinstance(package_data["id"], int):
                    existing_package = ServicePackage.objects.filter(
                        id=package_data["id"], service=service
                    ).first()

                # If no existing package found by ID, try to find by name
                if not existing_package:
                    existing_package = ServicePackage.objects.filter(
                        name=package_data["name"], service=service
                    ).first()

                # Add service ID to package data
                package_data["service"] = service.id

                if existing_package:
                    # Update existing package
                    package_serializer = ServicePackageSerializer(
                        existing_package, data=package_data
                    )
                else:
                    # Create new package
                    package_serializer = ServicePackageSerializer(data=package_data)

                if package_serializer.is_valid():
                    package_serializer.save()
                else:
                    return Response(
                        package_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

        # Return the complete service with packages
        return Response(
            ServiceWithPackagesSerializer(service).data,
            status=(
                status.HTTP_201_CREATED if not existing_service else status.HTTP_200_OK
            ),
        )

    @action(detail=False, methods=["get"])
    def active(self):
        active_services = Service.objects.filter(is_active=True)
        serializer = self.get_serializer(active_services, many=True)
        return Response(serializer.data)


class ServicePackageViewSet(viewsets.ModelViewSet):
    queryset = ServicePackage.objects.all()
    serializer_class = ServicePackageSerializer

    def create(self, request, *args, **kwargs):
        # Handle nested service creation if service_data is provided
        service_data = request.data.pop("service_data", None)
        print(service_data)
        if service_data:
            service_serializer = ServiceSerializer(data=service_data)
            if service_serializer.is_valid():
                service = service_serializer.save()
                request.data["service"] = service.id
            else:
                return Response(
                    service_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def by_service(self, request):
        service_id = request.query_params.get("service_id")
        if service_id:
            packages = ServicePackage.objects.filter(service_id=service_id)
            serializer = self.get_serializer(packages, many=True)
            return Response(serializer.data)
        return Response(
            {"error": "service_id is required"}, status=status.HTTP_400_BAD_REQUEST
        )
