from django.conf import settings
from django.contrib.auth import get_user_model
from ldap3 import Server, Connection, NTLM, SUBTREE

from user.models import User


# noinspection PyBroadException
class Backend:
	@staticmethod
	def authenticate(request, username=None, password=None):
		server = Server(settings.LDAP_HOST)
		try:
			connection = Connection(
				server,
				user='{0}\\{1}'.format(settings.LDAP_DOMAIN, username),
				password=password,
				authentication=NTLM,
				auto_bind=True,
			)
			user = get_user_model()
			result, created = user.objects.update_or_create(
				username=username,
			)
			search_filter = '(&(objectClass=user)(samAccountName=' + username + '))'
			entry_list = connection.extend.standard.paged_search(
				search_base=settings.LDAP_SEARCH_BASE,
				search_filter=search_filter,
				search_scope=SUBTREE,
				attributes=[
					'sn',
					'givenname',
					'displayname',
					'mail',
					'department',
				],
				paged_size=5,
				size_limit=1000,
				generator=False,
				get_operational_attributes=True,
			)
			connection.unbind()
			for entry in entry_list:
				if created:
					result.is_staff = True
				result.screenname = entry['attributes']['displayName']
				result.first_name = entry['attributes']['sn']
				result.last_name = entry['attributes']['givenname']
				result.email = entry['attributes']['mail']
				result.department = entry['attributes']['department']
			result.save()
			return result
		except User.DoesNotExist:
			return None

	@staticmethod
	def get_user(user_id):
		user = get_user_model()
		try:
			return user.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
