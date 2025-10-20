from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.views import APIView
from .serializers import CategorySerializers, ProductSerializers
from .models import Category, Product

@api_view(['POST'])
@permission_classes([IsAdminUser]) #  is_authenticated=True  ---->  is_staff=True ---->  ...
def add_category(request):
    serializer = CategorySerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"response": "successful added"})
    else:
        return Response(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAdminUser]) #  is_authenticated=True  ---->  is_staff=True ---->  ...
def read_all_category(request):
    objs_catg = Category.objects.all()
    serializer = CategorySerializers(instance=objs_catg, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAdminUser]) #  is_authenticated=True  ---->  is_staff=True ---->  ...
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
@permission_classes([IsAdminUser]) #  is_authenticated=True  ---->  is_staff=True ---->  ...
def delete_category(request, pk):
    try:
        obj_catg = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"})
    obj_catg.delete()
    return Response({"response": "deleted"})


class ProductAPI(APIView):
    def get_permissions(self):
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get(self, request):
        if request.method == "GET":
            products = Product.objects.all()
            if request.GET.get('category') or request.GET.get('price'):
                if not request.GET.get('category'):
                        products = Product.objects.filter(price=request.GET.get('price'))
                elif not request.GET.get('price'):
                    products = Product.objects.filter(category__name=request.GET.get('category'))
                else:
                    products = Product.objects.filter(category__name=request.GET.get('category'), price=request.GET.get('price'))
            serializer = ProductSerializers(instance=products, many=True)
            return Response(serializer.data)

    @permission_classes([IsAdminUser])
    def post(self, request):
        if request.method == "POST":
            serializer = ProductSerializers(data=request.data)
            if serializer.is_valid():
                print(request.data.get('category'))
                serializer.save()
                return Response({'response': 'added'})
            else:
                return Response(serializer.errors)

    @permission_classes([IsAdminUser])
    def patch(self, request, pk):
        if request.method == "PATCH":
            try:
                product_obj = Product.objects.get(id=pk)
            except Product.DoesNotExist:
                return Response({'error': "Product not found"})
            serializer = ProductSerializers(instance=product_obj, data=request.data, partial=True)
            if request.data.get('category') is not None:
                if serializer.is_valid():
                    serializer.save()
                    return Response({'response': f'{product_obj.name} updated'})
                else:
                    return Response(serializer.errors)
            else:
                return Response({'error': 'You must enter a category.'})

    @permission_classes([IsAdminUser])
    def delete(self, request, pk):
        if request.method == "DELETE":
            try:
                product_obj = Product.objects.get(id=pk)
            except Product.DoesNotExist:
                return Response({'error': "Product not found"})

            product_obj.delete()
            return Response({'response': f'{product_obj.name} deleted'})
