document.addEventListener("DOMContentLoaded", function () {
  get_xqc_logs_today("xqc", "xqc");
});
function get_todays_chat(channel) {
  // Send a GET request to the URL
  fetch(`https://logs.ivr.fi/channel/${channel}`, {
    headers: { "Content-Type": "application/json", Accept: "application/json" },
  })
    // Put response into json form
    .then((response) => response.json())
    .then((data) => {
      return data;
    });
}

function get_xqc_logs_today(channel, user) {
  fetch(`https://logs.ivr.fi/channel/${channel}/user/${user}`, {
    headers: { "Content-Type": "application/json", Accept: "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      chat_div(data);
    });
}

function chat_div(data) {
  let chat_box = document.querySelector(".chat-height");

  console.log(data);
  data.messages.reverse().forEach((element) => {
    let single_msg_div = document.createElement("div");
    let li = document.createElement("li");
    let timestamp = document.createElement("span");
    let username = document.createElement("div");
    let message = document.createElement("div");

    if (check_text_link(element.text)) {
      let link_text = check_text_link(element.text);
      message.innerHTML = link_text;
    } else {
      message.innerHTML = element.text;
    }

    message.className = "message";
    timestamp.className = "timestamp";
    li.className = "single-chat-text";
    single_msg_div.className = "single-chat";
    username.className = "username";

    let d = new Date(Date.parse(element.timestamp));

    timestamp.innerHTML = d.toISOString().replace(/T/, " ").replace(/\..+/, "");
    username.innerHTML = `${element.displayName}:`;

    li.append(timestamp);
    li.append(username);
    li.append(message);

    single_msg_div.appendChild(li);

    chat_box.append(single_msg_div);
  });
}

function isValidHttpUrl(string) {
  let url;
  try {
    url = new URL(string);
  } catch (_) {
    return false;
  }
  return url.protocol === "http:" || url.protocol === "https:";
}

function check_text_link(text) {
  normalString = "";
  textArray = text.split(/(\s+)/);

  textArray.forEach(function (text) {
    if (/\s/g.test(text)) {
      normalString += " ";
      return;
    }
    if (isValidHttpUrl(text)) {
      let a = document.createElement("a");
      a.href = text;
      a.innerHTML = text;
      normalString += a.outerHTML;
    } else {
      normalString += text;
    }
  });
  return normalString;
}
