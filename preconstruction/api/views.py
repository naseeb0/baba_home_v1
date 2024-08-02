from rest_framework.response import Response
from rest_framework.decorators import api_view
from preconstruction.models import PreConstruction, Developer, City
from preconstruction.api.serializers import PreConstructionSerializer, DeveloperSerializer, CitySerializer


@api_view(['GET', 'POST'])
def preconstruction_list(request):
    if(request.method=='GET'):
        preconstruction = PreConstruction.objects.all()
        serializer = PreConstructionSerializer(preconstruction, many=True)
        return Response(serializer.data)
    if(request.method=='POST'):
        serializer = PreConstructionSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400) 
        
@api_view(['GET', 'PUT', 'DELETE'])
def precon_details(request, pk):
    try:
        preconstruction = PreConstruction.objects.get(pk=pk)
    except PreConstruction.DoesNotExist:
        return Response({'error':"PreConstruction not found"}, status=404)
    if(request.method=='GET'):
        serializer = PreConstructionSerializer(preconstruction)
        return Response(serializer.data)
    if(request.method=='PUT'):
        serializer = PreConstructionSerializer(preconstruction, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    if(request.method=='DELETE'):
        preconstruction.delete()
        return Response(status=204)
@api_view(['GET', 'POST'])
def developer_list(request):
    if(request.method=="GET"):
        developer = Developer.objects.all()
        serializer = DeveloperSerializer(developer, many=True)
        return Response(serializer.data)
    if(request.method=="POST"):
        serializer = DeveloperSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def developer_details(request, pk):
    try:
        developer = Developer.objects.get(pk=pk)
    except Developer.DoesNotExist:
        return Response({'error':"Developer not found"}, status=404)
    if(request.method=='GET'):
        serializer = DeveloperSerializer(developer)
        return Response(serializer.data)
    if(request.method=='PUT'):
        serializer = DeveloperSerializer(developer, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    if(request.method=='DELETE'):
        developer.delete()
        return Response(status=204)
    
@api_view(['GET', 'POST'])
def city_list(request):
    if(request.method=="GET"):
        city = City.objects.all()
        serializer = CitySerializer(city, many=True)
        return Response(serializer.data)
    if(request.method=="POST"):
        serializer = CitySerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def city_details(request, pk):
    try:
        city = City.objects.get(pk=pk)
    except City.DoesNotExist:
        return Response({'error':"City not found"}, status=404)
    if(request.method=='GET'):
        serializer = CitySerializer(city)
        return Response(serializer.data)
    if(request.method=='PUT'):
        serializer = CitySerializer(city, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    if(request.method=='DELETE'):
        city.delete()
        return Response(status=204)