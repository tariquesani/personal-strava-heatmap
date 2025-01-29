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
    

    # Format dates
    date_format = '%d-%b-%Y'
    start_str = start_date.strftime(date_format)
    end_str = end_date.strftime(date_format)

    # Create the legend HTML with higher z-index
    legend_html = f'''
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
        <p style="margin-bottom: 0;"><strong>Activities:</strong> {len(activities)}<br>
        <strong>Date: </strong>{start_str} to {end_str}</p>
    </div>
    '''

    # Add the legend to the map
    heatmap.get_root().html.add_child(folium.Element(legend_html))

    return heatmap._repr_html_()