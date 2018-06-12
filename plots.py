import pandas as pd
from bokeh.io import output_file, show
from bokeh.layouts import column
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, sources, Select
from bokeh.models.widgets import Tabs, Panel
import json
import numpy as np

with open('books.json', 'r') as infile:
    data_books = json.load(infile)

df = pd.DataFrame(data_books['list'])
df['iter'] = [i for i in range(len(df.index))]
df['updates'] = [count['updates'] for count in df['counts']]
df['editors'] = ["Con colaboradores" if count['collaborators'] != 0 else 'Sin colaboradores' for count in df['counts']]

source = ColumnDataSource(data={
	'title' : df['title'],
	'iter' : df['iter'],
	'updates' : df['updates'],
	'editors' : df['editors']
})

mapper = CategoricalColorMapper(
	factors=['Con colaboradores', 'Sin colaboradores'],
	palette=['red', 'blue']
)

hover = HoverTool(tooltips=[
	("Título", '@title'),
	("Número de actualizaciones", '@updates')
])

p = figure(x_axis_label='Cursos',
          y_axis_label='Número de Actualizaciones',
		  tools=[hover, 'wheel_zoom', 'reset', 'pan'])

p.circle('iter', 'updates', size=8, source=source, color={
	'field': 'editors', 'transform': mapper
}, legend='editors')

# show(p)

with open('traffic.json', 'r') as infile:
    data_traffic = json.load(infile)

df_traffic = pd.DataFrame(data_traffic)
df_traffic['title'] = [data_traffic[str(i)]['title'] for i in range(len(data_traffic))]
df_traffic['visitas_totales'] = []
df_traffic['visitas_unicas'] = []
df_traffic['descargas'] = []

# Recupero los datos necesarios
for i in range(len(data_traffic)):
    try:
        df_traffic['visitas_totales'].append(data_traffic[str(i)]['traffic']['total'])
    except:
        df_traffic['visitas_totales'].append(0)

    try:
        df_traffic['visitas_unicas'].append(data_traffic[str(i)]['traffic']['total'])
    except:
        df_traffic['visitas_unicas'].append(0)

    try:
        df_traffic['descargas'].append(data_traffic[str(i)]['traffic']['total'])
    except:
        df_traffic['descargas'].append(0)

# for i in range(len(data_traffic)):
# 	try:
# 	    if not data_traffic[str(i)]['platforms']['list']:
# 	        platforms.append(None)
# 	    else:
# 	        platforms.append(data_traffic[str(i)]['platforms']['list'])
# 	except:
# 	    platforms.append(None)

