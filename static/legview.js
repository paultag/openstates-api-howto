(function(global) {
    global.query = function(who, data) {
        $.getJSON('/data/' + who, function(data) {
            var fill = d3.scale.category20();

            d3.layout.cloud().size([300, 300])
                .words(data.map(function(d) {
                    console.log(d)
                    return {text: d[1][0], size: d[0] * 30};
                }))
                .padding(5)
                .rotate(function() { return ~~(Math.random() * 2) * 90; })
                .font("cantarell")
                .fontSize(function(d) { return d.size; })
                .on("end", draw)
                .start();

            function draw(words) {
            d3.select("body").append("svg")
                .attr("width", 300)
                .attr("height", 300)
                .append("g")
                .attr("transform", "translate(150,150)")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function(d) { return d.size + "px"; })
                .style("font-family", "cantarell")
                .style("fill", function(d, i) { return fill(i); })
                .attr("text-anchor", "middle")
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" +
                        d.rotate + ")";})
                .text(function(d) { return d.text; });
            }
        });
    }
}(this.exports || this));
