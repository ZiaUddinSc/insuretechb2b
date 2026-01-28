# from django.shortcuts import render
# from rest_framework.views import APIView 
# from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,AllowAny
# from rest_framework.renderers import JSONRenderer,TemplateHTMLRenderer
# from django.http import JsonResponse
# from django.shortcuts import render 
# from rest_framework.viewsets import ModelViewSet
# from rest_framework import serializers
# # from .models import Employee 
# # from .serializers import
# # Create your views here.
# class DashboardView(APIView): 
#     permission_classes = [AllowAny] 
#     renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
#     # def get(self, request, *args, **kwargs): 
#     #     if request.accepted_renderer.format == 'html': 
#     #         context = { 'employees': "Su" } 
#     #         return render(request, 'base.html', context) 
#     #     else: 
#     #         return Response({"success":"test"})
             
#     #         # employees = Employee.objects.all() 
#     #         # serializer = EmployeeSerializer(employees, many=True) 
#     #         # return Response(serializer.data)

#     def get(self, request, *args, **kwargs):
#         # Check for API request by looking at headers
#         # if request.headers.get('Accept') == 'application/json':
#         #     data = {
#         #         "message": "Mobile API response",
#         #         "user": request.user.username,
#         #         "stats": {"sales": 1200, "performance": "Excellent"}
#         #     }
#         #     return Response(data)
#         # return Response({
#         #         "message": "Mobile API response",
#         #         "user": "TST",
#         #         "stats": {"sales": 1200, "performance": "Excellent"}
#         #     })
#         # elif request.accepted_renderer.format == 'html': 
#         #     context = { 'employees': "Su" } 
#         #     return render(request, 'base.html', context) 
#         # Render HTML template for admin dashboard
#         # return render(request, "base.html", {
#         #     "user_data": request.user,
#         #     "stats": {"sales": 1200, "performance": "Excellent"}
#         # })

#         # if request.headers.get('Accept') == 'application/json':
#         #     data = {"user": request.user.username, "stats": {"sales": 1200, "performance": "Excellent"}}
#         #     # serializer = DashboardSerializer(data)
#         #     return JsonResponse(data, safe=False)

#         # return render(request, "base.html", {"user": request.user})

#         # def get(self, request, *args, **kwargs):
#         # Check if it's a mobile API request (JSON response)
#         # data = {
#         #         "message": "Mobile API response",
#         #         "user": request.user.username,
#         #         "stats": {"sales": 1200, "performance": "Excellent"}
#         #     }
#         # if request.headers.get('Accept') == 'application/json':
#         #     data = {
#         #         "message": "Mobile API response",
#         #         "user": request.user.username,
#         #         "stats": {"sales": 1200, "performance": "Excellent"}
#         #     }
#         #     return Response(data)
#         # return Response(data)
#         # Otherwise, render an HTML template for admin dashboard
#         # return render(request, "base.html", context={
#         #     "user_data": request.user,
#         #     "stats": {"sales": 1200, "performance": "Excellent"}
#         # })
#         # content = {'user_count': "ser"}
#         # return Response(content)
#         # queryset = Users.objects.filter(active=True)
#         # if request.accepted_renderer.format == 'html':
#         #     # TemplateHTMLRenderer takes a context dict,
#         #     # and additionally requires a 'template_name'.
#         #     # It does not require serialization.
#         #     data = {'users': 'user'}
#         #     return Response(data, template_name='base.html')

#         #     # JSONRenderer requires serialized data as normal.
#         # # serializer = UserSerializer(instance=queryset)
#         # # data = serializer.data
#         # return Response({"data":"sdaa"})

#     # def get(self, request):
#         # Return JSON data
#         data = {'message': 'Hello, world!'}
#         return Response(data)

#     def render_html(self, request):
#         # Render HTML template
#         template = 'base.html'
#         context = {'message': 'Hello, world!'}
#         return render(request, template, context)
    

# class MyModelViewSet(ModelViewSet):
#     # queryset = MyModel.objects.all()

#     def get_serializer_class(self):
#         if self.request.accepted_media_type == 'application/json':
#             return "MyJSONSerializer"
#         else:
#             return "MyHTMLSerializer"

#     def list(self, request):
#         serializer = self.get_serializer_class()(self.queryset, many=True)
#         return Response({"USER":"serializer.data"})

#     def retrieve(self, request, pk):
#         instance = self.queryset.get(pk=pk)
#         serializer = self.get_serializer_class()(instance)
#         return Response({"USER":"serializer.data"})

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer


class DashboardView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    permission_classes = [IsAuthenticated,AllowAny]
    def get(self, request):
        if request.accepted_renderer.format == 'html':
            # Render HTML template
            return Response({'data': 'Hello, World!'}, template_name='base.html')
        elif self.request.accepted_media_type == 'application/json':
            # Serve JSON data
            return Response({'data': 'Hello, World! and welcome to Home'})
        return Response({'data': 'Hello, World!'})