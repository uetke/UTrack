import os

import h5py

import numpy as np

# from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Span, HoverTool, LinearColorMapper
from bokeh.models.widgets import Button
from bokeh.plotting import figure
from bokeh.server.server import Server
import pims
import trackpy as tp
# from lib.track_2d import find_particles

data_dir = '/home/aquiles/Documents/Data/Tracking/run100nm'
filename = 'data.h5'
file = h5py.File(os.path.join(data_dir, filename))
data = file['Basler data']
total_intensity = np.sum(np.sum(data[:,:,:],1),1)
min_value = np.min(data)
max_value = np.max(data)
Nframes = data.shape[0]
Nx = data.shape[2]
Ny = data.shape[1]
total_intensity = total_intensity/Nx*Ny
frames = np.arange(0, Nframes, 1)

def initial_plots(doc):
    color_mapper = LinearColorMapper(palette="Viridis256", low=min_value, high=max_value)
    source = ColumnDataSource(data=dict(image=[data[0, :, :]]))
    p = figure(x_range=(0, Nx), y_range=(0, Ny))
    p.image(image='image', x=0, y=0, dw=Nx, dh=Ny, source=source, color_mapper=color_mapper)
    hove = HoverTool(tooltips=[("x", "$x"), ("y", "$y"), ("Intensity", "@image")])
    p.add_tools(hove)

    f2 = figure()
    f2.line(frames, total_intensity, line_width=2)
    hover = HoverTool(tooltips=[("Frame", "@x"), ("Intensity", "@y")])
    f2.add_tools(hover)
    slider = Slider(start=0, end=(Nframes - 1), value=0, step=1, title="Frame")

    vertical_line = Span(location=0,
                         dimension='height', line_color='green',
                         line_dash='dashed', line_width=3)
    f2.add_layout(vertical_line)

    def update(attr, old, new):
        source.data = dict(image=[data[slider.value, :, :]])
        vertical_line.location = slider.value

    slider.on_change('value', update)

    first_row = column(p, slider)
    second_row = column(f2)

    layout = row(first_row, second_row)
    doc.add_root(layout)


def trackpy_initial(doc):
    color_mapper = LinearColorMapper(palette="Viridis256", low=min_value, high=max_value)
    source = ColumnDataSource(data=dict(image=[data[0, :, :]]))

    f1 = figure(x_range=(0, Nx), y_range=(0, Ny))
    f1.image(image='image', x=0, y=0, dw=Nx, dh=Ny, source=source, color_mapper=color_mapper)

    center_source = ColumnDataSource(data=dict(x=[], y=[]))
    f1.circle(x='x', y='y',source=center_source, radius=3, fill_alpha=0)

    slider = Slider(start=0, end=(Nframes - 1), value=0, step=1, title="Frame")
    def update(attr, old, new):
        source.data = dict(image=[data[slider.value, :, :]])
        centers = tp.locate(data[slider.value, :, :], 9, minmass=250)
        # centers = find_particles(data[slider.value, :, :])
        center_source.data = dict(x=centers['x'], y=centers['y'])

    slider.on_change('value', update)

    doc.add_root(f1)
    doc.add_root(slider)


def main(doc):
    initial_plots(doc)
    trackpy_initial(doc)
    doc.title = 'Traces'

server = Server({'/': main}, num_procs=1)
server.start()

if __name__ == '__main__':
    print('Opening Bokeh application on http://localhost:5006/')

    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()