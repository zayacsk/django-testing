from django.urls import reverse

NOTE_SLUG = 'slug'
NEW_SLUG = 'new-slug'

HOME_URL = reverse('notes:home')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')

LIST_URL = reverse('notes:list')
ADD_URL = reverse('notes:add')
SUCCESS_URL = reverse('notes:success')

DETAIL_URL = reverse('notes:detail', args=(NOTE_SLUG,))
EDIT_URL = reverse('notes:edit', args=(NOTE_SLUG,))
DELETE_URL = reverse('notes:delete', args=(NOTE_SLUG,))
