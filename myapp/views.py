from django.shortcuts import render, redirect
from django.http import JsonResponse
from .blockchain_utils import get_company_details, get_total_companies, register_company, add_product,edit_company,delete_company
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Get the web3 instance (this should already be set up in your blockchain_utils.py)
from web3 import Web3

# Ensure CSRF is disabled for simplicity in these views (not recommended in production)
import json
@csrf_exempt
def register_company_view(request):
    if request.method == 'POST':
        try:
            body = request.body
            print("Request body:", body)  # Add this line to debug
            
            company_id = request.POST.get('company_id')
            company_name = request.POST.get('company_name')
            company_email = request.POST.get('company_email')
            company_phoneno = request.POST.get('company_phoneno')
            owner_address = request.POST.get('owner_address')

            # Print values to debug
            print("Company ID:", company_id)
            print("Company Name:", company_name)
            print("Owner Address:", owner_address)

            receipt = register_company(company_id,company_name,company_email,company_phoneno, owner_address) 
            # receipt = register_company(company_id, company_name, owner_address)
            
            return JsonResponse({'status': 'success', 'transaction': receipt}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON: ' + str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return render(request, 'register_company.html')
@csrf_exempt
def edit_company_view(request):
    """
    Handle requests to edit an existing company.
    """
    if request.method == 'POST':
        try:
            # Parse the request data
            company_id = request.POST.get('company_id')
            company_name = request.POST.get('company_name')
            company_email = request.POST.get('company_email')
            company_phoneno = request.POST.get('company_phoneno')
            owner_address = request.POST.get('owner_address')

            # Debugging logs
            print("Company ID:", company_id)
            print("New Company Name:", company_name)
            print("New Owner Address:", owner_address)

            # Call the edit company function
            receipt = edit_company(company_id,company_name,company_email,company_phoneno, owner_address)

            # Return success response with transaction details
            return JsonResponse({'status': 'success', 'transaction': receipt}, status=200)
        except Exception as e:
            # Handle errors and return an error response
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # Render the edit company form (if applicable)
    return render(request, 'edit_company.html')
@csrf_exempt
def delete_company_view(request):
    """
    Handle requests to delete a company.
    """
    if request.method == 'POST':
        try:
            # Parse the request data
            company_id = request.POST.get('company_id')

            # Debugging logs
            print("Company ID to delete:", company_id)

            # Call the delete company function
            receipt = delete_company(company_id)

            # Return success response with transaction details
            return JsonResponse({'status': 'success', 'transaction': receipt}, status=200)
        except Exception as e:
            # Handle errors and return an error response
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # Render the delete company form (if applicable)
    return render(request, 'delete_company.html')


@csrf_exempt
def add_product_view(request):
    if request.method == 'POST':
        # Get data from the form or request body
        product_id = request.POST.get('product_id')
        company_id = request.POST.get('company_id')
        product_name = request.POST.get('product_name')

        try:
            # Call the blockchain function to add a product
            receipt = add_product(product_id, company_id, product_name)
            return JsonResponse({'status': 'success', 'transaction': receipt}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return render(request, 'add_product.html')

@csrf_exempt
def edit_product_view(request):
    """
    Handle requests to edit an existing product.
    """
    if request.method == 'POST':
        # Extract data from the request
        product_id = request.POST.get('product_id')
        company_id = request.POST.get('company_id')
        new_product_name = request.POST.get('new_product_name')

        try:
            # Call the blockchain function to edit a product
            receipt = edit_product(product_id, company_id, new_product_name)
            return JsonResponse({'status': 'success', 'transaction': receipt}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # Render the edit product form if the request method is GET
    return render(request, 'edit_product.html')

@csrf_exempt
def delete_product_view(request):
    """
    Handle requests to delete a product.
    """
    if request.method == 'POST':
        # Extract product ID from the request
        product_id = request.POST.get('product_id')

        try:
            # Call the blockchain function to delete a product
            receipt = delete_product(product_id)
            return JsonResponse({'status': 'success', 'transaction': receipt}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # Render the delete product form if the request method is GET
    return render(request, 'delete_product.html')



def get_company_details_view(request, company_id):
    try:
        # Call the blockchain function to get company details
        company_details = get_company_details(company_id)
        return JsonResponse({'status': 'success', 'data': company_details}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def get_total_companies_view(request):
    try:
        # Call the blockchain function to get the total number of companies
        total_companies = get_total_companies()
        return JsonResponse({'status': 'success', 'total_companies': total_companies}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
