import requests
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse

API_BASE_URL = "https://api.mercadopublico.cl/servicios/v1/publico/"
TICKET = "F8537A18-6766-4DEF-9E59-426B4FEE2844"  # Ticket de prueba

def list_licitaciones(request):
    url = f"{API_BASE_URL}licitaciones.json?ticket={TICKET}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get('Listado', [])
        if not data:
            return render(request, 'licitaciones.html', {'no_data': True})
    except requests.exceptions.HTTPError as http_err:
        return HttpResponse(f"HTTP error occurred: {http_err}. URL: {url}", status=response.status_code)
    except requests.exceptions.RequestException as err:
        return HttpResponse(f"Error occurred: {err}. URL: {url}", status=500)
    except ValueError as json_err:
        return HttpResponse(f"JSON decode error: {json_err}. URL: {url}", status=500)

    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'licitaciones.html', {'page_obj': page_obj})


def list_ordenes(request):
    # Obtener parámetros de la solicitud
    fecha = request.GET.get('fecha')  # Formato ddmmaaaa
    estado = request.GET.get('estado')
    codigo = request.GET.get('codigo')
    codigo_organismo = request.GET.get('CodigoOrganismo')
    codigo_proveedor = request.GET.get('CodigoProveedor')

    # Construir la URL base
    url = f"{API_BASE_URL}ordenesdecompra.json?ticket={TICKET}"

    # Agregar parámetros a la URL según estén disponibles
    if fecha:
        url += f"&fecha={fecha}"
    if estado:
        url += f"&estado={estado}"
    if codigo:
        url += f"&codigo={codigo}"
    if codigo_organismo:
        url += f"&CodigoOrganismo={codigo_organismo}"
    if codigo_proveedor:
        url += f"&CodigoProveedor={codigo_proveedor}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get('Listado', [])
        
        # Manejar el caso donde no hay órdenes de compra disponibles
        if not data:
            return render(request, 'ordenes.html', {'no_data': True})
        
    except requests.exceptions.HTTPError as http_err:
        return HttpResponse(f"HTTP error occurred: {http_err}", status=response.status_code)
    except requests.exceptions.RequestException as err:
        return HttpResponse(f"Error occurred: {err}", status=500)
    except ValueError as json_err:
        return HttpResponse(f"JSON decode error: {json_err}", status=500)

    paginator = Paginator(data, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'ordenes.html', {'page_obj': page_obj})


def licitacion_detail(request, codigo):
    url = f"{API_BASE_URL}licitaciones.json?codigo={codigo}&ticket={TICKET}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get('Listado', [])[0] if response.json().get('Listado') else None
        
        if not data:
            return HttpResponse("No se encontró la licitación.")
        
        # Debug: Imprimir la estructura del JSON recibido
        print(data)
        
        return render(request, 'licitacion_detail.html', {'licitacion': data})
        
    except requests.exceptions.HTTPError as http_err:
        return HttpResponse(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        return HttpResponse(f"Error occurred: {err}")
    except ValueError as json_err:
        return HttpResponse(f"JSON decode error: {json_err}")

def orden_detail(request, codigo):
    url = f"{API_BASE_URL}ordenesdecompra.json?codigo={codigo}&ticket={TICKET}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get('Listado', [])[0] if response.json().get('Listado') else None
        
        if not data:
            return HttpResponse("No se encontró la orden de compra.")
        
        # Debug: Imprimir la estructura del JSON recibido
        print(data)
        
        return render(request, 'orden_detail.html', {'orden': data})
        
    except requests.exceptions.HTTPError as http_err:
        return HttpResponse(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        return HttpResponse(f"Error occurred: {err}")
    except ValueError as json_err:
        return HttpResponse(f"JSON decode error: {json_err}")

def buscar_proveedor(request, rut):
    url = f"{API_BASE_URL}Empresas/BuscarProveedor?rutempresaproveedor={rut}&ticket={TICKET}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Asegurarse de que hay resultados en la lista
        if data.get('Cantidad', 0) == 0:
            return HttpResponse("No se encontró ningún proveedor con ese RUT.")

        empresa = data['listaEmpresas'][0]

        return render(request, 'proveedor_detail.html', {'empresa': empresa})

    except requests.exceptions.HTTPError as http_err:
        return HttpResponse(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        return HttpResponse(f"Error occurred: {err}")
    except ValueError as json_err:
        return HttpResponse(f"JSON decode error: {json_err}")