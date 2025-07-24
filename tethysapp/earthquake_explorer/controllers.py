import requests
from tethys_sdk.layouts import MapLayout
from tethys_sdk.routing import controller
from .app import App
from tethys_sdk.gizmos import DatePicker, Button, SelectInput
from datetime import datetime, timedelta
from django.http import JsonResponse
import os # Add this

global start_date, end_date, min_magnitude
@controller(name="home")
class EarthquakeExplorerMap(MapLayout):
    app = App
    base_template = 'earthquake_explorer/base.html'
    template_name = 'earthquake_explorer/home.html'
    map_title = 'Earthquake Explorer'
    map_subtitle = 'Recent Earthquakes'
    default_map_extent = [-180, -90, 180, 90]
    max_zoom = 18
    min_zoom = 2
    show_properties_popup = True
    
    
    def get_context(self, request, *args, **kwargs):
        context=super().get_context(request, *args, **kwargs)
        today = datetime.now().strftime('%m-%d-%Y')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%m-%d-%Y')
        start_date=DatePicker(name='start_date',display_text='Start Date', format='mm-dd-yyyy',initial=yesterday, attributes={"class": "form-input"})
        end_date=DatePicker(name='end_date',display_text='End Date',format='mm-dd-yyyy',initial=today, attributes={"class": "form-input"})
        min_magnitude=SelectInput(
            name='min_magnitude',
            display_text='Minimum Magnitude',
            multiple=False,
            options=[
                ('1.0', '1.0'),
                ('2.0', '2.0'),
                ('3.0', '3.0'),
                ('4.0', '4.0'),
                ('5.0', '5.0'),
                ('6.0', '6.0'),
                ('7.0', '7.0'),
                ('8.0', '8.0'),
                ('9.0', '9.0')
            ],
            initial='5.0'
        )
        submit_btn = Button(display_text='Submit', name='submit', style='success', submit=True, attributes={'form': 'query-form'})

    # Generate the base context to add Gizmos to
        context['start_date'] = start_date
        context['end_date'] = end_date
        context['submit_btn'] = submit_btn
        context['min_magnitude'] = min_magnitude
        return context
 
    def update_map(self, request, *args, **kwargs):
        form_data = request.POST
        start_date = form_data.get('start_date')
        start_date = datetime.strptime(start_date, '%m-%d-%Y').strftime('%Y-%m-%d') if start_date else None
        end_date = form_data.get('end_date')
        end_date = datetime.strptime(end_date, '%m-%d-%Y').strftime('%Y-%m-%d') if end_date else None
        min_magnitude = form_data.get('min_magnitude', '5.0')
        if not start_date or not end_date:
            return JsonResponse({'error': 'Start date and end date are required.'}, status=400)
        url = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
        params = {
            'format': 'geojson',
            'starttime': start_date,
            'endtime': end_date,
            'minmagnitude': min_magnitude,
            'limit': '20000'
        }
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            earthquake_geojson = response.json()
        except Exception as e:
            print(f"Error fetching earthquake data: {e}")
            earthquake_geojson = {"type": "FeatureCollection", "features": []}
        return JsonResponse({
            'geojson': earthquake_geojson,
            'start_date': start_date,
            'end_date': end_date,
            'min_magnitude': min_magnitude
        }, status=200)
            
