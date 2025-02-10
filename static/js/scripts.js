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


