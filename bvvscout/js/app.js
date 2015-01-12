/*global $, L, _ */
/*jslint browser:true */

var map;
$(document).ready(function() {
  "use strict";

  // create a map in the "map" div, set the view to a given place and zoom
  map = L.map('map').setView([52.516667, 13.383333], 12);

  // add an OpenStreetMap tile layer
  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  var containers;
  $.getJSON("data/all.geojson", function(data) {
    containers = data;
  })
  .done(function(){
    addContainers(containers);
  });


  var districts;
  $.getJSON("data/berlin-districts.geojson", function(data) {
    districts = data;
  })
  .done(function(){
    L.geoJson(districts, { style: {
      fillColor: "hotPink",
      color: "#2E85CB"
    }}).addTo(map);
  });

  function filterPoints(){
    var filterBrown = $("#linke").prop("checked");
    var filterWhite = $("#piraten").prop("checked");
    var filterGreen = $("#gruene").prop("checked");
    var filterColored = $("#spd").prop("checked");
    var colorFilters = {
      "linke": filterBrown,
      "piraten": filterWhite,
      "gruene": filterGreen,
      "spd": filterColored
    };
//     var filterPlz = $("#plz").val();
//     var filterSupplier = $("#supplier").val();
    var filterBezirk = $("#bezirk").val();
    var filterTyp = $("#typ").val();


    var filteredContainers = containers.features;
//     if (filterPlz !== "-1"){
//       filteredContainers = _.filter(filteredContainers, function(container){
//         return container.properties.plz === filterPlz;
//       });
//     }

    filteredContainers = _.filter(filteredContainers, function(container) {
      for (var color in colorFilters){
        if (colorFilters[color] && container.properties[color] === ""){
          return false;
        }
      }
      return true;
    });

//     if (filterSupplier !== ""){
//       filteredContainers = _.filter(filteredContainers, function(container) {
//         return container.properties.aufsteller === filterSupplier;
//       });
//     }


    if (filterBezirk !== ""){
      filteredContainers = _.filter(filteredContainers, function(container) {
        return container.properties.bezirk === filterBezirk;
      });
    }
    
    if (filterTyp !== ""){
      filteredContainers = _.filter(filteredContainers, function(container) {
        return container.properties.typ === filterTyp;
      });
    }

    addContainers(filteredContainers);
  }

  var allContainers = [];
  function addContainers(data){
    map.removeLayer(allContainers);
    allContainers = L.geoJson(data, {
      onEachFeature: function (feature, layer) {
        layer.bindPopup(data2html(feature));
      }

    }).addTo(map);
  }

  var data2html = function(item){
    // flatten the json
    var content = _.extend(item.properties,item.properties.data);
    delete content.data;

    var template = _.template($("#tooltip_tmpl").html());
    return template(content);
  };

  $("input").change(filterPoints);
  $("select").on("change", filterPoints);

});
