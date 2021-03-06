import pandas as pd
from bokeh.io import output_file, show
from bokeh.layouts import column
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, sources, Select
from bokeh.models.widgets import Tabs, Panel
import json
import numpy as np
import datetime

with open('books.json', 'r') as infile:
    data_books = json.load(infile)

dfb = pd.DataFrame(data_books)
df = pd.DataFrame(data_books['list'])
df['updates'] = [count['updates'] for count in df['counts']]
df['editors'] = ["Con colaboradores" if count['collaborators'] != 0 else 'Sin colaboradores' for count in df['counts']]
df['creation'] = [datetime.datetime.strptime(date['dates']['created'].split('T')[0], '%Y-%m-%d').strftime('%d/%m/%y') for date in dfb['list']]
df['creation_plot'] = pd.to_datetime([date['dates']['created'] for date in dfb['list']])

df = df.sort_values('creation_plot')

df['iter'] = [i for i in range(len(df.index))]

source = ColumnDataSource(data={
	'title' : df['title'],
	'iter' : df['iter'],
	'updates' : df['updates'],
	'editors' : df['editors'],
	'creation': df['creation'],
	'creation_plot': df['creation_plot']
})

mapper = CategoricalColorMapper(
	factors=['Con colaboradores', 'Sin colaboradores'],
	palette=['red', 'blue']
)

hover = HoverTool(tooltips=[
	("Título", '@title'),
	("Número de actualizaciones", '@updates'),
	("Fecha de creación", '@creation')
])

p0 = figure(x_axis_label='Cursos',
          y_axis_label='Número de Actualizaciones',
		  tools=[hover, 'wheel_zoom', 'reset', 'pan'],
		  plot_width=1000)

p0.circle('iter', 'updates', size=8, source=source, color={
	'field': 'editors', 'transform': mapper
}, legend='editors')

output_file('actualizaciones.html')
show(p0)

with open('traffic.json', 'r') as infile:
    data_traffic = json.load(infile)

df_traffic = pd.DataFrame(data_traffic)
df_traffic = pd.DataFrame.transpose(df_traffic)
print(df_traffic.info())

visitas_totales = sum([visita.get('total') if visita.get('total') != None else 0 for visita in df_traffic.traffic.values])
visitas_unicas = sum([visita.get('unique') if visita.get('unique') != None else 0 for visita in df_traffic.traffic.values])
descargas = sum([visita.get('downloads') if visita.get('downloads') != None else 0 for visita in df_traffic.traffic.values])

print('{} visitas totales\n{} visitas únicas\n{} descargas'.format(visitas_totales, visitas_unicas, descargas))

p1 = figure(x_axis_label='Fecha de creación o importación', y_axis_label='Número de libros', x_axis_type='datetime',
		  tools=[hover, 'wheel_zoom', 'reset', 'pan'], plot_width=1000)
		
p1.line('creation_plot', 'iter', source=source, line_dash='2 2', line_alpha=0.8, line_width=8, line_join='bevel', line_dash_offset=2)

output_file('progreso.html')
show(p1)