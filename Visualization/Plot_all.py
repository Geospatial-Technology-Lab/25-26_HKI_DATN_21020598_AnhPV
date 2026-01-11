#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 15:08:15 2022
@author: Guoding_Chen
This program plots matrices and creates videos.
"""

import cv2
import numpy as np
import re
import h5py
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import os
import shapefile as shp

# Font settings
font1 = {'family': 'Arial', 'style': 'normal', 'weight': 'normal', 'size': 16}

# Base path
base_path = 'D:/Recheck/iHydroSlide3D_v1_1/Visualization'

# Create output directories
for folder in ["R", "W", "SM", "FS", "PF", "Volume"]:
    os.makedirs(os.path.join(base_path, folder), exist_ok=True)

# Clear output directories
for folder in ["R", "W", "SM", "FS", "PF", "Volume"]:
    folder_path = os.path.join(base_path, folder)
    for filename in os.listdir(folder_path):
        try:
            os.remove(os.path.join(folder_path, filename))
        except PermissionError:
            print(f"Could not delete {filename} in {folder_path}")

# Read control file
control_file_path = 'D:/Recheck/iHydroSlide3D_v1_1/Control.Project'
try:
    with open(control_file_path, 'r') as control_file:
        control_contents = control_file.readlines()
except FileNotFoundError:
    print(f"Control file not found: {control_file_path}")
    exit(1)

def get_control_value(key):
    try:
        line = re.sub(r'\s+', '', [s for s in control_contents if key in s][0])
        return float(line.split("#", 1)[0].split("=", 1)[1])
    except IndexError:
        print(f"Key {key} not found in control file")
        exit(1)

# Hydro and landslide parameters
XLLCorner_hydro = get_control_value("XLLCorner_Hydro")
YLLCorner_hydro = get_control_value("YLLCorner_Hydro")
nCols_hydro = get_control_value("NCols_Hydro")
nRows_hydro = get_control_value("NRows_Hydro")
cellSize_hydro = get_control_value("CellSize_Hydro")
XLLCorner_land = get_control_value("XLLCorner_Land")
YLLCorner_land = get_control_value("YLLCorner_Land")
nCols_land = get_control_value("NCols_Land")
nRows_land = get_control_value("NRows_Land")
cellSize_land = get_control_value("CellSize_Land")

print(f"Hydro domain: {int(nCols_hydro)}x{int(nRows_hydro)}, cellsize: {cellSize_hydro}")
print(f"Land domain: {int(nCols_land)}x{int(nRows_land)}, cellsize: {cellSize_land}")

# Extents
extent_hydro = [XLLCorner_hydro, XLLCorner_hydro + nCols_hydro * cellSize_hydro,
                YLLCorner_hydro, YLLCorner_hydro + nRows_hydro * cellSize_hydro]
extent_land = [XLLCorner_land, XLLCorner_land + nCols_land * cellSize_land,
               YLLCorner_land, YLLCorner_land + nRows_land * cellSize_land]

# Read boundary shapefile
shp_path = "D:/Recheck/iHydroSlide3D_v1_1/HydroBasics/Basin_boundary.shp"
try:
    sf = shp.Reader(shp_path)
    x = np.array([i[0] for shape in sf.shapeRecords() for i in shape.shape.points])
    y = np.array([i[1] for shape in sf.shapeRecords() for i in shape.shape.points])
except Exception as e:
    print(f"Error reading shapefile {shp_path}: {e}")
    exit(1)

# Color settings
NODATA_value = -9999
colorbar_R = 'YlGnBu'
colorbar_W = plt.get_cmap('GnBu', 8)
colorbar_SM = plt.get_cmap('YlGnBu', 8)
colorbar_PF = plt.get_cmap('BuPu', 10)
colorbar_Volume = plt.get_cmap('viridis_r', 6)
style_color_FS = np.array([(151, 0, 29), (219, 116, 93), (233, 245, 186),
                           (136, 189, 103), (100, 169, 77), (22, 120, 55)])
bounds_FS = np.array([0, 0.8, 1, 1.2, 1.4, 2, 3])
norm_FS = colors.BoundaryNorm(boundaries=bounds_FS, ncolors=7)
colorbar_FS = LinearSegmentedColormap.from_list('my_palette', style_color_FS / 255, N=7)

# Plotting
variable_list = ["R", "W", "SM", "FS3D", "PF", "FVolume"]
filename = 'D:/Recheck/iHydroSlide3D_v1_1/Results/Result_all.h5'
try:
    data = h5py.File(filename, 'r')
except FileNotFoundError:
    print(f"HDF5 file not found: {filename}")
    exit(1)

for group in data.keys():
    for dset in data[group].keys():
        print(f"Processing dataset: {dset}")
        try:
            variable_tag = dset.split("_", 2)[1]
            print(f"Variable tag: {variable_tag}")
            if variable_tag in variable_list:
                print(f"Plotting {variable_tag} for {dset}")
                variable_matrix = data[group][dset][:]
                variable_matrix = variable_matrix.astype(np.float32)
                variable_matrix[variable_matrix == NODATA_value] = np.nan
                variable_matrix = variable_matrix / 100
                Time_moment = dset.split("_", 2)[2]
                OutFigure_name = dset.split("_", 1)[1] + ".jpg"

                fig, ax = plt.subplots(figsize=(6, 6))
                plt.subplots_adjust(bottom=0.0, top=0.98, left=0.00, right=0.9)

                if variable_tag == "R":
                    variable_matrix[variable_matrix == 0] = 0.000001
                    im = ax.imshow(variable_matrix, extent=extent_hydro, cmap=colorbar_R,
                                   norm=colors.LogNorm(vmin=10**-1, vmax=10**3))
                    cb_label = 'R ($\mathrm{m^3/s}$)'
                    cb_pos = [-40, 1.25]
                    folder = "R"
                    cbar_ax = fig.add_axes([0.82, 0.35, 0.035, 0.3])
                elif variable_tag == "W":
                    im = ax.imshow(variable_matrix, extent=extent_hydro, cmap=colorbar_W, vmin=0, vmax=150)
                    cb_label = 'W ($\mathrm{mm}$)'
                    cb_pos = [-30, 1.25]
                    folder = "W"
                    cbar_ax = fig.add_axes([0.82, 0.35, 0.035, 0.3])
                elif variable_tag == "SM":
                    im = ax.imshow(variable_matrix, extent=extent_hydro, cmap=colorbar_SM, vmin=0, vmax=100)
                    cb_label = 'SM ($\%$)'
                    cb_pos = [-30, 1.25]
                    folder = "SM"
                    cbar_ax = fig.add_axes([0.82, 0.35, 0.035, 0.3])
                elif variable_tag == "FS3D":
                    im = ax.imshow(variable_matrix, extent=extent_land, cmap=colorbar_FS, norm=norm_FS)
                    cb_label = '$F_{s}$ (-)'
                    cb_pos = [-20, 1.18]
                    folder = "FS"
                    cbar_ax = fig.add_axes([0.86, 0.30, 0.035, 0.4])
                elif variable_tag == "PF":
                    im = ax.imshow(variable_matrix, extent=extent_land, cmap=colorbar_PF, vmin=0, vmax=1)
                    cb_label = '$P_{f}$ (-)'
                    cb_pos = [-25, 1.23]
                    folder = "PF"
                    cbar_ax = fig.add_axes([0.86, 0.35, 0.035, 0.3])
                elif variable_tag == "FVolume":
                    im = ax.imshow(variable_matrix, extent=extent_land, cmap=colorbar_Volume, vmin=2*10**5, vmax=5*10**5)
                    cb_label = '$V_{L}$ ($\mathrm{10^5~m^{3}}$)'
                    cb_pos = [-30, 1.15]
                    folder = "Volume"
                    cbar_ax = fig.add_axes([0.86, 0.25, 0.035, 0.5])

                ax.plot(x, y, 'k', linewidth=1.5)
                ax.set_xlim(extent_hydro[0:2] if variable_tag in ["R", "W", "SM"] else extent_land[0:2])
                ax.set_ylim(extent_hydro[2:4] if variable_tag in ["R", "W", "SM"] else extent_land[2:4])
                plt.suptitle(Time_moment, fontsize=16)
                ax.axis('off')

                cbar_ax.tick_params(labelsize=15)
                cb = plt.colorbar(im, cax=cbar_ax)
                cb.set_label(cb_label, fontdict=font1, rotation=0, labelpad=cb_pos[0], y=cb_pos[1])
                if variable_tag == "W":
                    cb.set_ticks([0, 25, 50, 75, 100, 125, 150])
                elif variable_tag == "PF":
                    cb.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1])
                elif variable_tag == "FVolume":
                    cb.set_ticks([2*10**5, 2.5*10**5, 3*10**5, 3.5*10**5, 4*10**5, 4.5*10**5, 5*10**5])
                    cb.set_ticklabels(["2", "2.5", "3", "3.5", "4", "4.5", "5"])
                elif variable_tag == "FS3D":
                    cb = plt.colorbar(im, cax=cbar_ax, extend="max")

                save_path = os.path.join(base_path, folder, OutFigure_name)
                plt.savefig(save_path, dpi=300)
                plt.close()
                print(f"Saved plot: {save_path}")
            else:
                print(f"Skipping dataset {dset}: variable_tag {variable_tag} not in {variable_list}")
                continue  # Skip non-matching datasets
        except Exception as e:
            print(f"Error processing dataset {dset}: {e}")
            continue
data.close()

# Video creation
print("Start making videos")
for folder in ["R", "W", "SM", "FS", "PF", "Volume"]:
    folder_path = os.path.join(base_path, folder)
    file_list = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    if file_list:
        file_list.sort(key=lambda x: int("".join([i for i in x if i.isdigit()])))
        img_array = []
        for filename in file_list:
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)
            if img is not None:
                img_array.append(img)
            else:
                print(f"Failed to read image: {img_path}")
        if img_array:
            height, width, layers = img_array[0].shape
            out_path = os.path.join(base_path, f"{folder}.avi")
            out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'DIVX'), 5, (width, height))
            for img in img_array:
                out.write(img)
            out.release()
            print(f"Created video: {out_path}")
    else:
        print(f"No images found in {folder_path}")