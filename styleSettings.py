# -*- coding: utf-8 -*-
'''
Created on 17 Mar 2013

@author: 
'''

from wrappers import style

                   
class DefaultSettings:
    inner_radius = 30
    outer_radius = 32
    
    shadow_offset = 7
    shadow_blur = 15
    
    border_thickness = 2
    border_color= "#000000"
    
    bevel_size = 6
    highlight_amount = 0.1
    lowlight_amount = 0.3
    
    color="#3030c0"
    

class EngraveSettingsOuter:
    inner_radius = 14
    outer_radius = 16
    
    shadow_offset = 0
    shadow_blur = 15
    
    border_thickness = 1
    border_color= "#000000"
    
    bevel_size = 4
    highlight_amount = -0.3
    lowlight_amount = -0.3
    
    color="#6f6f6f"

class EngraveSettingsInner:
    inner_radius = 1
    outer_radius = 2
    
    shadow_offset = 0
    shadow_blur = 15
    
    border_thickness = 0
    border_color= "#000000"
    
    bevel_size = 2
    highlight_amount = -0.1
    lowlight_amount = -0.1
    
    color="#4f4f4f"

class KnobSettings:
    inner_radius = 10
    outer_radius = 12
    
    #inner_radius = 15
    #outer_radius = 18
    
    shadow_offset = 5
    shadow_blur = 4
    
    border_thickness = 1
    border_color= "#000000"
    
    bevel_size = 2
    highlight_amount = 0.1
    lowlight_amount = 0.3
    
    color="#c0c0c0"

class BarSettings:
    
    inner_radius = 0
    outer_radius = 0
    
    shadow_offset = 0
    shadow_blur = 0
    
    border_thickness = 0
    border_color= "#000000"
    
    bevel_size = 0
    highlight_amount = 0.1
    lowlight_amount = 0.3
    
#    color="#c0c0c0"
    color=style.page.background_color
    
class HighlightBarSettings(BarSettings):
    pass
    

class BarSettingsOLD:
    inner_radius = 12
    outer_radius = 14
    
    shadow_offset = 4
    shadow_blur = 4
    
    border_thickness = 1
    border_color= "#000000"
    
    bevel_size = 4
    highlight_amount = 0.1
    lowlight_amount = 0.3
    
    color="#c0c0c0"
    
class HighlightBarSettingsOLD(BarSettings):
    inner_radius = 12
    outer_radius = 14
    
    shadow_offset = 2
    shadow_blur = 2
    
    border_thickness = 1
    border_color= "#c0c0c0"
    
    bevel_size = 4
    highlight_amount = 0.2
    lowlight_amount = 0.3
    
    color="#c0c0f0"
    

class LEDSettings:
    inner_radius = 10
    outer_radius = 12
    
    shadow_offset = 6
    shadow_blur = 8
    
    border_thickness = 1
    border_color= "#000000"
    
    bevel_size = 3
    highlight_amount = 0.5
    lowlight_amount = 0.3
    
    color="#10a010"