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
df['colors'] = ['red' if count['collaborators'] != 0 else 'blue' for count in df['counts']]

source = ColumnDataSource(data={
	'title' : df['title'],
	'iter' : df['iter'],
	'updates' : df['updates'],
	'colors' : df['colors']
})

hover = HoverTool(tooltips=[
	("Título", '@title'),
])

p = figure(x_axis_label='Cursos',
          y_axis_label='Número de Actualizaciones',
		  tools=[hover])

p.circle('iter', 'updates', size=5, source=source, color='colors', legend="A ver")
show(p)
