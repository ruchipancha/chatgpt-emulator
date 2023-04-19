from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf import settings
import os
from django.core.files.storage import default_storage

import json
import openai
import csv


from .forms import IDInputForm, StorySubmitForm
# Create your views here.
openai.api_key = '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'
model_engine = "gpt-3.5-turbo"
#initial_story= "As the sun began to set, a soft orange glow illuminated the sky. The air was cool and calm, and the world seemed to slow down. Maria sat on the front porch of her house, gazing out at the serene scene before her. The warm glow of the sun was reflected in her eyes, casting a soft glow on her face. She breathed in the fresh air, feeling a sense of peace that she hadn't felt in a long time. Suddenly, she saw a small flicker of light in the distance. As it grew closer, she realized it was a firefly. Its small body glowed a soft yellow, illuminating the darkness around it. Maria watched in wonder as it danced around her, leaving a trail of light in its wake. The firefly flew closer to Maria, hovering in front of her face. It seemed to be studying her, as if trying to communicate something. Maria couldn't help but feel a sense of connection to the small creature. Without warning, the firefly flew away, disappearing into the darkness. But Maria felt something different inside her. She felt a warmth and a sense of purpose she had never experienced before. She knew that the firefly had brought her a message, although she wasn't quite sure what it was. The next morning, Maria woke up with a renewed sense of energy. She knew that she had to make a change in her life, and she felt ready to take on whatever challenges lay ahead. As she walked outside, the sun once again began to set, casting a warm glow on the world around her. Maria smiled, feeling grateful for the small firefly that had shown her the way. She knew that, no matter what, the glow inside her would never fade."
initial_story = "Amy sat in the waiting room, tapping her foot anxiously. This was her fifth chance to get it right, and she couldn't afford to mess it up again. She had failed so many times before, but she had to keep trying.The door finally opened and a stern-looking woman beckoned her inside. Amy followed her into a small room and sat down at the table. The woman began to ask her questions, and Amy did her best to answer them truthfully. She didn't want to give the wrong impression or say something that would make her lose this chance. As the interview went on, Amy's nerves began to get the best of her. She stumbled over her words and lost her train of thought. The woman looked unimpressed and made a note on her clipboard. After what felt like an eternity, the interview was over. Amy left the room feeling defeated. She had tried so hard, but it didn't seem to be enough. As she walked out of the building, she saw a man sitting on the sidewalk with a cardboard sign that read, 'Anything helps.' Amy dug into her pocket and pulled out a few dollars. As she handed them to the man, she noticed something strange. He had a tattoo on his wrist that looked familiar. It was the same one she had. Amy's heart skipped a beat. She turned to the man and asked, 'How did you get that tattoo?' The man looked up at her and smiled. 'I got it when I was trying to turn my life around. It's a symbol of hope.' Amy felt a glimmer of hope herself. Maybe this wasn't the end of the road. Maybe she still had a chance to get it right."   
chat_history = [{"role": "assistant", "content": initial_story}]
userid = ''
try_chat = []


def HomePageView(request):

    template_name = "index.html"   
    form = IDInputForm(request.POST)
    global userid
    userid = request.GET.get("id")
    return redirect("trygpt")
        #add else for if id does not exist return form with validation
    return render(request,template_name)

def checkIfIDExists(id):
    #read from file containing ids
    return True

#127.0.0.1:5500/index/?id=5536

def ChatWindowView(request):
    template_name = "chatwindow.html"
    if request.method == 'POST':
        #pass to chatgpt here
        data = json.load(request)
        model_response = OpenAIChatResponse(data['user_response'])
        response = {}
        response['model_response'] = model_response
        return JsonResponse(response, safe=False)
    else:
        return render(request,template_name)

def OpenAIChatResponse(user_response):
    chat_history.append({"role": "user", "content": user_response})

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=chat_history
    )
    model_response = completion.choices[0].message.content
    chat_history.append({"role": "assistant", "content": model_response})
    return model_response

def TryGPTView(request):
    template_name = "trygpt.html"
    if request.method == 'POST':
        data = json.load(request)
        try_chat.append({"role": "user", "content": data['user_response']})
        completiontry = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=try_chat
        )
        model_response = completiontry.choices[0].message.content
        try_chat.append({"role": "assistant", "content": model_response})
        response = {}
        response['model_response'] = model_response
        return JsonResponse(response, safe=False)
    else:
        return render(request,template_name)




def CompletionView(request):
    template_name = "completion.html"
    if request.method == 'POST':
        data = json.load(request)
        story = data['user_story']
        time = data['time']
        filename = userid + "Results.csv"
        f = open(filename,"w+")
        writer = csv.writer(f)
        writer.writerow(["Trial Conversations with ChatGPT\n"])
        for trychat in try_chat:
            writer.writerow([trychat['role'], trychat['content'],"\n" ])
        writer.writerow("\nConversations for the study about the story")
        for chat in chat_history:
            writer.writerow([chat['role'], chat['content'] ,"\n"])
        writer.writerow (["\nFinal Story : "+story])
        writer.writerow(["\nTotal Time : "+str(time) + "s"])
        f.close()
        # return redirect("complete")
        return JsonResponse("success", safe=False)
    else:
        return render(request, template_name)



