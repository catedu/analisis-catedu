import pandas as pd
from bokeh.io import output_file, show
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, sources
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

show(p)
