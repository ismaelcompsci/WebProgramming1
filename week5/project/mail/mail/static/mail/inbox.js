document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";
  document.querySelector("#email-box").style.display = "none";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";

  // send email
  document.querySelector("form").onsubmit = function () {
    send_mail();
    load_mailbox("sent");
  };
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#email-box").style.display = "none"

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  if (mailbox) {
    // Get latest emails in the mailbox
    get_emails(mailbox);
    console.log(mailbox);
  }

}

function send_mail() {
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      if ("message" in result) {
        load_mailbox("sent");
      }
    });
}

function get_emails(box) {
  // GET request to "/emails/mailbox_name"
  fetch(`/emails/${box}`)
    .then((response) => response.json())
    .then((emails) => {
      if (emails) {
        emails.forEach((email) => {
          div = create_email_box(email);

          document.querySelector("#emails-view").append(div);
        });
      }
    });

}

// Creates the individual email view box
function create_email_box(email) {
  let div = document.createElement("div"); 
  let b_sender = document.createElement("b");
  let span_subject = document.createElement("span");
  let span_time = document.createElement("span");

  
  // let a_link = document.createElement("a");
  // let span_link = document.createElement("span");

  div.setAttribute("class", "container-mail");
  div.setAttribute("id", `${email.id}`);
  span_time.setAttribute("id", "timestamp");
  span_subject.setAttribute("id", "subject");
  //span_link.setAttribute("id", "mail-look");

  b_sender.innerHTML = email.sender;
  span_subject.innerHTML = email.subject;
  span_time.innerHTML = email.timestamp;

  //a_link.appendChild(span_link);
  div.appendChild(b_sender);
  div.appendChild(span_subject);
  div.appendChild(span_time);
  //div.appendChild(a_link);

  if (email.read === true) {
    div.style.backgroundColor = "#808080";
  }

  div.addEventListener("click" ,() => load_email(email)); // load email view and unload inbox
  return div;
}




function load_email(email){
  document.querySelector("#emails-view").style.display = "none"; // hide other view
  document.querySelector("#email-box").style.display = "block";
  document.querySelector("#email-box").innerHTML = "";

  // GET email with id
  fetch(`/emails/${email.id}`)
  .then(response => response.json())
  .then(email => {
    let view = load_single_email(email);
    document.querySelector("#email-box").append(view);
  })

  fetch(`/emails/${email.id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true
    })
  })

}


function load_single_email(email) {
  // // Create new div for mail
  let div = document.createElement("div");
  div.setAttribute("class" ,"email-data");

  // From:
  let from = document.createElement("span");
  from.setAttribute("id" ,"email-data-from");
  from.innerHTML = `<b>From: </b>${email.sender}<br>`;

  // To:
  let to = document.createElement("span");
  to.setAttribute("id" ,"email-data-to");
  to.innerHTML = `<b>To: </b>${email.recipients}<br>`;

  // Subject:
  let subject = document.createElement("span");
  subject.setAttribute("id" ,"email-data-subject");
  subject.innerHTML = `<b>Subject: </b>${email.subject}<br>`;

  // Timestamp:
  let timestamp = document.createElement("span");
  timestamp.setAttribute("id" ,"email-data-time");
  timestamp.innerHTML = `<b>Timestamp: </b>${email.timestamp}<br>`;

  // Reply button
  let reply = document.createElement("button");
  reply.setAttribute("id" ,"email-data-reply");
  reply.innerText = "Reply!";

  // Archive Button
  if (document.querySelector("h3").innerHTML !== "Sent"){
    let archive = document.createElement("button");
    archive.setAttribute("id" ,"email-data-reply");
    if (email.archived === false) archive.innerText = "Archive!";
    else archive.innerText = "Unarchive!";  
    div.appendChild(archive);

    archive.addEventListener("click", function() {
      // archive function
      console.log(email.archived)
      if (email.archived == false) {
        archive_item(email, true);
        archive.innerText = "Unarchive!";
      } else {
        archive_item(email, false);
        archive.innerText = "Archive!";
      }
      load_mailbox("inbox");
    });
  }


  reply.addEventListener("click", function() {
    console.log("Reply!");
    // reply funciton
    compose_email()
    document.querySelector("#compose-recipients").value = email.sender;
    document.querySelector("#compose-subject").value = `Re: ${email.subject}`;
    document.querySelector("#compose-body").value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
    document.querySelector("#submit-button").addEventListener("submit", () => load_mailbox("sent"));

  });

  // body
  let body = document.createElement("p");
  body.setAttribute("id", "email-data-body");
  body.innerHTML = `${email.body}`;

  // divider 
  let divider = document.createElement("hr");

  

  div.appendChild(from);
  div.appendChild(to);
  div.appendChild(subject);
  div.appendChild(timestamp);
  div.appendChild(reply);
  div.appendChild(divider);
  div.appendChild(body);

  return div;

}


function archive_item(email, archived) {
  fetch(`/emails/${email.id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: archived
    })
  })
}