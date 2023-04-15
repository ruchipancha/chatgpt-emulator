let startTime, endTime;

function nextPage1() {
    const instructions = document.getElementById("instructions");
    instructions.remove()

    const instructions2 = document.getElementById("instructions-2")
    instructions2.style.display = "block"
}



function nextPage2(){
    //const initial_story= "As the sun began to set, a soft orange glow illuminated the sky. The air was cool and calm, and the world seemed to slow down. Maria sat on the front porch of her house, gazing out at the serene scene before her. The warm glow of the sun was reflected in her eyes, casting a soft glow on her face. She breathed in the fresh air, feeling a sense of peace that she hadn't felt in a long time. Suddenly, she saw a small flicker of light in the distance. As it grew closer, she realized it was a firefly. Its small body glowed a soft yellow, illuminating the darkness around it. Maria watched in wonder as it danced around her, leaving a trail of light in its wake. The firefly flew closer to Maria, hovering in front of her face. It seemed to be studying her, as if trying to communicate something. Maria couldn't help but feel a sense of connection to the small creature. Without warning, the firefly flew away, disappearing into the darkness. But Maria felt something different inside her. She felt a warmth and a sense of purpose she had never experienced before. She knew that the firefly had brought her a message, although she wasn't quite sure what it was. The next morning, Maria woke up with a renewed sense of energy. She knew that she had to make a change in her life, and she felt ready to take on whatever challenges lay ahead. As she walked outside, the sun once again began to set, casting a warm glow on the world around her. Maria smiled, feeling grateful for the small firefly that had shown her the way. She knew that, no matter what, the glow inside her would never fade."
    const initial_story = 'Amy sat in the waiting room, tapping her foot anxiously. This was her fifth chance to get it right, and she couldn\'t afford to mess it up again. She had failed so many times before, but she had to keep trying. \nThe door finally opened and a stern-looking woman beckoned her inside. Amy followed her into a small room and sat down at the table. The woman began to ask her questions, and Amy did her best to answer them truthfully. She didn\'t want to give the wrong impression or say something that would make her lose this chance.\n As the interview went on, Amy\'s nerves began to get the best of her. She stumbled over her words and lost her train of thought. The woman looked unimpressed and made a note on her clipboard.\n After what felt like an eternity, the interview was over. Amy left the room feeling defeated. She had tried so hard, but it didn\'t seem to be enough. As she walked out of the building, she saw a man sitting on the sidewalk with a cardboard sign that read, "Anything helps."\n Amy dug into her pocket and pulled out a few dollars. As she handed them to the man, she noticed something strange. He had a tattoo on his wrist that looked familiar. It was the same one she had.\n Amy\'s heart skipped a beat. She turned to the man and asked, "How did you get that tattoo?" \n The man looked up at her and smiled. "I got it when I was trying to turn my life around. It\'s a symbol of hope." '
    const instructions2 = document.getElementById("instructions-2")
    instructions2.remove()

    //const chatwindow = document.getElementById("chatwindow");
    const chatwindow = document.getElementById("chatwindow-row");
    const storysubmit = document.getElementById("storysubmitwindow")
    chatwindow.style.display = "flex"
    storysubmit.style.display = "block"
    $("#chatwindow-instructions").css("display","block")
    //chatwindowinstructions.style.display = "block"


    //add story to chatgpt?
    createConvoItem(initial_story,'model',false);

    

}

function chatSend() {
    const textInputElem = document.getElementById("chatwindow-chatinput");
    const textInput = textInputElem.value;

    if(textInput.length <= 0) {
        return
    }
    //const chatWindow = document.getElementById("chatwindow-chats")

    //const convoDiv = createConvoItem(textInput);
    createConvoItem(textInput);
    //chatWindow.append(convoDiv)

    textInputElem.value = ""
    //after passing to chatgpt, return result from view and add to left of window
    $.ajax({
        url: 'chat',
        type: 'POST',
        dataType: 'json',
        data: JSON.stringify({user_response: textInput,}),
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
        },
        success: (data) => {
            createConvoItem(data['model_response'],'model');
        },
          error: (error) => {
            console.log(error);
        },

    })
    console.log("waiting")



}

function taskComplete() {
    document.getElementById("submit-btn").disabled = false
    final_story = document.getElementById("storysubmitwindow-textarea").value

    $.ajax({
        url: 'complete',
        type: 'POST',
        dataType: 'json',
        data: JSON.stringify({user_story: final_story}),
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
        },
        success: (data) => {
            location.href = '/complete';
        },
          error: (error) => {
            console.log(error);
        }

    });
}

function createConvoItem(text,type,loading) {
    const chatWindow = document.getElementById("chatwindow-chats")
    const convoDiv = document.createElement("div")
    if (type == 'model') {

        convoDiv.classList.add("modelConvoItem")
        convoDiv.classList.add("float-start")
        if(loading){
            convoDiv.classList.add("loading")
        }
    }
    else {
        convoDiv.classList.add("userConvoItem")
        convoDiv.classList.add("float-end")
    }
    const textNode = document.createTextNode(text);
    const preNode = document.createElement("pre")
    preNode.classList.add("preNode")
    preNode.appendChild(textNode)
    convoDiv.appendChild(preNode)
    chatWindow.append(convoDiv)
    //return convoDiv
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  window.onload = (event) => {
    document.getElementById("storysubmitwindow").addEventListener("keyup", function() {
        var storyInput = document.getElementById('storysubmitwindow-textarea').value;
        var wordCountDivSpan = document.getElementById("wordcount-count")
        if (storyInput != "") {
            document.getElementById('submit-btn').removeAttribute("disabled");
            wordCountDivSpan.innerHTML = storyInput.trim().split(/\s+/).length
        } else {
            document.getElementById('submit-btn').setAttribute("disabled", null);
            wordCountDivSpan.innerHTML = "0"
        }
    })
  };

function addLoader(event) {
    if(event.target.id == 'submit-btn'){
        return
    }
    else {
        createConvoItem("....","model",true)
    }
}

$(document).on({
    ajaxStart: (event) => {
        setTimeout(addLoader(event),1000)
    },
    ajaxStop: () => {
        document.getElementsByClassName("loading")[0].remove()
    }
})





