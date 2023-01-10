document.addEventListener("DOMContentLoaded", function () {
  if (window.location.pathname === "/chatlogs") {
    return;
  }
  var bar_height = document.querySelector(".navbar").offsetHeight;

  var embed = new Twitch.Embed("twitch-embed", {
    channel: "xqc",
    width: "100%",
    height: window.innerHeight - bar_height,
    theme: "dark",
  });

  getStreams("xqc");

  const friends = [
    "xqc",
    "pokelawls",
    "dizzy",
    "jessesmfi",
    "hasanabi",
    "omie",
    "slwalekop",
    "jsmfi",
  ];
  friends.forEach(function (element) {
    getStreams(element);
  });
});
