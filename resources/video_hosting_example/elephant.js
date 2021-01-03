
var games_list = [];
var clip_list = null;
var apache_proxy = 'clips';

function buildIndex(games) {
    var index_div = document.getElementById("index");
    var dropdown_div = document.createElement("div");
    dropdown_div.setAttribute("id", "clip_dropdown");
    dropdown_div.setAttribute("class", "dropdown-content");

    games.forEach(function (game) {
        var new_link = document.createElement("a");
        new_link.innerHTML = game;
        new_link.setAttribute("onclick", "loadClips('" + game + "')");
        dropdown_div.appendChild(new_link);
        games_list.push(game);
    });

    index_div.appendChild(dropdown_div);
}

function request(str, option = null) {
    let promise = new Promise(function (myResolve) {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                myResolve(this.responseText);
            }
        };
        if (option === null) {
            xmlhttp.open("GET", "/clips/helper.php?action=" + str, true);
        } else {
            xmlhttp.open("GET", "/clips/helper.php?action=" + str + "&option=" + option, true);
        }
        xmlhttp.send();
    });

    promise.then(
        function (value) {
            value = JSON.parse(value);
            switch (str) {
                case 'pageLoad':
                    pageLoad(value);
                    break;
                default:
                    break;
            }
        }
    );
}

function pageLoad(value_array) {
    buildIndex(value_array['games_index']);
    clip_list = value_array['game_clips'];
}

function loadClips(game_choice) {
    var sub_body = document.getElementById("sub_body");
    recursivelyKillChildren(sub_body);
    for (var key in clip_list) {
        if (key == game_choice) {

            for (var sub_key in clip_list[key]) {
                var new_div = document.createElement("div");
                new_div.setAttribute("class", "video_div");

                var title_div = document.createElement("div");
                title_div.setAttribute("class", "video_title_div");
                title_div.innerHTML = clip_list[key][sub_key]['datetime'];

                var new_video = document.createElement("video");
                new_video.setAttribute("class", "video_player");
                new_video.setAttribute("width", "320");
                new_video.setAttribute("height", "240");
                new_video.setAttribute("controls", "");

                var new_source = document.createElement("source");
                new_source.setAttribute("src", clip_list[key][sub_key]['src']);
                new_source.setAttribute("type", "video/mp4");

                var link_button = document.createElement("button");
                link_button.setAttribute("type", "button");
                link_button.innerHTML = "Copy video link to clipboard";
                link_button.setAttribute("onclick","link2Clipboard('" + clip_list[key][sub_key]['src'] + "')");

                new_video.appendChild(new_source);
                new_div.appendChild(title_div);
                new_div.appendChild(new_video);
                new_div.appendChild(link_button);
                sub_body.appendChild(new_div);
            }   
        }
    }
    document.getElementById("body_top").innerHTML = game_choice;
}

function recursivelyKillChildren(node) {
    while (node.childNodes.length > 0) {
        node.removeChild(node.childNodes[0]);
    }
}

function link2Clipboard(link) {
    var clipboard = document.getElementById("clipboard");
    var clipboard_content = document.createElement('input');
    link = encodeURI(window.location.href.replace(apache_proxy,'') + link);
    clipboard_content.setAttribute("value", link);
    clipboard.appendChild(clipboard_content);
    clipboard_content.select();
    document.execCommand('copy');
    recursivelyKillChildren(clipboard);
}

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function showDropDown() {
    document.getElementById("clip_dropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
} 