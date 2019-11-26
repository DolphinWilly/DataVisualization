import numpy as np
import pandas as pd

from bokeh.models import ColumnDataSource, TextInput, Button
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.io import curdoc,show


doc = curdoc()


table = [[1,2,3,4,1],[2,3,4,5,2],[3,4,5,6,3],[4,5,6,7,4]]
df = pd.DataFrame(table, columns=['a','b','c','d','e'])
colors = ["navy", "firebrick", "red", "darkorchid", "hotpink", "black", "pink"]
next_group = 0

source = ColumnDataSource(data = {'x':[], 'y':[], 'label':[], 'colors':[]})
plot = figure(width=400, plot_height=300, title=None, tools='pan')

text_input = TextInput(value="ab", title="Label:")
button = Button(label="back", button_type="success", width = 100)

#plot.line(x='x', y= 'y', source = source1, legend_label = 'label', line_width=2, color=colors[next_group], muted_alpha = 0.1)
plot.multi_line(xs='x', ys= 'y', source = source, legend_field = 'label', line_width=2, color='colors', muted_alpha = 0.1)
plot.legend.location = "top_left"
plot.legend.click_policy="mute"


def update_plot(attrname, old, new):
    global next_group

    choice =  text_input.value
    n = len(df['e'])
    cl = [char for char in choice]

    # create a new dict to set up the new source wihtout getting "columns must be of same length" warnings
    new_data = {'x': [df['e'].tolist() * len(cl)], 'y': [[x for e in cl for x in df[e].tolist()]], 'label': [choice], 'colors': [colors[next_group]]}

    # total update 
    #source1.data = new_data

    # use stream for continious updates
    source.stream(new_data)

    next_group += 1

def update_back():
    global next_group
    if next_group <= 0:
        return
    next_group -= 1
    print(next_group)
    dd = {'x': source.data['x'][:next_group], 'y': source.data['y'][:next_group], \
    'label': source.data['label'][:next_group], 'colors': source.data['colors'][:next_group]}
    source.data = dd


button.on_click(update_back)

text_input.on_change('value', update_plot)

layout = row(plot, column(text_input, button))

doc.add_root(layout)
