from django.contrib.auth.decorators import login_required

from .models import User, Requester


@login_required()
def context(request):
	user = User.objects.all()
	if request.user in user:
		requester = Requester.objects.get(user=request.user)
		return {'requester': requester}
	else:
		return None
