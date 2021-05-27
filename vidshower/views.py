from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from random import choice
from .models import videodisplayer as _VIDEO,usermodellikedvideoslist as Like_Videos
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
# from django.contrib.auth import authenticate,login

# Create your views here.

Global_List = []
is_liked = []


def commentfinder(oneobject):
    usercommentdelimitor = '@m;#$}[('
    useruserdelimitor = '$%vV;#}{=)'
    users = []
    comments = []
    mainbreak = []
    try:
        mainbreak = oneobject.comments.split(useruserdelimitor)
    except:
        pass
    for content in mainbreak:
        try:
            temp = content.split(usercommentdelimitor)
            users.append(temp[0])
            comments.append(temp[1])
        except:
            pass
    combine = zip(users,comments)
    return combine



def home(request):
    global Global_List
    ### query from database
    _ALL = _VIDEO.objects.all()
    oneobject = choice(_ALL)
    alreadyliked = False
    if request.user.is_authenticated:
        datal = Like_Videos.objects.filter(user=request.user)
        for data in datal:
            try:
                likedvid = data.likedvids.split(' ')
                if str(oneobject.id) in likedvid:
                    alreadyliked = True 
            except:
                pass
    combine = commentfinder(oneobject)
    Global_List.append(oneobject)
    is_liked.append(alreadyliked)
    return render(request,'videoshow.html',{'data':oneobject,'liked':alreadyliked,'comments':combine})


def prevvideo(request):
    global Global_List,is_liked
    try:
        a = Global_List.pop()
        b = is_liked.pop()
        finer = Global_List[-1]
        print('prev video')
        combine = commentfinder(finer)
        print(finer.title)
        return render(request,'videoshow.html',{'data': finer,'liked':is_liked[-1],'comments':combine})

    except Exception as e:
        print(e)
        return home(request)


def requestvideo(request,videopersonal=None):
    if videopersonal == None:
        videoid = request.GET['videoid']
    else:
        videoid = videopersonal
    if videoid == None:
        return home(request)
    else:
        _FILTER = _VIDEO.objects.filter(id=videoid)
        if not len(_FILTER):
            ########## show message video doesn't exists ##############
            return home(request)
        alreadyliked = False
        if request.user.is_authenticated:
            datal = Like_Videos.objects.filter(user=request.user)
            for data in datal:
                try:
                    likedvid = data.likedvids.split(' ')
                    for xyz in _FILTER:
                        if str(xyz.id) in likedvid:
                            alreadyliked = True 
                except Exception as e:
                    print(e)
                    pass
        for _FILTERS_ in _FILTER:
            combine = commentfinder(_FILTERS_)
            return render(request,'videoshow.html',{'data':_FILTERS_,'comments':combine,'liked':alreadyliked})

@csrf_exempt
def like(request):
    if request.user.is_authenticated:
        username = json.loads(request.body).get('user')
        video = json.loads(request.body).get('videoid')
        likedlist = Like_Videos.objects.filter(user=request.user)
        vidobj = _VIDEO.objects.filter(id=video)
        for items in likedlist:
            try:
                alllikevids = items.likedvids.split(' ')
                if str(video) in alllikevids:
                    alllikevids.remove(str(video))
                    for vid in vidobj:
                        vid.likes -= 1
                        vid.save()
                else:
                    alllikevids.append(str(video))
                    for vid in vidobj:
                        vid.likes += 1
                        vid.save()
                alllikevids = ' '.join(alllikevids)
                items.likedvids = alllikevids
                items.save()
                return JsonResponse({'value':'success'})
            except:
                items.likedvids = str(video)
                items.save()
                for vid in vidobj:
                    vid.likes += 1
                    vid.save()
                    return JsonResponse({'value':'success'})


    
    return JsonResponse({'value':'failure'})

@csrf_exempt
def postcomments(request,id=None):
    if request.user.is_authenticated:
        global Global_List,is_liked
        try:
            comment = request.POST['comment']
            username = request.user.username
        except:
            return redirect('/login')
        usercommentdelimitor = '@m;#$}[('
        useruserdelimitor = '$%vV;#}{=)'
        if usercommentdelimitor in comment or useruserdelimitor in comment:
            return redirect('/')
        if useruserdelimitor in username or usercommentdelimitor in username:
            return redirect('/')
        newcommentelement = username + usercommentdelimitor + comment
        videoplayer = _VIDEO.objects.filter(id=id)
        for video in videoplayer:
            comments = video.comments
            if comments == '' or comments == None:
                comments = ''
                comments += newcommentelement
            else:
                # comments = comments.split(useruserdelimitor)
                # comments.append(newcommentelement)
                # comments = useruserdelimitor.join(comments)
                comments = newcommentelement + useruserdelimitor + comments
            video.comments = comments
            video.save()
            return requestvideo(request,id)
    else:
        return redirect('/login')


def iwanttoupload(request):
    if request.user.is_authenticated:
        return render(request,'index.html')
    else:
        return redirect('/login')


@csrf_exempt
def registervideo(request):
    if request.user.is_authenticated:
        title = request.POST['title']
        video = request.FILES['video']
        desc = request.POST['desc']
        owner = request.user.username


        myobj = _VIDEO(title=title,video=video,desc=desc,likes=0,owner=owner)
        myobj.save()

        print(myobj.id)

        # return link of video to user
        messages.success(request,f"Congratulations Your Video has been Uploaded at http://127.0.0.1:8000/filters?videoid={myobj.id}")
        return redirect('/upload')
    else:
        return redirect('/login')