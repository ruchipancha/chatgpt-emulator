function nextPage() {
    const instructions = document.getElementById("instructions");
    instructions.remove()

    const chatwindow = document.getElementById("chatwindow");
    chatwindow.style.display = "block"
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
        }
        
    })
    
}

function createConvoItem(text,type) {
    const chatWindow = document.getElementById("chatwindow-chats")
    const convoDiv = document.createElement("div")
    if (type == 'model') {
        
        convoDiv.classList.add("modelConvoItem")
        convoDiv.classList.add("float-start")
    }
    else {
        convoDiv.classList.add("userConvoItem")
        convoDiv.classList.add("float-end")
    }
    const node = document.createTextNode(text);
    convoDiv.appendChild(node)
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
