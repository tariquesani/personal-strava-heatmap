from branca.element import Element, Figure
from folium.elements import JSCSSMixin
from folium.map import Layer
from folium.template import Template
import json


class PolylineWithTime(JSCSSMixin, Layer):
    """
    A Folium plugin to display polylines on a map, updating them dynamically based on time.
    """

    _template = Template("""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = L.layerGroup();
            
            (function() {
                try {
                    // Extract polylines and timestamps from Python
                    const polylines = {{ this.polylines | tojson | safe }};
                    const availableTimes = {{ this.available_times | tojson | safe }}.map(date => new Date(date).getTime());
                    
                    // Get Folium-generated map object
                    var map = {{ this._parent.get_name() }};
                    
                    // Store existing layers
                    var existingLayers = [];
                    map.eachLayer(function(layer) {
                        existingLayers.push(layer);
                    });
                    
                    // Add time dimension if it doesn't exist
                    if (!map.timeDimension) {
                        // Create time dimension instance
                        map.timeDimension = new L.TimeDimension({
                            times: availableTimes,
                            currentTime: availableTimes[0]
                        });
                        
                        // Set up time control
                        var timeDimensionControl = new L.Control.TimeDimension({
                            loopButton: true,
                            timeSliderDragUpdate: true,
                            displayDateFormat: 'YYYY-MM-DD HH:mm:ss',
                            position: 'topleft'
                        });
                        map.addControl(timeDimensionControl);
                        
                        // Re-add any existing layers that were on the map
                        existingLayers.forEach(function(layer) {
                            if (layer instanceof L.TileLayer) {
                                layer.addTo(map);
                            }
                        });
                    }

                    // Function to update polylines based on selected time
                    function updatePolylines(timestamp) {
                        {{this.get_name()}}.clearLayers();
                        const currentDate = new Date(timestamp);

                        polylines.forEach((poly, index) => {
                            const polyDate = new Date(poly.time);
                            if (polyDate.getTime() === currentDate.getTime()) {
                                const line = L.polyline(poly.coords, {
                                    color: `hsl(${index * 60}, 70%, 50%)`,
                                    weight: 3
                                });
                                {{this.get_name()}}.addLayer(line);
                                map.fitBounds(line.getBounds());
                            }
                        });
                    }

                    // Update polylines when time changes
                    map.timeDimension.on('timeload', function(data) {
                        updatePolylines(map.timeDimension.getCurrentTime());
                    });

                    // Initial update
                    updatePolylines(map.timeDimension.getCurrentTime());
                    
                    {{this.get_name()}}.addTo(map);
                    
                } catch (error) {
                    console.error("Error in PolylineWithTime plugin:", error);
                }
            })();
        {% endmacro %}
    """)

    default_js = [
        (
            "iso8601",
            "https://cdn.jsdelivr.net/npm/iso8601-js-period@0.2.1/iso8601.min.js",
        ),
        (
            "leaflet.timedimension.min.js",
            "https://cdn.jsdelivr.net/npm/leaflet-timedimension@1.1.1/dist/leaflet.timedimension.min.js",
        ),
    ]

    default_css = [
        (
            "leaflet.timedimension.control.min.css",
            "https://cdn.jsdelivr.net/npm/leaflet-timedimension@1.1.1/dist/leaflet.timedimension.control.css",
        )
    ]

    def __init__(self, polylines, available_times, name=None, overlay=True, control=True, show=True):
        """
        :param polylines: A list of dictionaries containing 'coords' (list of lat/lon points) and 'time' (ISO 8601 timestamp).
        :param available_times: A list of timestamps in ISO 8601 format representing available time steps.
        """
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self._name = "PolylineWithTime"

        # Ensure JSON serialization is valid
        try:
            self.polylines = json.loads(json.dumps(polylines))
            self.available_times = json.loads(json.dumps(available_times))
        except Exception as e:
            raise ValueError(f"Error in JSON serialization: {e}")

    def render(self, **kwargs):
        super().render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), "You cannot render this Element if it is not in a Figure."

        figure.header.add_child(Element("""
            <script>
                console.log("PolylineWithTime plugin loaded successfully.");
            </script>
        """))