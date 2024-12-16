import plotly.graph_objects as go
import plotly.io as pio
from dataclasses import dataclass, field
import copy

# Dictionary of colorways
chem_colorways = dict(
    default = ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD", "#8C564B", "#E377C2", "#7F7F7F", "#BCBD22", "#17BECF"],
    pastels = ["#9dc4ff", "#dbaefe", "#ff91cd", "#ff8978", "#ffa600"],
    jewel = ["#9966CC", "#009473", "#0F52BA", "#830E0D", "#E4D00A" ],
    neon = ["#5fe8ff", "#fc49ab", "#ff7300", "#64ff00", "#e7ff00"],
    reds = ["#950000", "#af3d27", "#c6654c", "#db8b74", "#eeb19f", "#ffd7cb"],
    blues = ["#004867", "#336583", "#5684a1", "#79a4bf", "#9dc5df", "#c1e7ff"],
    purples = ["#7d2c95", "#9650a9", "#ae72bd", "#c694d2", "#ddb6e6", "#f5d9fb"],
    complimentary = ["#0773b1", "#e79f27"],
    triadic = ["#a23768", "#1d5700", "#e79f27"],
    split_complimentary = ["#0773b1", "#e79f27", "#d36027"],
    analogous = ["#a23768", "#0773b1", "#9ba0d8"],
    Lear = ["#0773b1", "#d36027", "#A23768", "#e79f27", "#9ba0d8", "#1d5700"],
    greys = ['#00000', '#333333', '#666666', '#999999']
    )


'''
TEMPLATE DICTIONARIES
- these are each created in three parts...
    1. An aux dictionary entry, which is supporting info for calculating things. This is not directly put into the final template
    2. The data dictionary that will be added to the template
    3. The layout dictionary that will be added to the template. 
'''

JACS = {}

JACS["aux"] = dict( #specifications to allow calculations
        dpi = 600,
        canvas_width = 3.3, # convert cm to inches),
        aratio = 8.5/11,
        font_size = 7,
        )

JACS["data"] = dict(
        scatter = [
            dict(
                line = dict(width = JACS["aux"]["font_size"] * JACS["aux"]["dpi"]/72*0.17), 
                marker = dict(size = JACS["aux"]["font_size"] * JACS["aux"]["dpi"]/72*0.5)
                )
            ]
        )

JACS["layout"] = dict(
        meta = JACS["aux"], # can store meta data here, has to be in layout
        width = int(JACS["aux"]["dpi"] * JACS["aux"]["canvas_width"]),
        height = int(JACS["aux"]["dpi"] * JACS["aux"]["canvas_width"]* JACS["aux"]["aratio"]), #give a golden ratio-esq
        
        xaxis = dict(automargin = True, showgrid = False, ticks = "outside", showline = True, mirror = True, zeroline = False, title = {'standoff': 0.5*JACS["aux"]["font_size"]*JACS["aux"]["dpi"]/72}, ticklen = 0.33*JACS["aux"]["font_size"]*JACS["aux"]["dpi"]/72),
        yaxis = dict(automargin = True, showgrid = False, ticks = "outside", showline = True, mirror = True, zeroline = False, title = {'standoff': JACS["aux"]["font_size"]*JACS["aux"]["dpi"]/72}, ticklen = 0.33*JACS["aux"]["font_size"]*JACS["aux"]["dpi"]/72),
        
        margin=dict(l=JACS["aux"]["font_size"] * JACS["aux"]["dpi"]/72, r=JACS["aux"]["font_size"] * JACS["aux"]["dpi"]/72, t=JACS["aux"]["font_size"] * JACS["aux"]["dpi"]/72, b=JACS["aux"]["font_size"] * JACS["aux"]["dpi"]/72), # set the margins to be equal to the font size

        colorway = chem_colorways["default"],

        legend=dict(x=1, y=1, xanchor = "right", yanchor = "top"),
        showlegend = True,

        font = dict(
            size = int(JACS["aux"]["font_size"] * JACS["aux"]["dpi"]/72),
            family = "helvetica",
            ),
        )



ccb_color = {}
ccb_color["aux"] = dict( #specifications to allow calculations
        dpi = 600,
        canvas_width = 5, # in inches),
        aratio = 148 / 210, # the ratio of A4 paper,
        font_size = 8,
        )

ccb_color["data"] = dict(
        scatter = [
            dict(
                line = dict(width = ccb_color["aux"]["font_size"] * ccb_color["aux"]["dpi"]/72*0.17), 
                marker = dict(size = ccb_color["aux"]["font_size"] * ccb_color["aux"]["dpi"]/72*0.5)
                )
            ]
        )

ccb_color["layout"] = dict(
        meta = ccb_color["aux"], # can store meta data here, has to be in layout
        width = int(ccb_color["aux"]["dpi"] * ccb_color["aux"]["canvas_width"]),
        height = int(ccb_color["aux"]["dpi"] * ccb_color["aux"]["canvas_width"]* JACS["aux"]["aratio"]), #give a golden ratio-esq
        
        xaxis = dict(automargin = True, showgrid = False, ticks = "outside", showline = True, mirror = True, zeroline = False, title = {'standoff': 0.5*ccb_color["aux"]["font_size"]*ccb_color["aux"]["dpi"]/72}, ticklen = 0.33*ccb_color["aux"]["font_size"]*ccb_color["aux"]["dpi"]/72),
        yaxis = dict(automargin = True, showgrid = False, ticks = "outside", showline = True, mirror = True, zeroline = False, title = {'standoff': ccb_color["aux"]["font_size"]*ccb_color["aux"]["dpi"]/72}, ticklen = 0.33*ccb_color["aux"]["font_size"]*ccb_color["aux"]["dpi"]/72),
        
        margin=dict(l=ccb_color["aux"]["font_size"] * ccb_color["aux"]["dpi"]/72, r=ccb_color["aux"]["font_size"] * ccb_color["aux"]["dpi"]/72, t=ccb_color["aux"]["font_size"] * ccb_color["aux"]["dpi"]/72, b=ccb_color["aux"]["font_size"] * ccb_color["aux"]["dpi"]/72), # set the margins to be equal to the font size

        colorway = chem_colorways["Lear"],

        legend=dict(x=1, y=1, xanchor = "right", yanchor = "top"),
        showlegend = True,

        font = dict(
            size = int(ccb_color["aux"]["font_size"] * ccb_color["aux"]["dpi"]/72),
            family = "helvetica",
            ),
        )


'''
Now, update the chemplate_dicts to have all the chemplates we want
'''

chemplate_dicts = dict(
    JACS = JACS,
    ccb_color = ccb_color,
    simple_white = copy.deepcopy(pio.templates["simple_white"]),
    )

def new_chemplate(name = "simple_white", base_template = "simple_white"):
    '''
    Function that generates a new template, working from a base template. 
    '''
    new_template = copy.deepcopy(pio.templates[base_template]) # get the template for the base template
    
    
    if "data" not in new_template:
        new_template["data"] = {}
    if "layout" not in new_template:
        new_template["layout"] = {}

    if "data" not in chemplate_dicts[name]:
        chemplate_dicts[name]["data"] = {}
    if "layout" not in chemplate_dicts[name]:
        chemplate_dicts[name]["layout"] = {}
        
    new_template["data"].update(chemplate_dicts[name]["data"]) # update the data portion of the template with new values
    new_template["layout"].update(chemplate_dicts[name]["layout"]) # update the layout portion of the template with new values

    return go.layout.Template(new_template)

def length_to_pixels (value, dpi):
    if "in" in value:
        pixels = int(value.split("in")[0].strip())*dpi 
    if "cm" in value:
        pixels = int(value.split("cm")[0].strip())*dpi*0.3937007874 # convert cm to in
    
    return pixels

def apply_template(fig, chemplate, cols = 1, width = None, fontsize = None, height = None, dpi = None, fontfamily = None):    
    if dpi is None:
        dpi = chemplate["layout"]["meta"]["dpi"]
        
    if fontsize is not None:
        chemplate["layout"]["font"]["size"] = int(fontsize * dpi/72)
        
    if fontfamily is not None:
        chemplate["layout"]["font"]["family"] = fontfamily
        
    if cols == 2:
        chemplate["layout"]["width"] = 7*dpi 
        
    if width is not None:
        chemplate["layout"]["width"] = length_to_pixels(width, dpi)
            
    if height is not None:
        chemplate["layout"]["height"] = length_to_pixels(height, dpi)

    fig.update_layout(template = chemplate, dict1 = chemplate["layout"])
    
@dataclass
class chemplates:
    JACS : dict = field(default_factory = lambda: new_chemplate("JACS",))
    ccb_color : dict = field(default_factory = lambda: new_chemplate("ccb_color",))


# now initilize the templates class, so we can access the attributes
chemplate = chemplates()




















# restructure this as a data class
# be able to accept a dictionary key-like thing for this, for the ones that exist right now
# make classes for each publisher/family (acs, rsc, springer, elsevier, mdpi, etc AND by use case: slides, powerpoint, keynote, etc) and then have subclasses for specifics (JACS, ChemSci, dark, light, etc. )
'''
        
    if "ChemSci" in name: # from here: https://www.rsc.org/journals-books-databases/author-and-reviewer-hub/authors-information/prepare-and-format/figures-graphics-images/#figuresgraphics
        dpi = 600
        aratio = 210/297 # the ratio of A4 paper
        font_size = 7
        page_width = 8.3*0.3937007874 # convert cm to inches
        font_family = "helvetica"
        if "2" in name:
            page_width = 17.1*0.3937007874 # this is the 2-column figure
    
    if "Science" == name: # from https://www.science.org/content/page/instructions-preparing-initial-manuscript#preparation-of-figures
        dpi = 600
        aratio = 8.5/11
        font_size = 6
        page_width = 5.7*0.3937007874 # convert cm to inches
        font_family = "helvetica"
        if "2" in name:
            page_width = 18.3*0.3937007874 # this is the 2-column figure
        
    if "Nature" == name: # from https://www.nature.com/nature/for-authors/final-submission
        dpi = 600
        aratio = 210/297 # the ratio of A4 paper
        font_size = 6
        page_width = 8.9*0.3937007874 # convert cm to inches
        font_family = "helvetica"
        if "2" in name:
            page_width = 12.1*0.3937007874 # this is the 2-column figure
        if "3" in name:
            page_width = 18.4*0.3937007874 # this is the 3-column figure
            
    if "JCP" in name: # from https://publishing.aip.org/resources/researchers/author-instructions/#graphics
        dpi = 600
        aratio = 210/297 # the ratio of A4 paper
        font_size = 8
        page_width = 8.5*0.3937007874 # convert cm to inches
        font_family = "helvetica"
        if "2" in name:
            page_width = 17*0.3937007874 # this is the 2-column figure

    if "Lear" in name:
        dpi = 300
        aratio = 1/1.61803
        page_width = 2.5
        font_size = 6
        font_family = "helvetica"
        colorway = ["#0773b1", "#d36027", "#A23768", "#e79f27", "#9ba0d8", "#1d5700"]
        if "pres" in name:
            page_width = 12
            page_height = 6
            aratio = 0.5
            font_size = 16
            font_family = "avenir"
            if "2" in name: 
                page_width = 6.25
                aratio = 5.75/6.25
'''
