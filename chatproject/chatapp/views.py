from django.http import JsonResponse  # or other appropriate response


def index(request):
    return JsonResponse({"message": "Welcome to Chat API"})
