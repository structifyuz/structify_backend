import re

from myapp.models import ArticleFileAttachment


def mark_article_attachment_files_as_used(content):
    urls = re.findall(r'src="([^"]+)"', content)
    for url in urls:
        try:
            file_obj = ArticleFileAttachment.objects.get(file=url.replace('/media/', ''), used=False)
            file_obj.used = True
            file_obj.save()
        except ArticleFileAttachment.DoesNotExist:
            pass