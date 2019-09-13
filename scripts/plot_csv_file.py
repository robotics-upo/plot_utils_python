#!/usr/bin/env python
'''
    This script loads a textfile in csv format generated by bag2csv script. 
    The csv file should have the first element of each row the time and represents two things:
    
     a) if no rows are given --> it generates the plot of all the rows against the time
     b) if a list of rows are given --> it only represents the list
     
    
    The figure is represented in Gtk backend so the user can zoom and save it at will
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import sys
import argparse

from gi.repository import Gtk
# gi.require_version('Gtk', '3.0')
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar


if __name__ == '__main__':
    # Argument handling
    parser = argparse.ArgumentParser(prog=sys.argv[0], description='A small script for plotting a file ')
    parser.add_argument('filename', nargs=1, help='Filename containing the data in CSV format')
    parser.add_argument('--x_label', nargs=1, help='String to display in the x axis')
    parser.add_argument('--y_label', nargs=1, help='String to display in the y axis')
    parser.add_argument('--cols', nargs=1, help='Set of cols to represent (examples: 3, 1:4)', default=['3'])
    parser.add_argument('--y_offset', nargs=1, type=float, default=0, help='Adds the offset to the y values');
    parser.add_argument('--scale', nargs=1, type=float, default=1);
    args = parser.parse_args(sys.argv[1:])
    
    # Setup matplotlib parameters
    SMALL_SIZE = 18
    MEDIUM_SIZE = 20
    
    # Setup the gtk window
    win = Gtk.Window()
    win.connect("delete-event", Gtk.main_quit)
    win.set_default_size(1000, 800)
    win.set_title("Plot csv file")
    
    
    # Performing the plots:
    s = np.loadtxt(args.filename[0], delimiter=',', skiprows=1)
    s[:,0] = s[:,0] - s[0,0]    # Set the init time to zero
    s[:,0] /= 1e9               # Convert to seconds
    f = Figure(figsize=(5, 4), dpi=100)
    ax1 = f.add_subplot(1,1,1)
    
    # Perform the offset and scaling of the data if necessary
    code = 's[:, ' + args.cols[0] + '] += ' + str(args.y_offset)
    exec(code)
    code = 's[:, ' + args.cols[0] + '] *= ' + str(args.scale)    
    exec(code)
    
    
    
    # Define plot code
    code = 'ax1.plot(s[:,0], s[:, ' + args.cols[0] + '], LineWidth=3)'
    exec(code)
    if (args.x_label != None):
        ax1.set_xlabel(args.x_label[0])
    if (args.y_label != None):
        ax1.set_ylabel(args.y_label[0])
    
    # Fonts
    for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] ):
        item.set_fontsize(MEDIUM_SIZE)
        
    for item in (ax1.get_xticklabels() + ax1.get_yticklabels()):
        item.set_fontsize(SMALL_SIZE)
    
    # Represent the figure in a GTK window with pan & zoom stuff
    vbox = Gtk.VBox()
    win.add(vbox)
    
    # Add canvas to vbox
    canvas = FigureCanvas(f)  # a Gtk.DrawingArea
    vbox.pack_start(canvas, True, True, 0)

    # Create toolbar
    toolbar = NavigationToolbar(canvas, win)
    vbox.pack_start(toolbar, False, False, 0)
    
    win.show_all()
    Gtk.main()
        
        
  
