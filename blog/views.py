from django.shortcuts import render

posts=[
    {
        'author': 'John Doe',
        'title': 'My First Post',
        'content': 'This is the content of my first post.',
        'date_posted': 'August 27, 2023'
    },
    {
        'author': 'Jane Smith',
        'title': 'Another Day in Paradise',
        'content': 'Today was a beautiful day in paradise.',
        'date_posted': 'August 28, 2023'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    
    return render(request, 'blog/about.html', {'title': 'About'})
