function fadeInGraph() {
    $("#graph").fadeTo(400, 1);
    $("#main-graph-stats").fadeTo(400, 1);
}

$(document).ready(function() {
    $("#graph").fadeTo(0, 0);
    $("#main-graph-stats").fadeTo(0, 0);

    // auto select the search bar when the user starts typing.
    $(document).keypress(function() {
        let searchbar = $("#search-input")[0];
        if (!$("#search-input").is(":focus")) {
            searchbar.focus();
            searchbar.select();
        }
    });

    $("#search-form").submit(function(event) {
        let word = $("#search-input").val();
        let graph = $("#graph")[0];

        $("#graph").fadeTo(0, 0);
        graph.src = "/graph_word/" + word;

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
