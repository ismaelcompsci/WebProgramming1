document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".like").forEach(function (button) {
    button.onclick = function () {
      liked(button);
    };
  });
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
