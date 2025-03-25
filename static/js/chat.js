const chatSocket = new WebSocket(
  "ws://" +
    window.location.host +
    "/city_stars/profile/" +
    profile_slug +
    "/friends/" +
    friend_slug +
    "/chat/"
);
const chatContainer = document.querySelector("#id_chat_item_container");

window.onload = function () {
  chatContainer.scrollTop = chatContainer.scrollHeight;
};

document.querySelector("#id_message_send_input").focus();
document.querySelector("#id_message_send_input").onkeyup = function (e) {
  if (e.keyCode == 13) {
    document.querySelector("#id_message_send_button").click();
  }
};

document.querySelector("#id_message_send_button").onclick = function (e) {
  var messageInput = document.querySelector("#id_message_send_input").value;
  if (messageInput !== "") {
    chatSocket.send(
      JSON.stringify({
        message: messageInput,
        username: profile_username,
        chat: chat_id,
      })
    );
  } else {
    e.preventDefault();
  }
};

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);

  var div = document.createElement("div");
  div.classList.add("row");
  div.classList.add("g-0");
  if (data.username == user_username) {
    div.classList.add("profile-msg");
  } else {
    div.classList.add("friend-msg");
  }
  div.classList.add("flex");
  var strong = document.createElement("strong");
  var p = document.createElement("p");
  strong.innerHTML = data.username + " - " + data.sent;
  p.innerHTML = data.message;

  div.appendChild(strong);
  div.appendChild(p);

  document.querySelector("#id_message_send_input").value = "";
  chatContainer.appendChild(div);
  if (
    chatContainer.scrollHeight - chatContainer.scrollTop <=
    chatContainer.clientHeight + 500
  ) {
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }
};
