from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.views import APIView
from .serializers import CategorySerializers, ProductSerializers, CartSerializer
from .models import Category, Product, Cart

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

    def get(self, request, name=None):
        products = Product.objects.all()
        if name is not None:
            try:
                product = Product.objects.get(name=name)
                serializer = ProductSerializers(instance=product)
                return Response(serializer.data)
            except Product.DoesNotExist:
                return Response({'error': "Product not found"})
        else:
            if request.GET.get('category') or request.GET.get('price'):
                if not request.GET.get('category'):
                        products = Product.objects.filter(price=request.GET.get('price')).order_by('-created_at')
                elif not request.GET.get('price'):
                    products = Product.objects.filter(category__name=request.GET.get('category')).order_by('-created_at')
                else:
                    products = Product.objects.filter(category__name=request.GET.get('category'), price=request.GET.get('price'))
            serializer = ProductSerializers(instance=products, many=True)
            return Response(serializer.data)

    def post(self, request):
            serializer = ProductSerializers(data=request.data)
            if serializer.is_valid():
                print(request.data.get('category'))
                serializer.save()
                return Response({'response': 'added'})
            else:
                return Response(serializer.errors)

    def patch(self, request, pk):
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

    def delete(self, request, pk):
            try:
                product_obj = Product.objects.get(id=pk)
            except Product.DoesNotExist:
                return Response({'error': "Product not found"})

            product_obj.delete()
            return Response({'response': f'{product_obj.name} deleted'})


class CartAPI(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        var = request.session.session_key
        if Cart.objects.filter(session_key=var).exists():  # exist cart for user???
            pass
        else:
            if not request.session.session_key:  # 1. create session for user if not exist
                request.session.create()
            cart = Cart.objects.create(user=None, session_key=var) # 2. create cart

        cart = Cart.objects.get(session_key=var) # call
        if request.user.is_authenticated:
            cart.user = request.user

        serializer = CartSerializer(instance=cart)
        return Response(serializer.data)
