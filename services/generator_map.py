import folium
import polyline
from folium import plugins


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
    heatmap = folium.Map(location=map_center, zoom_start=15)
    
    # Add fullscreen control
    plugins.Fullscreen(position="topright", force_separate_button=True).add_to(heatmap)

    # Collect all GPS points from activity polylines
    points = [
        point 
        for activity in activities 
        if activity.get("map")
        for point in polyline.decode(activity["map"])
    ]

    if points:
        plugins.HeatMap(points, radius=6, blur=2, scaleRadius=True).add_to(heatmap)

    return heatmap._repr_html_()
