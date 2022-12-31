document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".like").forEach(function (button) {
    button.onclick = function () {
      liked(button);
    };
  });

  // ADD EVENT LISTENER FOR FOLLOW BUTTON ONCLICK RUN FOLLOW() FUNCTION
  if (document.URL.includes("profile")) {
    let follow_button = document.querySelector("#follow-button");

    follow_button.onclick = function () {
      let follow_user_id = document.querySelector("#user-id").innerHTML;
      follow(follow_user_id);
    };
  }

  document.querySelectorAll("#edit-post").forEach(function (button) {
    // When edit button clicked
    button.onclick = function () {
      if (button.innerHTML === "Edit") {
        // Show textarea
        let post_id = showArea(this.dataset.edit);
        // Save saves the data to the post
        console.log("Done Showing TextArea");
        button.innerHTML === "Close";
      }

      document.querySelector(`#${this.dataset.edit} textarea`).onkeyup = () => {
        button.innerHTML = "Save";
      };

      if (button.innerHTML === "Save") {
        let post_id = showArea(this.dataset.edit);

        let new_text = document.querySelector(
          `#${this.dataset.edit} textarea`
        ).value;
        fetch(`/posts/${post_id}`, {
          method: "PUT",
          body: JSON.stringify({
            text: new_text,
          }),
        });
        console.log("PUTTING DATA INT DB");
        button.innerHTML = "Edit";
        document.querySelector(`#${this.dataset.edit}`).style.display = "none";
      }
    };
  });
  document.querySelectorAll("#close-text").forEach(function (button) {
    button.onclick = function () {
      if (button.innerHTML === "Close") {
        button.parentNode.style.display = "none";
      }
    };
  });
});

function liked(button) {
  let like_button = button;
  let red_button_path = "/static/network/liked.png";
  let white_button_path = "/static/network/non-likedV2.png";
  let source = like_button.src.replace("http://127.0.0.1:8000", "");

  let div = button.parentNode.parentNode;

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
    div.querySelector("#like-count").innerHTML++;
  }
  // unliked
  if (source === red_button_path) {
    like_button.src = white_button_path;
    fetch(`posts/${button.id}`, {
      method: "PUT",
      body: JSON.stringify({
        post_id: button.id,
        like: false,
      }),
    });
    div.querySelector("#like-count").innerHTML--;
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

function showArea(page) {
  // Open text area
  let post_id = page.replace("text", "");

  document.querySelector(`#${page}`).style.display = "block";

  // Fill text area with post text
  fetch(`/posts/${post_id}`)
    .then((response) => response.json())
    .then((post) => {
      document.querySelector(`#${page} textarea`).value = post.text;
    });
  return post_id;
}
