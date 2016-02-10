var ws = new WebSocket("ws://localhost:8080");

ws.onmessage = function draw(msg) {
  $('#graph').empty();
  
  var diameter = 300;

  var svg = d3.select('#graph').append('svg')
          .attr('width', diameter)
          .attr('height', diameter);

  var bubble = d3.layout.pack()
        .size([diameter, diameter])
        .value(function(d) {return d.size;})
        .padding(3);
  
  var nodes = bubble.nodes(processData(msg.data))
            .filter(function(d) { return !d.children; });
 
  var vis = svg.selectAll('circle').data(nodes);
  
  vis.enter().append('circle')
      .attr('transform', function(d) { return 'translate(' + d.x + ',' + d.y + ')'; })
      .attr('r', function(d) { return d.r; })
      .attr('class', function(d) { return d.className; });
  
  setColor(msg.data);

  var vis = svg.selectAll('circle').data(nodes);

  function processData(data) {
    var js = JSON.parse(data);
    var newDataSet = [];
    var total = Math.sqrt(js.dem*js.dem + js.rep*js.rep)/3;
    newDataSet.push({name: "rep", className: "rep", size: js.rep/total});
    newDataSet.push({name: "dem", className: "dem", size: js.dem/total});
    return {children: newDataSet};
  };

  function setColor(data) {
    var js = JSON.parse(data);
    console.log(js);
    if(js.dem_score == 0) {
      $('.dem').css('fill', 'rgb(0, 255, 0)');
    } else if(js.dem_score > 0) {
      $('.dem').css('fill', 'rgb('+ Math.floor(js.dem_score*255) + ', 20, 20)');
    } else {
      $('.dem').css('fill', 'rgb(20, 20, ' + Math.floor(js.dem_score*-255) +')');
    }

    if(js.rep_score == 0) {
      $('.rep').css('fill', 'rgb(0, 255, 0)');
    } else if(js.rep_score > 0) {
      $('.rep').css('fill', 'rgb('+ Math.floor(js.rep_score*255) + ', 20, 20)');
    } else {
      $('.rep').css('fill', 'rgb(20, 20, ' + Math.floor(js.rep_score*-255) + ')');
    }
  }
  
};