$(document).ready(function() {
    var currentLayer = null;
    var map = TETHYS_MAP_VIEW.getMap();
    var popupContainer = document.getElementById('popup');
    var popupOverlay = new ol.Overlay({
        element: popupContainer,
    });

    map.addOverlay(popupOverlay);
    $("#query-form").on("submit", function(event) {
        event.preventDefault();
        let formData = new FormData(this);
        formData.append('method', 'update_map');


        fetch('.', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'An unknown error occurred');
                });
            }
            return response.json();
        }).then(data => {
            const features = data.geojson.features;

            if (features.length === 0) {
                TETHYS_APP_BASE.alert("danger", "No earthquakes found for the selected date range.", "danger");
                return;
            }

            let newPointSource = new ol.source.Vector();

            features.forEach((feature) => {
                const coords = feature.geometry.coordinates;
                const properties = feature.properties;
                const lonLat = ol.proj.fromLonLat([coords[0], coords[1]]);

                let olFeature = new ol.Feature({
                    geometry: new ol.geom.Point(lonLat),
                    metadata: properties
                });

                olFeature.setStyle(new ol.style.Style({
                    image: new ol.style.Circle({
                        radius: 6,
                        fill: new ol.style.Fill({ color: 'orange' }),
                        stroke: new ol.style.Stroke({
                            color: 'black',
                            width: 1
                        })
                    })
                }));

                newPointSource.addFeature(olFeature);
            });

            if (currentLayer) {
                map.removeLayer(currentLayer);
            }

            currentLayer = new ol.layer.Vector({
                source: newPointSource,
                name: 'data_layer'
            });

            map.addLayer(currentLayer);
        }).catch(error => {
            console.error(error);
            TETHYS_APP_BASE.alert("danger", error.message);
        });
    });
  

    map.on('click', function(evt) {
        popupOverlay.setPosition(undefined);
        $("#popup").hide();
        map.forEachFeatureAtPixel(evt.pixel, function(feature, layer) {
            if (layer && layer.get('name') === 'data_layer') {
                const metadata = feature.getProperties().metadata;

                let popupContentHtml = "<table class='table table-striped table-bordered table-condensed'>";
                for (let key in metadata) {
                    if (key !== 'geometry') {
                        popupContentHtml += `<tr><th>${key}</th><td>${metadata[key]}</td></tr>`;
                    }
                }
                popupContentHtml += "</table>";

                $("#popup-content").html(popupContentHtml);
                $("#popup").show();

                popupOverlay.setPosition(evt.coordinate);
                return true;
            }
        });
        
    })


});
