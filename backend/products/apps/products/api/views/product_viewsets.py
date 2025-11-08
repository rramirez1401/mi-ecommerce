from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from apps.products.api.serializers.product_serializers import ProductSerializer



class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    
    def get_queryset(self,pk=None):
        model = self.serializer_class.Meta.model
        if pk is None:
            return model.objects.filter(state=True)
        return model.objects.filter(id=pk,state=True).first()
    
    def list(self,request,*args, **kwargs):
        serialized_list = self.get_serializer(self.get_queryset(),many=True)
        return Response(serialized_list.data, status=status.HTTP_200_OK)


    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(
            {'message':'Producto creado correctamente',
             'data':self.get_serializer(product).data},
            status=status.HTTP_201_CREATED
            )


    def destroy(self,request,*args, **kwargs):
        pk = kwargs.get('pk')
        product = get_object_or_404(self.get_queryset(), id=pk)
        product.state = False
        product.deleted_date = timezone.now()
        product.save()
        return Response({'message':'Producto eliminado correctamente'},status=status.HTTP_200_OK)

    def update(self,request,*args, **kwargs):
        pk = kwargs.get('pk')
        product = get_object_or_404(self.get_queryset(),id=pk)
        serializer = self.get_serializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_product = serializer.save()
        return Response(
            {'message':'Producto actualizado correctamente',
             'data':self.get_serializer(updated_product).data},
            status=status.HTTP_200_OK 
            )










    


    