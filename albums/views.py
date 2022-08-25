from django.db.models.functions import Lower
from django.shortcuts import render, get_object_or_404
from .models import Album
from .forms import AlbumForm
from django.shortcuts import redirect
from django.utils import timezone

# Create your views here.


def album_list(request):
    albums = Album.objects.all().order_by(Lower('title'))
    return render(request, 'album/album_list.html', {'albums': albums})


def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    return render(request, 'album/album_detail.html', {"album": album})


def album_new(request):
    if request.method == "POST":
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.author = request.user
            album.published_date = timezone.now()
            album.save()
            return redirect('album_detail', pk=album.pk)
    else:
        form = AlbumForm()
    return render(request, 'album/album_edit.html', {'form': form})


def album_edit(request, pk):
    post = get_object_or_404(Album, pk=pk)
    if request.method == "POST":
        form = AlbumForm(request.POST, instance=post)
        if form.is_valid():
            album = form.save(commit=False)
            album.author = request.user
            album.published_date = timezone.now()
            album.save()
            return redirect('album_detail', pk=post.pk)
    else:
        form = AlbumForm(instance=post)
    return render(request, 'album/album_edit.html', {'form': form})


def album_remove(request, pk):
    post = get_object_or_404(Album, pk=pk)
    post.delete()
    return redirect('album_list')