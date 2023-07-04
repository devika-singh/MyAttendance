from .models import Class

def courses(request):
	if request.user.is_authenticated:
		return {'foo_courses': request.user.classes.all().values('cid'), 'foo_courses_len': request.user.classes.all().values('cid').count(),}
	else:
		return {}
