from django.shortcuts import render
from django.http import HttpResponse, Http404
import yt_dlp
import os, random, string
import re

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*：｜]', '', filename)

def generate_random_file_name(ext):
    chars = string.ascii_letters + string.digits
    random_name = ''.join(random.choice(chars) for _ in range(12))
    return f"{random_name}.{ext}"

def youtube(request):
    if request.method == 'POST':
        link = request.POST.get('link')

        if not link:
            return render(request, 'index.html', {'error': 'No link provided'})

        download_dir = os.path.join(os.path.dirname(__file__), 'downloads')
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        try:
            video_ext = 'mp4'
            file_name = generate_random_file_name(video_ext)
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(download_dir, file_name),
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=True)
                video_title = sanitize_filename(info_dict.get('title', 'downloaded_video'))
                video_ext = info_dict.get('ext', 'mp4')

            file_path = os.path.join(download_dir, file_name)
            file_path = os.path.normpath(file_path)
            print(f"File path: {file_path}")

            # Send the file name and video title to the HTML page
            context = {
                'video_title': video_title,
                'file_name': file_name,
                'success_message': f"The video '{video_title}' has been processed and is ready for download."
            }
            return render(request, 'index.html', context)

        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'index.html', {'error': 'An error occurred during the download'})

    return render(request, 'index.html')

def download_file(request, file_name):
    download_dir = os.path.join(os.path.dirname(__file__), 'downloads')
    file_path = os.path.join(download_dir, file_name)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='video/mp4')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    else:
        raise Http404("File not found")
