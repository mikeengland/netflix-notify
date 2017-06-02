from django.views.generic import FormView

from .forms import WatcherForm


class WatcherView(FormView):
    """
    View for adding new 'watchers' (awaiting notifications on a title)
    """
    template_name = 'add_watcher.html'
    form_class = WatcherForm
    success_url = '.'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
