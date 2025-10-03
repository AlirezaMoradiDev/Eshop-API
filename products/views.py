from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CategorySerializers
from .models import Category

@api_view(['POST'])
def add_category(request):
    serializer = CategorySerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"response": "successful added"})
    else:
        return Response(serializer.errors)


@api_view(['GET'])
def read_all_category(request):
    objs_catg = Category.objects.all()
    serializer = CategorySerializers(instance=objs_catg, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
def update_obj_category(request, pk):
    if request.method == "PUT":
        try:
            obj_catg = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=404)
        serializer = CategorySerializers(data=request.data)
        if serializer.is_valid():
            serializer.update(instance=obj_catg, validated_data=serializer.validated_data)
            return Response({"response": "updated"})
        else:
            return Response(serializer.errors)
    else:
        try:
            obj_catg = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"})
        serializer = CategorySerializers(instance=obj_catg, many=False)
        return Response(serializer.data)


@api_view(['DELETE'])
def delete_category(request, pk):
    try:
        obj_catg = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"})
    obj_catg.delete()
    return Response({"response": "deleted"})