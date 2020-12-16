// not much of this is fault tolerant. I am okay with that for now.

let graphContainer;
let chart;
let lineSeries;
function fadeInGraph() {
    $("#graph").fadeTo(400, 1);
    $("#main-graph-stats").fadeTo(400, 1);
}

function generateSocials(word) {
    // call until twitter is loaded.
    if (twttr.widgets === undefined) {
        setTimeout(function(){generateSocials(word)}, 50);
        return;
    } else if (twttr.widgets === undefined) {
        twtter.ready(function() {
            generateSocials(word);
        });
    }

    let tweetContainer = $("#twitter-container")[0];

    // just in case something whacky happens and 2 buttons appear.
    while (tweetContainer.children.length > 0) {
        tweetContainer.removeChild(tweetContainer.firstChild);
    };

    twttr.widgets.createShareButton(
        "https://word-stocks.calderwhite.me/words/" + word + "?a=1",
        tweetContainer,
        {
            text: "Check out the performance of stocks relating to " + word + "!",
            size: "large"
        }
    );
 

}

$(window).resize(function(){
    chart.applyOptions({
        width: Math.max(600, window.innerWidth*0.5),
        height: Math.max(600*0.5, window.innerWidth*0.5*0.5)
    });
})

$(document).ready(function() {
    //$("#graph").fadeTo(0, 0);
    //$("#main-graph-stats").fadeTo(0, 0);
    let graphContainer = $("#graph-container")[0];
    chart = LightweightCharts.createChart(graphContainer, {
        width: Math.max(600, window.innerWidth*0.5),
        height: Math.max(600*0.5, window.innerWidth*0.5*0.5)
    });

    lineSeries = chart.addLineSeries();
    chart.applyOptions({
        layout: {
            backgroundColor: "#131722",
            textColor: "rgb(255, 255, 255)"
        },
        grid: {
            vertLines: {
                color: '#242938',
                style: 1,
                visible: true,
            },
            horzLines: {
                color: '#242938',
                style: 1,
                visible: true,
            },
        },
        watermark: {
            color: 'rgba(255, 255, 255, 0.6)',
            visible: true,
            fontSize: 24,
            horzAlign: 'left',
            vertAlign: 'bottom',
        },
        priceScale: {
            mode: 2
        },
        timeScale: {
        },
    });

    // auto select the search bar when the user starts typing.
    $(document).keypress(function() {
        let searchbar = $("#search-input")[0];
        if (!$("#search-input").is(":focus")) {
            searchbar.focus();
            searchbar.select();
        }
    });

    $("#search-form").submit(function(event) {
        try {
            let word = $("#search-input").val();
            //let graph = $("#graph")[0];

            //$("#graph").fadeTo(0, 0);
            //graph.src = "/api/words/" + word + "/graph";
            //
            generateSocials(word);
            

            $.get("/api/words/" + word + "/historical_data", function(data) {
                chart.applyOptions({
                    watermark: {
                        text: 'Performance of stocks containing "' + word + '"',
                    }
                });

                lineSeries.setData(data.chart);
                chart.timeScale().fitContent();
            });

            $.get("/api/words/" + word + "/metadata", function(data) {
                let stats = $(".graph-stats");
                for (let i=0; i<2; ++i) {
                    item = stats[i];
                    item.innerHTML = data;
                };
            });
        } catch (error) {
            event.preventDefault();

            throw error;
        }

        event.preventDefault();
    });

    let query = new URLSearchParams(window.location.search);

    if (query.get("word") != undefined) {
        $("#search-input").val(query.get("word"));
        $("#search-submit").click();
    }
});
