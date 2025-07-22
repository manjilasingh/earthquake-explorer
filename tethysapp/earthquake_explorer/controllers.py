import requests
from tethys_sdk.layouts import MapLayout
from tethys_sdk.routing import controller
from .app import App
from tethys_sdk.gizmos import DatePicker, Button
from datetime import datetime, timedelta
from django.http import JsonResponse
import os # Add this

global start_date, end_date
@controller(name="home", app_workspace=True)
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
        submit_btn = Button(display_text='Submit', name='submit', style='success', submit=True, attributes={'form': 'query-form'})

    # Generate the base context to add Gizmos to
        context['start_date'] = start_date
        context['end_date'] = end_date
        context['submit_btn'] = submit_btn
        return context
    
  
    def postTest(self, request, *args, **kwargs):
        form_data = request.POST
        print(f"Form data received: {form_data}")
        breakpoint()
        start_date = form_data.get('start_date')
        start_date = datetime.strptime(start_date, '%m/%d/%Y').date()
        start_date = str(start_date.strftime("%Y-%m-%d"))
        end_date = form_data.get('end_date')
        end_date = datetime.strptime(end_date, '%m/%d/%Y').date()
        end_date = str(end_date.strftime("%Y-%m-%d"))
        return JsonResponse({'success': True,
                            'input': form_data})
        
    def post(self, request, *args, **kwargs):
        form_data = request.POST
        
        start_date = form_data.get('start_date')
        start_date = datetime.strptime(start_date, '%m-%d-%Y').date()
        start_date = str(start_date.strftime("%Y-%m-%d"))
        end_date = form_data.get('end_date')
        end_date = datetime.strptime(end_date, '%m-%d-%Y').date()
        end_date = str(end_date.strftime("%Y-%m-%d"))
        return JsonResponse({'success': True,
                            'input': form_data})

    def compose_layers(self, request, map_view, app_workspace, *args, **kwargs):
        """
        Add layers to the MapLayout and create associated layer group objects.
        """

        url = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
        params = {
            'format': 'geojson',
            'starttime': '2023-01-01',
            'endtime': '2023-01-29',
            'minmagnitude': '5',
            'limit': '100'
        }
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            earthquake_geojson = response.json()
        except Exception as e:
            print(f"Error fetching earthquake data: {e}")
            earthquake_geojson = {"type": "FeatureCollection", "features": []}

        earthquake_layer = self.build_geojson_layer(
            geojson=earthquake_geojson,
            layer_name='earthquakes',
            layer_title='Earthquakes',
            layer_variable='earthquakes',
            visible=True,
            selectable=True,
            plottable=False,
        )

        layer_groups = [
            self.build_layer_group(
                id='earthquake-group',
                display_name='Earthquake Data',
                layer_control='checkbox',
                layers=[earthquake_layer]
            )
        ]

        return layer_groups

    @classmethod
    def get_vector_style_map(cls):
        return {
            'Point': {'ol.style.Style': {
                'image': {'ol.style.Circle': {
                    'radius': 6,
                    'fill': {'ol.style.Fill': {
                        'color': 'rgba(255, 0, 0, 0.9)',
                    }},
                    'stroke': {'ol.style.Stroke': {
                        'color': 'black',
                        'width': 1
                    }}
                }}
            }},
        }
        