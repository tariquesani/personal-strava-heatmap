from datetime import datetime, timezone
from collections import defaultdict
from typing import List, Dict, Tuple, Any

import folium
import polyline
from folium import plugins
from bottle import template
from services.polylinewithtime_plugin import PolylineWithTime

LEGEND_HTML = '''
<div style="position: fixed; top: 10px; left: 50px; width: 250px; z-index: 9999;
    background-color: white; padding: 10px; border: 2px solid lightgrey; border-radius: 6px;">
    <p style="margin-bottom: 0;">
        <strong>Activities:</strong> {activity_count}<br>
        <strong>Date: </strong>{start_date} to {end_date}
    </p>
</div>
'''


def create_base_map(center: List[float]) -> folium.Map:
    """Creates a base map with street and satellite layers."""
    base_map = folium.Map(location=center, zoom_start=15,
                          control_scale=True, tiles=None)

    folium.TileLayer(tiles='OpenStreetMap', name='Street',
                     control=True, show=True).add_to(base_map)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri', name='Satellite', control=True, overlay=False, show=False
    ).add_to(base_map)

    return base_map


def add_map_controls(map_obj: folium.Map, activities: List[Dict], start_date: datetime, end_date: datetime) -> None:
    """Adds legend, fullscreen control, and layer control to map."""
    legend_html = LEGEND_HTML.format(
        activity_count=len(activities),
        start_date=start_date.strftime('%d-%b-%Y'),
        end_date=end_date.strftime('%d-%b-%Y')
    )
    map_obj.get_root().html.add_child(folium.Element(legend_html))
    plugins.Fullscreen(position="topright",
                       force_separate_button=True).add_to(map_obj)
    folium.LayerControl(position='topright').add_to(map_obj)


def generate_heatmap(activities: List[Dict]) -> str:
    """Generates a static heatmap visualization of activities."""
    if not activities:
        return "No activities found."

    map_obj = create_base_map(
        [activities[0]['start_lat'], activities[0]['start_lng']])

    # Extract points and date range
    points = []
    start_date = end_date = datetime.strptime(
        activities[0]['start_date'][:10], '%Y-%m-%d')

    for activity in activities:
        if activity.get("map"):
            points.extend(polyline.decode(activity["map"]))
            activity_date = datetime.strptime(
                activity['start_date'][:10], '%Y-%m-%d')
            start_date = min(start_date, activity_date)
            end_date = max(end_date, activity_date)

    if points:
        plugins.HeatMap(points, name='Heatmap', control=True,
                        radius=6, blur=2, scaleRadius=True).add_to(map_obj)

        # Fit map bounds to points
        bounds = [[min(p[0] for p in points), min(p[1] for p in points)],
                  [max(p[0] for p in points), max(p[1] for p in points)]]
        map_obj.fit_bounds(bounds)

    add_map_controls(map_obj, activities, start_date, end_date)
    return map_obj._repr_html_()


def generate_heatmap_one_ata_time(activities: List[Dict]) -> str:
    """Generates a map visualization showing one activity at a time as a heatmap."""
    if not activities:
        return "No activities found."

    activities.sort(key=lambda x: x["start_date"])
    start_date = end_date = datetime.strptime(
        activities[0]['start_date'][:10], '%Y-%m-%d')
    map_obj = create_base_map(
        [activities[0]['start_lat'], activities[0]['start_lng']])

    heatmap_data = []
    time_labels = []

    for activity in activities:
        if activity.get("map"):
            points = polyline.decode(activity["map"])
            start_time = datetime.fromisoformat(
                activity["start_date"].replace("Z", "+00:00"))
            time_labels.append(start_time.strftime("%Y-%m-%d %H:%M"))
            activity_date = datetime.strptime(
                activity['start_date'][:10], '%Y-%m-%d')
            start_date = min(start_date, activity_date)
            end_date = max(end_date, activity_date)
            heatmap_data.append([[lat, lon] for lat, lon in points])

    plugins.HeatMapWithTime(
        heatmap_data, index=time_labels, position='topleft', auto_play=True,
        max_opacity=0.8, min_opacity=0.3, radius=5, name='Heatmap'
    ).add_to(map_obj)

    add_map_controls(map_obj, activities, start_date, end_date)
    return map_obj._repr_html_()


def generate_heatmap_with_time(activities: List[Dict]) -> str:
    """Generates a time-based heatmap visualization with accumulated points."""
    if not activities:
        return "No activities found."

    activities.sort(key=lambda x: x["start_date"])
    point_freq = defaultdict(lambda: [0] * len(activities))
    time_labels = []
    start_date = end_date = datetime.strptime(
        activities[0]['start_date'][:10], '%Y-%m-%d')

    # Process activities and build frequency map
    for timestep, activity in enumerate(activities):
        if activity.get("map"):
            points = polyline.decode(activity["map"])
            activity_date = datetime.strptime(
                activity['start_date'][:10], '%Y-%m-%d')
            start_date = min(start_date, activity_date)
            end_date = max(end_date, activity_date)

            for lat, lng in points:
                point_key = (round(lat, 5), round(lng, 5))
                for t in range(timestep, len(activities)):
                    point_freq[point_key][t] += 1

            time_labels.append(datetime.fromisoformat(activity["start_date"].replace("Z", "+00:00"))
                               .strftime("%Y-%m-%d %H:%M"))

    # Generate heatmap data
    all_points = list(point_freq.keys())
    heatmap_data = [
        [[lat, lng, point_freq[(lat, lng)][t]]
         for lat, lng in all_points if point_freq[(lat, lng)][t] > 0]
        for t in range(len(activities))
    ]

    # Create and configure map
    map_center = [sum(lat for lat, _ in all_points) / len(all_points),
                  sum(lng for _, lng in all_points) / len(all_points)]
    map_obj = create_base_map(map_center)

    plugins.HeatMapWithTime(
        heatmap_data, index=time_labels, auto_play=True, position='topleft',
        max_opacity=0.8, min_opacity=0.3, radius=5, name='Heatmap'
    ).add_to(map_obj)

    add_map_controls(map_obj, activities, start_date, end_date)
    return map_obj._repr_html_()


def generate_routes_map(activities: List[Dict]) -> str:
    """Generates a map with polylines showing activity routes over time."""
    if not activities:
        return "No activities found."

    map_obj = create_base_map(
        [activities[0]['start_lat'], activities[0]['start_lng']])
    start_date = end_date = datetime.strptime(
        activities[0]['start_date'][:10], '%Y-%m-%d')

    polylines = []
    for activity in activities:
        if activity.get("map"):
            date = datetime.fromisoformat(activity["start_date"])
            date = date if date.tzinfo else date.replace(tzinfo=timezone.utc)
            activity_date = datetime.strptime(
                activity['start_date'][:10], '%Y-%m-%d')
            start_date = min(start_date, activity_date)
            end_date = max(end_date, activity_date)

            polylines.append({
                "coords": polyline.decode(activity["map"]),
                "time": date.strftime("%Y-%m-%d %H:%M")
            })

    polylines.sort(key=lambda x: x["time"])
    available_times = sorted(set(p["time"] for p in polylines))

    PolylineWithTime(polylines, available_times, control=False).add_to(map_obj)
    add_map_controls(map_obj, activities, start_date, end_date)

    return map_obj._repr_html_()
