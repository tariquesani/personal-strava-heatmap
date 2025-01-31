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

def create_base_map(center):
    """Create a base map centered at the given coordinates."""
    base_map = folium.Map(
        location=center,
        zoom_start=15,
        control_scale=True,
        tiles=None
    )
    # Add tile layers
    folium.TileLayer(
        tiles='OpenStreetMap',
        name='Street',
        control=True,
        show=True
    ).add_to(base_map)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
        control=True,
        overlay=False,
        show=False
    ).add_to(base_map)
    return base_map

def add_legend(map_obj, activity_count, start_date, end_date):
    """Add a legend to the map."""
    legend_html = LEGEND_HTML_TEMPLATE.format(
        activity_count=activity_count,
        start_date=start_date.strftime('%d-%b-%Y'),
        end_date=end_date.strftime('%d-%b-%Y')
    )
    map_obj.get_root().html.add_child(folium.Element(legend_html))

def process_activities(activities):
    """Process activities to extract points and date range."""
    points = []
    start_date = datetime.strptime(activities[0]['start_date'][:10], '%Y-%m-%d')
    end_date = start_date

    for activity in activities:
        if activity.get("map"):
            points.extend(polyline.decode(activity["map"]))
            activity_date = datetime.strptime(activity['start_date'][:10], '%Y-%m-%d')
            start_date = min(start_date, activity_date)
            end_date = max(end_date, activity_date)
    
    return points, start_date, end_date

def generate_heatmap(activities):
    """Generate a heatmap from activity GPS data."""
    if not activities:
        return "No activities found."

    # Center map on first activity's starting point
    map_center = [activities[0]['start_lat'], activities[0]['start_lng']]
    heatmap = create_base_map(map_center)
    points, start_date, end_date = process_activities(activities)

    # Add heatmap layer if points exist
    if points:
        heatmap_layer = plugins.HeatMap(
            points,
            name='Heatmap',
            control=True,
            radius=6,
            blur=2,
            scaleRadius=True
        )
        heatmap.add_child(heatmap_layer)

    # Add fullscreen control and layer control
    plugins.Fullscreen(position="topright", force_separate_button=True).add_to(heatmap)
    folium.LayerControl(position='topright').add_to(heatmap)
    add_legend(heatmap, len(activities), start_date, end_date)

    return heatmap._repr_html_()

def generate_heatmap_with_time(activities):
    """Generates a map visualization with a heatmap that changes over time."""
    if not activities:
        return "No activities found."

    # Sort activities by date
    activities.sort(key=lambda x: x["start_date"])
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

            # Update point frequencies
            for lat, lng in points:
                point_key = (round(lat, 5), round(lng, 5))
                for t in range(timestep, len(activities)):
                    point_freq[point_key][t] += 1

            # Add timestamp label
            start_time = datetime.fromisoformat(activity["start_date"].replace("Z", "+00:00"))
            time_labels.append(start_time.strftime("%Y-%m-%d %H:%M"))

    heatmap_data = []
    all_points = list(point_freq.keys())

    # Create heatmap data for each timestep
    for t in range(len(activities)):
        timestep_data = [
            [lat, lng, point_freq[(lat, lng)][t]]
            for lat, lng in all_points
            if point_freq[(lat, lng)][t] > 0
        ]
        heatmap_data.append(timestep_data)

    # Calculate map center
    avg_lat = sum(lat for lat, _ in all_points) / len(all_points)
    avg_lng = sum(lng for _, lng in all_points) / len(all_points)
    heatmap = create_base_map([avg_lat, avg_lng])

    # Add the heatmap with time layer
    heatmap_layer = plugins.HeatMapWithTime(
        heatmap_data,
        index=time_labels,
        auto_play=True,
        position='topleft',
        max_opacity=0.8,
        min_opacity=0.3,
        radius=5,
        name='Heatmap'
    )
    heatmap_layer.add_to(heatmap)

    add_legend(heatmap, len(activities), start_date, end_date)
    plugins.Fullscreen(position="topright", force_separate_button=True).add_to(heatmap)
    folium.LayerControl().add_to(heatmap)

    return heatmap._repr_html_()

def generate_heatmap_one_ata_time(activities):
    """Generates a map visualization with routes for each activity, shown one at a time."""
    if not activities:
        return "No activities found."

    # Sort activities by date
    activities.sort(key=lambda x: x["start_date"])
    time_labels = []
    start_date = datetime.strptime(activities[0]['start_date'][:10], '%Y-%m-%d')
    end_date = start_date
    map_center = [activities[0]['start_lat'], activities[0]['start_lng']]
    heatmap = create_base_map(map_center)
    heatmap_data = []

    # Process each activity
    for activity in activities:
        if "map" in activity and activity["map"]:
            points = polyline.decode(activity["map"])
            start_time = datetime.fromisoformat(activity["start_date"].replace("Z", "+00:00"))
            time_labels.append(start_time.strftime("%Y-%m-%d %H:%M"))
            activity_date = datetime.strptime(activity['start_date'][:10], '%Y-%m-%d')
            start_date = min(start_date, activity_date)
            end_date = max(end_date, activity_date)
            heatmap_data.append([[lat, lon] for lat, lon in points])

    # Add HeatMapWithTime plugin to the map
    heatmap_layer = plugins.HeatMapWithTime(
        heatmap_data,
        index=time_labels,
        position='topleft',
        auto_play=True,
        max_opacity=0.8,
        min_opacity=0.3,
        radius=5,
        name='Heatmap'
    )
    heatmap_layer.add_to(heatmap)

    add_legend(heatmap, len(activities), start_date, end_date)
    plugins.Fullscreen(position="topright", force_separate_button=True).add_to(heatmap)
    folium.LayerControl().add_to(heatmap)

    return heatmap._repr_html_()