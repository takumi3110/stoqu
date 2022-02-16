from .models import Requester


def context(request):
	requester = Requester.objects.get(user=request.user)
	return {'requester': requester}
