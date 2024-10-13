from django.shortcuts import render
from django.http import HttpResponse

# Function to capture visitor's IP address
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# View function for the sports homepage
def sports_home(request):
    visitor_ip = get_client_ip(request)  # Get the visitor's IP address

    # Check if the IP address is already stored in cookies
    stored_ip = request.COOKIES.get('visitor_ip')
    if stored_ip != visitor_ip:
        # If the IP is new, this is a first visit or from a new location
        visit_count = 1
    else:
        # Increment visit count if the visitor has been here before
        visit_count = int(request.COOKIES.get('visit_count', 0)) + 1

    # Render the response and pass the visit count and IP address to the template
    response = render(request, 'sports/home.html', {'visit_count': visit_count, 'visitor_ip': visitor_ip})

    # Store the visitor's IP and visit count in cookies (expires in 30 days)
    response.set_cookie('visitor_ip', visitor_ip, max_age=30*24*60*60)
    response.set_cookie('visit_count', visit_count, max_age=30*24*60*60)

    return response
