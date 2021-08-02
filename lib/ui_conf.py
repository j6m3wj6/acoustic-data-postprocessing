ICON_DIR = "./icons/"


LINEWIDTHS = [1, 1.5, 2.5, 4]
LINESTYLES = ['-', '--']
LINEWIDTH_DEFAULT = LINEWIDTHS[1]
LINEWIDTH_HIGHLIGHT = LINEWIDTHS[3]

LEGEND_WRAP = 25

COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c',
          '#d62728', '#9467bd', '#8c564b', '#e377c2',
          '#7f7f7f', '#bcbd22', '#17becf']


FIGURE_CONF = {
    "General": {
        "Title": "",
        "Margin": {
            "left-right": 10,
            "top-bottom": 10,
        },
        "Legend": {
            "visible": True,
            "text-wrap": LEGEND_WRAP
        }
    },
    "Axis": {
        "X-Axis": {
            "auto-scale": False,
            "min": 20,
            "max": 20000,
            "label": "Frequency",
            "unit": "Hz",
            "scale": "log"
        },
        "Y-Axis": {
            "auto-scale": True,
            "min": 0,
            "max": 100,
            "label": "",
            "unit": "dBSPL",
            "scale": "linear"
        },
        "Sub_Y-Axis": {
            "auto-scale": True,
            "min": 0,
            "max": 100,
            "label": "",
            "unit": "dBSPL",
            "scale": "linear"
        }
    }
}


UI_CONF = {
    "MyCanvas": {
        "status": {
            "Main": [0],
            "UpAndDown": [0, 1],
            "Quater": [0, 1, 2, 3],
            "MainwithThreeSmall": [0, 1, 2, 3]
        },
        "mode": "Main",
        "canvasPool": {
            "0": {
                "id": 0,
                "types": ["Sound Pressure Level", "THD Ratio"],
                "parameter": FIGURE_CONF
            },
            "1": {
                "id": 1,
                "types": ["Impedance", "Phase"],
                "parameter": FIGURE_CONF
            },
            "2": {
                "id": 2,
                "types": ["THD Level", "Level and Distortion"],
                "parameter": FIGURE_CONF
            },
            "3": {
                "id": 3,
                "types": ["Distortion Product Level", "Distortion Product Ratio"],
                "parameter": FIGURE_CONF
            },
            "4": {
                "id": 4,
                "types": ["Rub & Buzz Peak Ratio", "None"],
                "parameter": FIGURE_CONF
            }

        }
    }
}
