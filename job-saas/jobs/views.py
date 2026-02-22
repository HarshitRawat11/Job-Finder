from django.shortcuts import render

# Create your views here.
from .services import search_jobs_with_agent

def search_job_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        result = search_jobs_with_agent(prompt)
        return render(request, 'jobs/results.html', {'result': result})
    else:
        return render(request, 'jobs/search.html')