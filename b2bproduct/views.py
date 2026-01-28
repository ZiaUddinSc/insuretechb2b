from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, status,permissions
from rest_framework.views import APIView
from .models import Product,Policy
from .serializers import ProductSerializer,PolicySerializer,PolicyListSerializer
from rest_framework.authentication import TokenAuthentication

from django.db.models import Q
from django.http import JsonResponse
# Create your views here.

class BasicPagination(PageNumberPagination):
    page_size_query_param = 10

def life(request):
    template_name = 'b2bproduct/life-list.html'
    return render(request,template_name=template_name)

def IPDHospitalizationCoverage(request):
    template_name = 'b2bproduct/IPD-hospitalization-coverage.html'
    return render(request,template_name=template_name)

def OPDCoverage(request):
    template_name = 'b2bproduct/OPD-coverage-list.html'
    return render(request,template_name=template_name)

def criticalIllness(request):
    template_name = 'b2bproduct/critical-Illness-list.html'
    return render(request,template_name=template_name)

def maternityCoverage(request):
    template_name = 'b2bproduct/maternity-coverage-list.html'
    return render(request,template_name=template_name)

def createB2bProduct(request):
    template_name = 'b2bproduct/create-b2b-product.html'
    return render(request,template_name=template_name)

def createPlan1(request):
    template_name = 'b2bproduct/plan1.html'
    return render(request,template_name=template_name)

def ClaimDashboard(request):
    template_name = 'b2bproduct/claim-dashboard.html'
    return render(request,template_name=template_name)

def CreateClaim(request):
    template_name = 'b2bproduct/create-claim.html'
    return render(request,template_name=template_name)

def ProductListView(request):
    template_name = 'b2bproduct/product-list.html'
    return render(request, template_name=template_name)



def TableTemp(request):
    template_name = 'b2bproduct/table-temp.html'
    return render(request, template_name=template_name)

def GroupeClaim(request):
    template_name = 'b2bproduct/group-claim.html'
    return render(request, template_name=template_name)

def MyFamily(request):
    template_name = 'b2bproduct/my-family.html'
    return render(request, template_name=template_name)







def getProductList(request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        queryset=Product.objects.all().order_by('-id')      
        # Grabing data with Search value        
        if search_value:
            queryset =  queryset.filter(
                Q(name__icontains=search_value)
            )
        # counting All records           
        total_records = Product.objects.count()
        #Count Filetred Data
        filtered_records = queryset.count()
        # Range query data
        products=queryset[start:start+length]
        #Paginate Query data
        # Serilization by Data        
        serializer =ProductSerializer(products, many=True)
        # Response Data
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': serializer.data
        })

class ProductListAPIView(APIView,PageNumberPagination):
    queryset = Product.objects.all()
    authentication_classes = [TokenAuthentication]  
    pagination_class = BasicPagination
    serializer_class =ProductSerializer
    def get(self, request):
        try:
            bank = Product.objects.all() #Sertalize single item
            serializer = ProductSerializer(bank,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
            
    
class ProductView(APIView,PageNumberPagination):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class =ProductSerializer
    def get(self, request):
        try:
            bank = Product.objects.all() #Sertalize single item
            serializer = ProductSerializer(bank,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        # Request Data
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({'success':True,"message":'Product has been saved',"data":serializer.data})
        else:           
            return Response({'success':False,"message":'Product has not been saved',"data":serializer.errors})

    def put(self, request, pk):
        try:
            product = Product.objects.get(id=pk) 
        except Product.DeesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data) 
        if serializer.is_valid():
            product = serializer.save(updated_by=request.user)
            return Response({
                "message": "Product has been updated",
                "success":True,
                "data":serializer.data
                })  
        return Response({
            "message": "Product didn't update",
            "success":False,
            "data":serializer.errors
            })


    def delete(self, request, pk):
        try:
          #Retrieve Iten by ID
          product = Product.objects.get(id=pk)

        except Product.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        #Delete the organization from the database 
        product.delete()
        #Return a 284 response
        return Response({"error": False,"message":'Product has been deleted'})
    
class ProductViewSigleList(APIView):
    def get(self, request,item_id):
        try:
            #Query a single tee by ID
            product = Product.objects.get(id=item_id) #Sertalize single item
            serializer =ProductSerializer(product)
            return Response({"success":True,"data":serializer.data}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
                return Response({"success":False,"error": "Product not found"},status=status.HTTP_404_NOT_FOUND)

# Policy Type

def PolicytListView(request):
    products=Product.objects.all()
    template_name = 'b2bproduct/policy-list.html'
    return render(request, template_name=template_name,context={"products":products})


def getPolicyList(request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        queryset=Policy.objects.all().order_by('-id')      
        # Grabing data with Search value        
        if search_value:
            queryset =  queryset.filter(
                Q(name__icontains=search_value)
            )
        # counting All records           
        total_records = Policy.objects.count()
        #Count Filetred Data
        filtered_records = queryset.count()
        # Range query data
        policies=queryset[start:start+length]
        #Paginate Query data
        # Serilization by Data        
        serializer =PolicyListSerializer(policies, many=True)
        # Response Data
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': serializer.data
        })
        
    
class PolicyView(APIView,PageNumberPagination):
    queryset = Policy.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class =PolicySerializer
    def get(self, request):
        try:
            policy = Policy.objects.all() #Sertalize single item
            serializer = PolicySerializer(policy,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Policy.DoesNotExist:
            return Response({"success":False,"error": "Policy not found"},status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        # Request Data
        serializer = PolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({'success':True,"message":'Policy has been saved',"data":serializer.data})
        else:           
            return Response({'success':False,"message":'Policy has not been saved',"data":serializer.errors})

    def put(self, request, pk):
        try:
            policy = Policy.objects.get(id=pk) 
        except Product.DeesNotExist:
            return Response({"error": "Policy not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PolicySerializer(policy, data=request.data) 
        if serializer.is_valid():
            policy = serializer.save(updated_by=request.user)
            return Response({
                "message": "Policy has been updated",
                "success":True,
                "data":serializer.data
                })  
        return Response({
            "message": "Policy didn't update",
            "success":False,
            "data":serializer.errors
            })


    def delete(self, request, pk):
        try:
          #Retrieve Iten by ID
          policy = Policy.objects.get(id=pk)

        except Policy.DoesNotExist:
            return Response({"error": "Policy not found"}, status=status.HTTP_404_NOT_FOUND)

        #Delete the organization from the database 
        policy.delete()
        #Return a 284 response
        return Response({"error": False,"message":'Policy has been deleted'})
    
class PolicyViewSigleList(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [TokenAuthentication] 
    def get(self, request):
        try:
            #Query a single tee by ID
            policices = Policy.objects.all() #Sertalize single item
            item_id = request.GET.get('item_id',False)
            serializer=[]
            product_id = request.GET.get('product_id',False)
            if item_id:
                policy =   policices.get(id=item_id)
                serializer =PolicyListSerializer(policy)
            if product_id:
                policices = policices.filter(product_id=product_id).order_by('id')
                serializer =PolicyListSerializer(policices,many=True)
            if serializer:
                return Response({"success":True,"data":serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"success":False,"error": "Policy not found"},status=status.HTTP_404_NOT_FOUND)
        except Policy.DoesNotExist:
                return Response({"success":False,"error": "Policy not found"},status=status.HTTP_404_NOT_FOUND)




    
class BenifitViewBuClaim(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication] 
    def get(self, request):
        try:
            #Query a single tee by ID
            policices = Policy.objects.all() #Sertalize single item
            item_id = request.GET.get('item_id',False)
            serializer=[]
            product_id = request.GET.get('product_id',False)
            if item_id:
                policy =   policices.get(id=item_id)
                serializer =PolicyListSerializer(policy)
            if product_id:
                policices = policices.filter(product_id=product_id).order_by('id')
                serializer =PolicyListSerializer(policices,many=True)
            if serializer:
                return Response({"success":True,"data":serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"success":False,"error": "Policy not found"},status=status.HTTP_404_NOT_FOUND)
        except Policy.DoesNotExist:
                return Response({"success":False,"error": "Policy not found"},status=status.HTTP_404_NOT_FOUND)





