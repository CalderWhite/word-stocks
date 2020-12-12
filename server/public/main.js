// not much of this is fault tolerant. I am okay with that for now.

let graphContainer;
let lineSeries;
function fadeInGraph() {
    $("#graph").fadeTo(400, 1);
    $("#main-graph-stats").fadeTo(400, 1);
}

$(document).ready(function() {
    //$("#graph").fadeTo(0, 0);
    //$("#main-graph-stats").fadeTo(0, 0);
    let graphContainer = $("#graph-container")[0];
    chart = LightweightCharts.createChart(graphContainer, {
        width: window.innerWidth*0.5,
        height: window.innerWidth*0.5*0.5
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
        let word = $("#search-input").val();
        //let graph = $("#graph")[0];

        //$("#graph").fadeTo(0, 0);
        //graph.src = "/api/words/" + word + "/graph";

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

        event.preventDefault();
    });
});
