from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post
from taggit.models import Tag
from django.db.models import Count

# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 4

class PostListViewByTag(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self, **kwargs):
        tag_slug = self.kwargs["tag"] if "tag" in self.kwargs else None

        tag = get_object_or_404(Tag, slug=tag_slug)

        return Post.objects.all().filter(tags__in=[tag])


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = context["object"]    # we have a guarantee that "object" exists in context

        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids)\
                                    .exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                     .order_by('-same_tags','-publish')[:4]

        context["similar_posts"] = similar_posts
        return context


def bio(request):
    return render(request, 'blog/bio.html', {'title': 'About'})

def interviews(request):
    return render(request, 'blog/interviews.html')