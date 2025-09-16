from .models import AreaOfWork

def areas_processor(request):
    return {
        "areas": AreaOfWork.objects.all()
    }

# def help_categories_processor(request):
#     return {
#         "help_categories": HelpCategory.objects.prefetch_related("options").all()
#     }