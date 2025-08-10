from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class User(AbstractUser):
    ROLE_CHOICES = (
        ('reader', 'reader'),
        ('author', 'author'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', limit_choices_to={'role': 'author'})
    description = models.TextField(blank=True)
    excerpt = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-publish_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200]
            slug = base
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # allow anonymous later if wanted
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)  # moderation switch

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"Comment by {self.author or 'Anonymous'} on {self.post.title}"
