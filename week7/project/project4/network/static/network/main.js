document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".like").forEach(function (button) {
    button.onclick = function () {
      liked(button);
    };
  });
  // ADD EVENT LISTENER FOR FOLLOW BUTTON ONCLICK RUN FOLLOW() FUNCTION
  let follow_button = document.querySelector("#follow-button");
  follow_button.onclick = function () {
    let follow_user_id = document.querySelector("#user-id").innerHTML;
    follow(follow_user_id);
  };
});

function liked(button) {
  let like_button = button;
  let red_button_path = "/static/network/liked.png";
  let white_button_path = "/static/network/non-likedV2.png";
  let source = like_button.src.replace("http://127.0.0.1:8000", "");

  console.log(like_button);
  console.log(source);

  //liked
  if (source === white_button_path) {
    like_button.src = red_button_path;
    fetch(`posts/${button.id}`, {
      method: "PUT",
      body: JSON.stringify({
        post_id: button.id,
        like: true,
      }),
    });
  }
  // unliked
  if (source === red_button_path) {
    like_button.src = white_button_path;
    console.log("tha one");
  }
}

function follow(user_id) {
  // IMPLEMENT FOLLOW BUTTON
  let follow_or_unfollow = document.querySelector("#follow-button");
  let browsing_id = document.querySelector("#browser-id").innerHTML;

  if (follow_or_unfollow.innerHTML === "Follow") {
    fetch(`${user_id}`, {
      method: "PUT",
      body: JSON.stringify({
        follow: true,
        being_followed: user_id,
        doing_following: browsing_id,
      }),
    });
    follow_or_unfollow.innerHTML = "Unfollow";
    count = document.querySelector("#followers-count");
    count.innerHTML++;
  } else {
    fetch(`${user_id}`, {
      method: "PUT",
      body: JSON.stringify({
        follow: false,
        being_followed: user_id,
        doing_following: browsing_id,
      }),
    });
    follow_or_unfollow.innerHTML = "Follow";
    count = document.querySelector("#followers-count");
    count.innerHTML--;
  }
}
