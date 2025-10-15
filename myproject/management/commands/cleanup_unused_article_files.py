from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from myapp.models import ArticleFileAttachment

class Command(BaseCommand):
    help = "Deletes temporary blog files older than 1 day and unused"

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(days=1)
        files_to_delete = ArticleFileAttachment.objects.filter(used=False, uploaded_at__lt=cutoff)
        count = files_to_delete.count()
        for f in files_to_delete:
            f.delete()
        self.stdout.write(f"Deleted {count} unused temporary files.")
