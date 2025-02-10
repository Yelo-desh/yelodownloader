function fetchFormats() {
    const url = document.getElementById("video_url").value;
    document.getElementById("hidden_url").value = url;
    fetch('/get_formats', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'url=' + encodeURIComponent(url)
    })
    .then(response => response.json())
    .then(data => {
        let formatSelect = document.getElementById("format_select");
        formatSelect.innerHTML = "";
        data.forEach(format => {
            let option = document.createElement("option");
            option.value = format.format_id;
            option.textContent = `${format.resolution} (${format.ext})`;
            formatSelect.appendChild(option);
        });
    });
}

function getCookie(name) {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim();
        if (c.startsWith(name + '=')) {
            return c.split('=')[1];
        }
    }
    return null;
}

function acceptCookies() {
    document.cookie = "cookiesAccepted=true; path=/; max-age=" + (60*60*24*365);
    document.getElementById('cookie-banner').style.display = 'none';
}

window.onload = function() {
    if (!getCookie("cookiesAccepted")) {
        document.getElementById('cookie-banner').style.display = 'block';
    }
};



