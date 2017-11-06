bl_info = {
    "name": "Lightmap Auto UV",
    "description": "Script makes automatic UV unwrap for lightmpas and help avoid a pixel sharing issue by islands.",
    "author": "Tomasz Muszynski",
    "version": (1, 11),
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "UV"
    }

import bpy
from bpy.props import *

class LightmapAutoUV(bpy.types.Operator):
    """Lightmap Auto UV"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "object.auto_lightmap"        # unique identifier for buttons and menu items to reference.
    bl_label = "Lightmap Auto UV"    # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    
    
    lightmap_Resolution=IntProperty(name="Lightmap Resolution [px]", min=4, max=65536)
    lightmap_KeepEditMode=BoolProperty(name="Keep Edit Mode")
    lightmap_Overwrite=BoolProperty(name="Auto-LM Overwrite")
    
    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')         
        try:    
            if self.lightmap_Overwrite==True :           
                bpy.context.active_object.data.uv_textures.remove(bpy.context.active_object.data.uv_textures["SmartUV Lightmap"])
        except:
            pass
        
        bpy.context.active_object.data.uv_textures.new(name="SmartUV Lightmap")
        bpy.context.active_object.data.uv_textures["SmartUV Lightmap"].active=True

        computedMargin=2*(1/self.lightmap_Resolution)
        print(self.lightmap_Resolution ," = ",computedMargin)
        bpy.ops.uv.smart_project(angle_limit=66,island_margin=computedMargin, user_area_weight=1.0, use_aspect=True, stretch_to_bounds=False)
        
        bpy.context.scene["lightmap_Resolution"]=self.lightmap_Resolution
        bpy.context.scene["lightmap_KeepEditMode"]=self.lightmap_KeepEditMode
        bpy.context.scene["lightmap_Overwrite"]=self.lightmap_Overwrite 
    
        if self.lightmap_KeepEditMode==False :    
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.active_object.data.uv_textures[0].active=True
        
    
        return {'FINISHED'}
    
    def invoke(self, context, event):                            
        try:        
            self.lightmap_Resolution=bpy.context.scene["lightmap_Resolution"]
            self.lightmap_KeepEditMode=bpy.context.scene["lightmap_KeepEditMode"]
            self.lightmap_Overwrite=bpy.context.scene["lightmap_Overwrite"]
        except:
            bpy.context.scene["lightmap_Resolution"]=256    
            bpy.context.scene["lightmap_KeepEditMode"]=False
            bpy.context.scene["lightmap_Overwrite"]=False
        
        
        self.lightmap_Resolution=bpy.context.scene["lightmap_Resolution"]
        self.lightmap_KeepEditMode=bpy.context.scene["lightmap_KeepEditMode"]
        self.lightmap_Overwrite=bpy.context.scene["lightmap_Overwrite"]
        return context.window_manager.invoke_props_dialog(self)
    
    
    

class LightmapAutoUVPanel(bpy.types.Panel):
    bl_label = "Dialog"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    global lightmap_Resolution
    def draw(self, context):
        self.layout.operator("object.auto_lightmap")

        

def register():
    bpy.utils.register_class(LightmapAutoUV)
    bpy.utils.register_class(LightmapAutoUVPanel)    


def unregister():
    bpy.utils.unregister_class(LightmapAutoUV)
    bpy.utils.unregister_class(LightmapAutoUVPanel)

    
if __name__ == "__main__":
    register()

#--------------------------------- RUN ---------------------
#bpy.ops.object.auto_lightmap('INVOKE_DEFAULT')





