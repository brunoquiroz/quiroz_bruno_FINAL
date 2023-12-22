from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.parsers import JSONParser
from .models import Inscrito, Institucion
from .serializers import InscritoSerializer, InstitucionSerializer

class InscritoListCreateView(generics.ListCreateAPIView):
    queryset = Inscrito.objects.all()
    serializer_class = InscritoSerializer

class InscritoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inscrito.objects.all()
    serializer_class = InscritoSerializer

class InstitucionListCreateView(generics.ListCreateAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer

class InstitucionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer

# Function Based Views
@csrf_exempt
def inscrito_list(request):
    if request.method == 'GET':
        inscritos = Inscrito.objects.all()
        serializer = InscritoSerializer(inscritos, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = InscritoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def inscrito_detail(request, pk):
    try:
        inscrito = Inscrito.objects.get(pk=pk)
    except Inscrito.DoesNotExist:
        return JsonResponse({'error': 'Inscrito not found'}, status=404)

    if request.method == 'GET':
        serializer = InscritoSerializer(inscrito)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = InscritoSerializer(inscrito, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        inscrito.delete()
        return JsonResponse({'message': 'Inscrito deleted successfully'}, status=204)

@csrf_exempt
def institucion_list(request):
    if request.method == 'GET':
        instituciones = Institucion.objects.all()
        serializer = InstitucionSerializer(instituciones, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = InstitucionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def institucion_detail(request, pk):
    try:
        institucion = Institucion.objects.get(pk=pk)
    except Institucion.DoesNotExist:
        return JsonResponse({'error': 'Institucion not found'}, status=404)

    if request.method == 'GET':
        serializer = InstitucionSerializer(institucion)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = InstitucionSerializer(institucion, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        institucion.delete()
        return JsonResponse({'message': 'Institucion deleted successfully'}, status=204)
    
class InscritoSearchView(View):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        inscrito_id = request.POST.get('id_persona') 
        if inscrito_id:
            try:
                inscrito = Inscrito.objects.get(id_persona=inscrito_id)  
                serializer = InscritoSerializer(inscrito)
                return JsonResponse(serializer.data)
            except Inscrito.DoesNotExist:
                return JsonResponse({'error': 'Inscrito not found'}, status=404)
        else:
            return JsonResponse({'error': 'ID parameter is required'}, status=400)

class InstitucionSearchView(View):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        institucion_id = request.POST.get('id')  
        if institucion_id:
            try:
                institucion = Institucion.objects.get(id=institucion_id)
                serializer = InstitucionSerializer(institucion)
                return JsonResponse(serializer.data)
            except Institucion.DoesNotExist:
                return JsonResponse({'error': 'Institucion not found'}, status=404)
        else:
            return JsonResponse({'error': 'ID parameter is required'}, status=400)

class SearchView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'inscrito_result': None, 'institucion_result': None})

    def post(self, request, *args, **kwargs):
        inscrito_id = request.POST.get('id_persona')
        institucion_id = request.POST.get('id_institucion')

        inscrito_result = None
        institucion_result = None

        if inscrito_id:
            try:
                inscrito = Inscrito.objects.get(id_persona=inscrito_id)
                serializer = InscritoSerializer(inscrito)
                inscrito_result = {
                    'inscrito': serializer.data,
                    'institucion': {
                        'nombre': inscrito.institucion.nombre,
                    }
                }
            except Inscrito.DoesNotExist:
                inscrito_result = {'error': 'Inscrito not found'}

        elif institucion_id:
            try:
                institucion = Institucion.objects.get(id=institucion_id)
                serializer = InstitucionSerializer(institucion)
                institucion_result = {'institucion': serializer.data}
            except Institucion.DoesNotExist:
                institucion_result = {'error': 'Institucion not found'}

        return render(request, self.template_name, {'inscrito_result': inscrito_result, 'institucion_result': institucion_result})


def index(request):
    return render(request, 'index.html')