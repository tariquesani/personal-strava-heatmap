import folium
import polyline
from folium import plugins
from datetime import datetime


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

    # Initialize date tracking
    start_date = datetime.strptime(activities[0]['start_date'][:10], '%Y-%m-%d')
    end_date = start_date

    # Collect all GPS points and track date range
    points = []
    for activity in activities:
        if activity.get("map"):
            points.extend(polyline.decode(activity["map"]))
            activity_date = datetime.strptime(activity['start_date'][:10], '%Y-%m-%d')
            start_date = min(start_date, activity_date)
            end_date = max(end_date, activity_date)

    if points:
        plugins.HeatMap(points, radius=6, blur=2, scaleRadius=True).add_to(heatmap)

    # Format dates
    date_format = '%b %d, %Y'
    start_str = start_date.strftime(date_format)
    end_str = end_date.strftime(date_format)

    # Create the legend HTML
    legend_html = f'''
    <div style="
        position: fixed; 
        top: 10px; 
        left: 50px; 
        width: 250px;
        z-index: 1000;
        background-color: white;
        padding: 10px;
        border: 2px solid lightgrey;
        border-radius: 6px;
        ">
        <p style="margin-bottom: 0;"><strong>Activities:</strong> {len(activities)}<br>
        <strong>Date: </strong>{start_str} to {end_str}</p>
    </div>
    '''

    # Add the legend to the map
    heatmap.get_root().html.add_child(folium.Element(legend_html))

    return heatmap._repr_html_()
