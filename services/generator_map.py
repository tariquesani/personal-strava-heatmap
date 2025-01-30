import folium
import polyline
from folium import plugins
from datetime import datetime
from collections import defaultdict

# Global legend HTML template
LEGEND_HTML_TEMPLATE = '''
<div style="
    position: fixed; 
    top: 10px; 
    left: 50px; 
    width: 250px;
    z-index: 9999;
    background-color: white;
    padding: 10px;
    border: 2px solid lightgrey;
    border-radius: 6px;
    ">
    <p style="margin-bottom: 0;"><strong>Activities:</strong> {activity_count}<br>
    <strong>Date: </strong>{start_date} to {end_date}</p>
</div>
'''

def generate_heatmap(activities):
    """
    Generates a heatmap visualization from activity GPS data.
    
    Args:
        activities: List of activity dictionaries containing map polyline data
        
    Returns:
        str: HTML representation of the heatmap, or error message if no activities
    """
    if not activities:
        return "No activities found."

    # Center map on first activity's starting point
    map_center = [activities[0]['start_lat'], activities[0]['start_lng']]
    
    # Create the base map with OpenStreetMap as default
    heatmap = folium.Map(
        location=map_center,
        zoom_start=15,
        control_scale=True,
        tiles= None  # Initialize with no tiles
    )
    
    # Add tile layers
    folium.TileLayer(
        tiles='OpenStreetMap',
        name='Street',
        control=True,
        show=True
    ).add_to(heatmap)
    
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
        control=True,
        overlay=False,
        show=False
    ).add_to(heatmap)
    
    # Collect all GPS points and track date range
    points = []
    start_date = datetime.strptime(activities[0]['start_date'][:10], '%Y-%m-%d')
    end_date = start_date

    for activity in activities:
        if activity.get("map"):
            points.extend(polyline.decode(activity["map"]))
            activity_date = datetime.strptime(activity['start_date'][:10], '%Y-%m-%d')
            start_date = min(start_date, activity_date)
            end_date = max(end_date, activity_date)

    # Add heatmap layer
    if points:
        heat_data = points
        heatmap_layer = plugins.HeatMap(
            heat_data,
            name='Heatmap',
            control=True,
            radius=6,
            blur=2,
            scaleRadius=True
        )
        heatmap.add_child(heatmap_layer)

    # Add fullscreen control
    plugins.Fullscreen(position="topright", force_separate_button=True).add_to(heatmap)

    # Add layer control after all layers are added
    folium.LayerControl(position='topright').add_to(heatmap)
    
    # Create the legend HTML with higher z-index
    legend_html = LEGEND_HTML_TEMPLATE.format(
        activity_count=len(activities),
        start_date=start_date.strftime('%d-%b-%Y'),
        end_date=end_date.strftime('%d-%b-%Y')
    )

    # Add the legend to the map
    heatmap.get_root().html.add_child(folium.Element(legend_html))

    return heatmap._repr_html_()

def generate_heatmap_with_time(activities):
    # Sort activities by date
    activities.sort(key=lambda x: x["start_date"])

    # Create a dictionary to store points and their frequencies at each timestep
    point_freq = defaultdict(lambda: [0] * len(activities))
    time_labels = []
    start_date = datetime.strptime(activities[0]['start_date'][:10], '%Y-%m-%d')
    end_date = start_date

    # Process each activity
    for timestep, activity in enumerate(activities):
        if "map" in activity and activity["map"]:
            points = polyline.decode(activity["map"])
            activity_date = datetime.strptime(activity['start_date'][:10], '%Y-%m-%d')
            start_date = min(start_date, activity_date)
            end_date = max(end_date, activity_date)

            # For each point in this activity
            for lat, lng in points:
                # Round coordinates to reduce unique points
                point_key = (round(lat, 5), round(lng, 5))

                # Increment the weight for this point for this timestep and all future timesteps
                for t in range(timestep, len(activities)):
                    point_freq[point_key][t] += 1

            # Add timestamp label
            start_time = datetime.fromisoformat(activity["start_date"].replace("Z", "+00:00"))
            time_labels.append(start_time.strftime("%Y-%m-%d %H:%M"))

    # Convert to format needed for HeatMapWithTime
    heatmap_data = []
    all_points = list(point_freq.keys())

    # For each timestep, create a list of [lat, lng, weight] entries
    for t in range(len(activities)):
        timestep_data = [
            [lat, lng, point_freq[(lat, lng)][t]]
            for lat, lng in all_points
            if point_freq[(lat, lng)][t] > 0
        ]
        heatmap_data.append(timestep_data)

    # Calculate map center correctly
    avg_lat = sum(lat for lat, _ in all_points) / len(all_points)
    avg_lng = sum(lng for _, lng in all_points) / len(all_points)

    # Create the base map with only OpenStreetMap layer
    heatmap = folium.Map(
        location=[avg_lat, avg_lng],
        zoom_start=15,
        control_scale=True
    )

    # Add the heatmap directly to the map
    heatmap_layer = plugins.HeatMapWithTime(
        heatmap_data,
        index=time_labels,
        auto_play=True,
        position='topleft',
        max_opacity=0.8,
        min_opacity=0.3,
        radius=3,
        name='Heatmap'  # This makes it show up in layer control
    )
    heatmap_layer.add_to(heatmap)

    # Create the legend HTML with higher z-index
    legend_html = LEGEND_HTML_TEMPLATE.format(
        activity_count=len(activities),
        start_date=start_date.strftime('%d-%b-%Y'),
        end_date=end_date.strftime('%d-%b-%Y')
    )

    # Add the legend to the map
    heatmap.get_root().html.add_child(folium.Element(legend_html))

    # Add layer control
    folium.LayerControl().add_to(heatmap)

    return heatmap._repr_html_()