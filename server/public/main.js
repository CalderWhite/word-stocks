function changeSVGStyle(iframe) {
    let svg = iframe.contentWindow.document.getElementsByTagName("svg")[0];
    if (svg === undefined) {
        return;
    }

    let width = svg.width.baseVal.value - 40;
    let height = svg.height.baseVal.value;

    let scaleFactor = window.innerWidth*0.5 / width;

    width *= scaleFactor;
    height *= scaleFactor;

    svg.setAttribute("width", width.toString() + "px");
    svg.setAttribute("height", height.toString() + "px");


    iframe.width = width;
    iframe.height = height;
    console.log(iframe);

    //svg.style.margin = "auto";

    $("#graph-container").fadeIn(400);
    $("#main-graph-stats").fadeIn(400);
}

$(document).ready(function() {
    $("#graph-container").fadeOut(0);
    $("#main-graph-stats").fadeOut(0);

    $("#search-form").submit(function(event) {
        let word = $("#search-input").val();
        let iframe = $("#graph-container")[0];

        $("#graph-container").fadeOut(0);
        iframe.src = "/graph_word/" + word;

        $.get("/word_metadata/" + word, function(data) {
            let stats = $(".graph-stats");
            for (let i=0; i<2; ++i) {
                item = stats[i];
                item.innerHTML = data;
            };
        });

        event.preventDefault();
    });
});
