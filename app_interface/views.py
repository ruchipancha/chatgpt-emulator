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
initial_story= "As the sun began to set, a soft orange glow illuminated the sky. The air was cool and calm, and the world seemed to slow down. Maria sat on the front porch of her house, gazing out at the serene scene before her. The warm glow of the sun was reflected in her eyes, casting a soft glow on her face. She breathed in the fresh air, feeling a sense of peace that she hadn't felt in a long time. Suddenly, she saw a small flicker of light in the distance. As it grew closer, she realized it was a firefly. Its small body glowed a soft yellow, illuminating the darkness around it. Maria watched in wonder as it danced around her, leaving a trail of light in its wake. The firefly flew closer to Maria, hovering in front of her face. It seemed to be studying her, as if trying to communicate something. Maria couldn't help but feel a sense of connection to the small creature. Without warning, the firefly flew away, disappearing into the darkness. But Maria felt something different inside her. She felt a warmth and a sense of purpose she had never experienced before. She knew that the firefly had brought her a message, although she wasn't quite sure what it was. The next morning, Maria woke up with a renewed sense of energy. She knew that she had to make a change in her life, and she felt ready to take on whatever challenges lay ahead. As she walked outside, the sun once again began to set, casting a warm glow on the world around her. Maria smiled, feeling grateful for the small firefly that had shown her the way. She knew that, no matter what, the glow inside her would never fade."
   
chat_history = [{"role": "assistant", "content": initial_story}]
userid = ''

def HomePageView(request):
    template_name = "index.html"
    form = IDInputForm(request.POST)
    if form.is_valid():
        idInput = form.cleaned_data

        exists = checkIfIDExists(idInput)
        if exists :
            global userid
            userid = idInput
            return redirect("chatwindow")
        #add else for if id does not exist return form with validation
    else:
        form = IDInputForm()
        return render(request, template_name, {'form':form})
    return render(request,template_name)

def checkIfIDExists(id):
    #read from file containing ids
    return True

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

def CompletionView(request):
    template_name = "completion.html"
    if request.method == 'POST':
        data = json.load(request)
        story = data['user_story']
        filename = userid['id_field'] + "Results.csv"
        f = open(filename,"w+")
        writer = csv.writer(f)
        writer.writerow(['Role', 'Input'])
        for chat in chat_history:
            writer.writerow([chat['role'], chat['content'] ])
        writer.writerow (["\nFinal Story : "+story])
        f.close()
        # return redirect("complete")
        return JsonResponse("success", safe=False)
    else:
        return render(request, template_name)



