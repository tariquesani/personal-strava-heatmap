import folium
import polyline
from folium import plugins

def generate_heatmap(activities):
    """
    Generates a heatmap based on activity data using polyline data.

    :param activities: List of activities containing map polyline data.
    :return: HTML string of the heatmap.
    """
    if not activities:
        return "No activities found."

    # Initialize map centered on the first activity
    first_activity = activities[0]
    map_center = [first_activity['start_lat'], first_activity['start_lng']]
    heatmap_map = folium.Map(location=map_center, zoom_start=16)

    # Extract coordinates from polylines
    heatmap_points = []
    for activity in activities:
        if activity.get("map"):
            decoded_points = polyline.decode(activity["map"])
            heatmap_points.extend(decoded_points)

    # Add heatmap layer if points exist
    if heatmap_points:
        plugins.HeatMap(heatmap_points).add_to(heatmap_map)

    # Return map as HTML
    return heatmap_map._repr_html_()
