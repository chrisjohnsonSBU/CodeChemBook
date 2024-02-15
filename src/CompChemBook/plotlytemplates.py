# -*- coding: utf-8 -*-
import plotly.graph_objects as go

# if you dont' specify anything you basically get simple_white
def chemPlot(name, ratio = None, font = None, colors = None, legend = "top-right"): # default ratio is US paper
    '''
    name: string that specifies the template in chemTemplates
    aratio: foat that specifies the desired aspect ratio of width/height
    cProg: list of color values that specify the colors that are cycled through
    dpi: the desired pixels per inch, and this is used to determine text size, linewidth, marker size, etc. 
    '''
    
    if "JACS" in name: # from appendix 2 of https://publish.acs.org/publish/author_guidelines?coden=jacsat#preparing_graphics
        dpi = 300
        aratio = 8.5/11
        font_size = 6
        page_width = 3.3 # in inches
        font_family = "helvetica"
        if "2" in name:
            page_width = 7.0
        
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
            
    #if "Coding" in name:
    
    # check to see if we need to use a user supplied ratio
    if ratio != None:
        aratio = ratio
        if "golden" in ratio:
            aratio = 1/1.61803
        if "letter" in ratio:
            aratio = 8.5/11
        if "A4" in ratio:
            aratio = 210/297
        if "square" in ratio:
            aratio = 1
        if "movie" in ratio:
            aratio = 1/2.4
        if "tv" in ratio:
            aratio = 1/1.77
        if "ppt" in ratio:
            aratio = 9/16
            if "narrow" in ratio:
                aratio = 3/4

    
    
    # select colors
    if colors == None:
        colorway = ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD", "#8C564B", "#E377C2", "#7F7F7F", "#BCBD22", "#17BECF"]
    if colors == "pastel":
        colorway = ["#9dc4ff", "#dbaefe", "#ff91cd", "#ff8978", "#ffa600"]
    if colors == "jewel":
        colorway = ["#9966CC", "#009473", "#0F52BA", "#830E0D", "#E4D00A" ]
    if colors == "neon":
        colorway = ["#5fe8ff", "#fc49ab", "#ff7300", "#64ff00", "#e7ff00"]
    if colors == "reds":
        colorway = ["#950000", "#af3d27", "#c6654c", "#db8b74", "#eeb19f", "#ffd7cb"]
    if colors == "blues":
        colorway = ["#004867", "#336583", "#5684a1", "#79a4bf", "#9dc5df", "#c1e7ff"]
    if colors == "purples":
        colorway = ["#7d2c95", "#9650a9", "#ae72bd", "#c694d2", "#ddb6e6", "#f5d9fb"]
    if colors == "complimentary":
        colorway = ["#0773b1", "#e79f27"]
    if colors == "triadic":
        colorway = ["#a23768", "#1d5700", "#e79f27"]
    if colors == "split complimentary":
        colorway = ["#0773b1", "#e79f27", "#d36027"]
    if colors == "analogous":
        colorway = ["#a23768", "#0773b1", "#9ba0d8"]
    if colors == "Lear":
        colorway = ["#0773b1", "#d36027", "#A23768", "#e79f27", "#9ba0d8", "#1d5700"]
    
    
    #let's handle the legend...
    sl = True
    lx = 1
    ly = 1
    xanchor = 'right'
    yanchor='top'
    
    if "bottom" in legend:
        ly = 0
        yanchor = "bottom"
    if "left" in legend:
        lx = 0
        xanchor = "left"
    if "none" in legend:
        sl = False
    if type(legend) == list and len(legend) == 2:
        try:
            lx = float(legend[0])
        except:
            raise ValueError("Error in using 'legend': float or int type expected")  
        try: 
            ly = float(legend[1])
        except:
            raise ValueError("Error in using 'legend': float or int type expected")
        
    chemTemplate = dict( 
            data = dict(
                scatter = [dict(line = dict(width = font_size*dpi/72*0.17), marker = dict(size = font_size*dpi/72*0.5))] # base size on font (since presumed to be legible)
                ),
            layout = dict(
                width = int(dpi*page_width), # for a single column, need 3.3in at 300 dpi
                height = int(dpi*page_width*aratio), #give a golden ratio-esq
                
                xaxis = dict(automargin = True, showgrid = False, ticks = "outside", showline = True, mirror = True, zeroline = False, title = {'standoff': 0.5*font_size*dpi/72}, ticklen = 0.33*font_size*dpi/72),
                yaxis = dict(automargin = True, showgrid = False, ticks = "outside", showline = True, mirror = True, zeroline = False, title = {'standoff': font_size*dpi/72}, ticklen = 0.33*font_size*dpi/72),
                
                font = dict(family = font_family, size = font_size*dpi/72), # equivalent to 6pt
                
                margin=dict(l=font_size*dpi/72, r=font_size*dpi/72, t=font_size*dpi/72, b=font_size*dpi/72), # set the margins to be equal to the font size
                
                colorway = colorway,
                
                legend=dict(x=lx, y=ly, xanchor = xanchor, yanchor = yanchor),
                showlegend = sl
                )
            )
 
    return go.layout.Template(chemTemplate)