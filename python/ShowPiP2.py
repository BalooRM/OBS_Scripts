# based upon upgradeQ's example toggle_sceneitem_vis.py
# https://github.com/upgradeQ/OBS-Studio-Python-Scripting-Cheatsheet-obspython-Examples-of-API
# This script seeks to display or clear a picture-in-picture source in a scene. Elements, notably
# dimensions, are hard-coded as I discover the methods to determine them from the objects. 
import obspython as S
import time

# set scene dimensions
scenedim = S.vec2()
scenedim.x = 1920
scenedim.y = 1080

# set PiP inset dimensions - these can be read from the visible source
insetdim = S.vec2()
insetdim.x = 640
insetdim.y = 480

class PiP:
    def __init__(self, source_name=None):
        self.source_name = source_name

    def toggle(self):
        current_scene = S.obs_scene_from_source(S.obs_frontend_get_current_scene())
        scene_item = S.obs_scene_find_source(current_scene, self.source_name)
        boolean = not S.obs_sceneitem_visible(scene_item)
        S.obs_sceneitem_set_visible(scene_item, boolean)
        S.obs_scene_release(current_scene)

    def activate(self, pstr):
        # fill initial values of position dictionary
        pos = {}
        for p in ['UL', 'UR', 'LL', 'LR']:
            pos[p] = S.vec2()
            pos[p].x = 0
            pos[p].y = 0
        # activate the scene item
        current_scene = S.obs_scene_from_source(S.obs_frontend_get_current_scene())
        scene_item = S.obs_scene_find_source(current_scene, self.source_name)
        # source must be visible to get width and height
        S.obs_sceneitem_set_visible(scene_item, True) 
        time.sleep(0.05)
        scale = S.vec2()
        S.obs_sceneitem_get_scale(scene_item, scale)
        source = S.obs_get_source_by_name(self.source_name)
        srcwidth = S.obs_source_get_width(source)
        srcheight = S.obs_source_get_height(source)
        pos['UR'].x = scenedim.x - (srcwidth * scale.x)
        pos['LL'].y = scenedim.y - (srcheight * scale.y)
        pos['LR'].x = scenedim.x - (srcwidth * scale.x)
        pos['LR'].y = scenedim.y - (srcheight * scale.y)
        
        print(' '.join(['Source dimensions:', str(srcwidth), 'x', str(srcheight)]))
        print(' '.join(['Position:', str(pos[pstr].x), ',', str(pos[pstr].y)]))
        print(' '.join(['Scale:', str(scale.x), 'x', str(scale.y)]))
        # set the position
        S.obs_sceneitem_set_pos(scene_item, pos[pstr])
        S.obs_scene_release(current_scene)

    def clear(self):
        # clear the scene item
        current_scene = S.obs_scene_from_source(S.obs_frontend_get_current_scene())
        scene_item = S.obs_scene_find_source(current_scene, self.source_name)
        S.obs_sceneitem_set_visible(scene_item, False)
        S.obs_scene_release(current_scene)


pip = PiP()  # class created ,obs part starts


def activate_pressedUL(props, prop):
    pip.activate('UL')
    

def activate_pressedUR(props, prop):
    pip.activate('UR')
    

def activate_pressedLL(props, prop):
    pip.activate('LL')
    

def activate_pressedLR(props, prop):
    pip.activate('LR')

    
def pip_clear(props, prop):
    pip.clear()


def script_update(settings):
    pip.source_name = S.obs_data_get_string(settings, "source")


def script_properties():  # ui
    props = S.obs_properties_create()
    p = S.obs_properties_add_list(
        props,
        "source",
        "Text Source",
        S.OBS_COMBO_TYPE_EDITABLE,
        S.OBS_COMBO_FORMAT_STRING,
    )
    sources = S.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = S.obs_source_get_unversioned_id(source)
            name = S.obs_source_get_name(source)
            S.obs_property_list_add_string(p, name, name)

        S.source_list_release(sources)
    S.obs_properties_add_button(props, "button1", "Upper Left", activate_pressedUL)
    S.obs_properties_add_button(props, "button2", "Upper Right", activate_pressedUR)
    S.obs_properties_add_button(props, "button3", "Lower Left", activate_pressedLL)
    S.obs_properties_add_button(props, "button4", "Lower Right", activate_pressedLR)
    S.obs_properties_add_button(props, "button5", "Clear PiP", pip_clear)
    return props
