"""
Plot map.
"""

import pathlib

from pathlib import PurePath
from typing import Optional, Sequence, Union

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

from xarray import DataArray, Dataset

from ..utils import find_bbox, shift_longitudes

try:
    import cartopy

    CARTOPY_AVAILABLE = True
except ImportError:  # pragma: no cover
    CARTOPY_AVAILABLE = False  # pragma: no cover


def plot_map(
    maps: np.array,
    figname: Union[str, PurePath],
    ds: Union[DataArray, Dataset],
    alpha: int = 5,
    dd: int = 2,
    extent: Optional[Sequence] = None,
):
    """Plot and save to file map of model domain and data locations.

    Parameters
    ----------
    maps : array
        Info about datasets. [min_lon, max_lon, min_lat, max_lat, source_name]
    figname : Union[str, PurePath]
        Map will be saved here.
    ds : Union[DataArray, Dataset]
        Model output.
    extent: 
        [min longitude, max longitude, min latitude, max latitude]
    """
    
    ds = shift_longitudes(ds)
    
    if not CARTOPY_AVAILABLE:
        raise ModuleNotFoundError(  # pragma: no cover
            "Cartopy is not available so map will not be plotted."
        )
        
    import cartopy

    pc = cartopy.crs.PlateCarree()
    col_label = "k"  # "r"
    land_10m = cartopy.feature.NaturalEarthFeature(
        "physical", "land", "10m", edgecolor="face", facecolor="0.8"
    )
    res = "10m"

    min_lons, max_lons = maps[:, 0].astype(float), maps[:, 1].astype(float)
    min_lats, max_lats = maps[:, 2].astype(float), maps[:, 3].astype(float)

    central_longitude = min_lons.mean()
    proj = cartopy.crs.Mercator(central_longitude=float(central_longitude))
    fig = plt.figure(figsize=(8, 7), dpi=100)
    ax = fig.add_axes([0.06, 0.01, 0.93, 0.95], projection=proj)
    # ax.set_frame_on(False) # kind of like it without the box
    # ax.set_extent([-98, -87.5, 22.8, 30.5], cartopy.crs.PlateCarree())
    gl = ax.gridlines(
        linewidth=0.2, color="gray", alpha=0.5, linestyle="-", draw_labels=True
    )
    gl.bottom_labels = False  # turn off labels where you don't want them
    gl.right_labels = False
    ax.coastlines(resolution=res)
    ax.add_feature(land_10m, facecolor="0.8")

    # alphashape
    _, _, bbox, p = find_bbox(ds, dd=dd, alpha=alpha)
    ax.add_geometries([p], crs=pc, facecolor="none", edgecolor="r", linestyle="-")

    # plot stations
    # if min_lons == max_lons:  #  check these are stations
    ax.plot(
        min_lons,
        min_lats,
        marker="o",
        markersize=1,
        transform=pc,
        ls="",
        color=col_label,
    )

    # annotate stations
    for i, (lon, lat) in enumerate(zip(min_lons, min_lats)):
        xyproj = ax.projection.transform_point(lon, lat, pc)
        ax.annotate(i, xy=xyproj, xytext=xyproj, color=col_label)

    # [min lon, max lon, min lat, max lat]
    if extent is None:
        extent_use = [bbox[0] - 0.1, bbox[2] + 0.1, bbox[1] - 0.1, bbox[3] + 0.1]
    
    # if model is global - based on extent - write that it is global and use smaller extent
    if np.allclose(bbox[0], -180, atol=2) and np.allclose(bbox[2], 180, atol=2) and np.allclose(bbox[1], -90, atol=2) and np.allclose(bbox[3], 90, atol=2):
        # explain global model
        ax.set_title("Only showing part of global model")
        
        # change delta deg for extent to max(10% of total diff lons/lats, 1 deg)
        if extent is None:
            dlon, dlat = 0.1*(min(min_lons) - max(max_lons)), 0.1*(min(min_lats) - max(max_lats))
            ddlon, ddlat = max(dlon, 5), max(dlat, 2)
            extent_use = [min(min_lons) - ddlon, max(max_lons) + ddlon,
                          min(min_lats) - ddlat, max(max_lats) + ddlat]
        
        
    ax.set_extent(extent_use, pc)

    fig.savefig(figname, dpi=100, bbox_inches="tight")
