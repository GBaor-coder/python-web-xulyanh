from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import base64
from io import BytesIO
from .services.image_processing import enhance_image, image_to_base64
import logging

logger = logging.getLogger(__name__)

@require_http_methods(["GET"])
def home(request):
    return render(request, 'enhancer/index.html')

@csrf_exempt
@require_http_methods(["POST"])
def enhance_api(request):
    try:
        algorithm = request.POST.get('algorithm', 'gamma')
        gamma = float(request.POST.get('gamma', 1.0))
        
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image provided'}, status=400)
        
        image_file = request.FILES['image']
        image_bytes = image_file.read()
        
        enhanced_img = enhance_image(image_bytes, algorithm, gamma)
        enhanced_base64 = image_to_base64(enhanced_img)
        
        return JsonResponse({'image': enhanced_base64})
    
    except ValueError as e:
        logger.error(f'ValueError in enhance_api: {str(e)}')
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        logger.error(f'Error in enhance_api: {str(e)}')
        return JsonResponse({'error': 'Image processing failed'}, status=500)


