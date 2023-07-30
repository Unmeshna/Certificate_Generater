from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from .models import Certificate
import hashlib
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render
from django.template.loader import render_to_string
# from weasyprint import HTML
from xhtml2pdf import pisa
from io import BytesIO


def home_view(request):
    return render(request,'index.html')





def create_certificate(request):
    if request.method=='POST':
        name=request.POST.get('name')
        date=request.POST.get('date')
        description=request.POST.get('description')
        unique_identifier=request.POST.get('unique_identifier')
        content=request.POST.get('content')
       

        certificate=Certificate.objects.create(name=name,date=date, description=description,
                                                 unique_identifier=unique_identifier, content=content)
        
        
        return redirect('view_certificate',certificate_id=certificate.id)
    else:
        return render(request,'create_certificate.html')
    






@api_view(['POST'])
@permission_classes([IsAuthenticated])
def customize_certificate(request):
    # Retrieve the certificate from the request data or database based on your use case
    certificate_id = request.data.get('certificate_id')
    certificate = get_object_or_404(Certificate, pk=certificate_id)
    
    # Check if the authenticated user is the owner of the certificate
    if request.user.id != certificate.user.id:
        return Response({'detail': 'You do not have permission to customize this certificate.'}, status=403)
    
    # Update the certificate content with the custom data sent in the request
    new_content = request.data.get('content')
    certificate.content = new_content
    certificate.save()
    return Response({'detail': 'Certificate customization successful.'}, status=200)







@api_view(['POST'])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_certificate_jwt(request):
    # Get the JWT token from the request headers
    jwt_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    
    # Verify the JWT token
    jwt_authentication = JWTAuthentication()
    try:
        user, _ = jwt_authentication.authenticate(request)
    except Exception as e:
        return Response({'detail': 'Invalid or expired token.'}, status=401)
    
    # Perform the certificate verification logic
    # Retrieve the certificate from the request data or database based on your use case
    certificate_id = request.data.get('certificate_id')
    certificate = get_object_or_404(Certificate, pk=certificate_id)
    
    # Compare the certificate data with the data stored in the JWT token
    if user.id != certificate.user.id:
        return Response({'detail': 'Certificate does not belong to the authenticated user.'}, status=403)
    
    # Add any other verification logic here as per your requirements
    # ...
    
    return Response({'detail': 'Certificate verification successful.'}, status=200)






# def generate_pdf(request, certificate_id):
#     certificate = get_object_or_404(Certificate, pk=certificate_id)
    
#     # PDF Generation logic using reportlab
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="certificate_{certificate_id}.pdf"'
#     p = canvas.Canvas(response, pagesize=letter)
#     # Customize the PDF content here
#     p.drawString(100, 750, f"Certificate Name: {certificate.name}")
#     p.drawString(100, 700, f"Date: {certificate.date}")
#     p.drawString(100, 650, f"Description: {certificate.description}")
#     p.showPage()
#     p.save()
#     return response


def generate_pdf(request, certificate_id):
    # Retrieve the certificate data from the database
    certificate = get_object_or_404(Certificate, pk=certificate_id)

    # Render the HTML template with the certificate data
    html_string = render_to_string('certificate_template.html', {'certificate': certificate})

    # Generate the PDF using xhtml2pdf
    pdf_file = BytesIO()
    pisa.CreatePDF(html_string, dest=pdf_file)

    # Send the PDF file as a response to the user
    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{certificate_id}.pdf"'
    return response


def view_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, pk=certificate_id)
    certificate_hash = certificate.generate_hash()
    return render(request, 'view_certificate.html', {'certificate': certificate,'certificate_hash':certificate_hash})



def verify_certificate(request):
    if request.method == 'POST':
        unique_identifier = request.POST.get('unique_identifier')
        certificate = get_object_or_404(Certificate, unique_identifier=unique_identifier)

        # Check the hash to verify the certificate
        received_hash = request.POST.get('hash')
        if received_hash == certificate.generate_hash():
            return HttpResponse('Certificate is valid!')
        else:
            return HttpResponse('Certificate is invalid!')
    else:
        return render(request, 'verify_certificate.html')

