from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings

import json
import openai


from .forms import IDInputForm
# Create your views here.
openai.api_key = settings.CHATGPT_KEY
model_engine = "gpt-3.5-turbo"
chat_history = []

def HomePageView(request):
    template_name = "index.html"
    form = IDInputForm(request.POST)
    if form.is_valid():
        idInput = form.cleaned_data

        exists = checkIfIDExists(idInput)
        if exists :
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



# content = input("User: ")
#     messages.append({"role": "user", "content": content})
    
#     completion = openai.ChatCompletion.create(
#       model="gpt-3.5-turbo",
#       messages=messages
#     )

#     chat_response = completion.choices[0].message.content
#     print(f'ChatGPT: {chat_response}')
#     messages.append({"role": "assistant", "content": chat_response})

    

