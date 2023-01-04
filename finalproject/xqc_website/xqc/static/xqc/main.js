document.addEventListener("DOMContentLoaded", function () {
  var bar_height = document.querySelector(".navbar").offsetHeight;

  var embed = new Twitch.Embed("twitch-embed", {
    channel: "xqc",
    width: "100%",
    height: window.innerHeight - bar_height,
    theme: "dark",
  });
  console.log(embed.innerHTML);
});

// document.addEventListener("DOMContentLoaded", function () {
//   let todays_chat = get_todays_chat("xqc");
// });

// function get_todays_chat(channel) {
//   // Send a GET request to the URL
//   fetch(`https://logs.ivr.fi/channel/${channel}`, {
//     headers: { "Content-Type": "application/json", Accept: "application/json" },
//   })
//     // Put response into json form
//     .then((response) => response.json())
//     .then((data) => {
//       // Log data to the console
//       return data;
//     });
// }
