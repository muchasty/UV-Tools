bl_info = {
    "name": "Lightmap Auto UV",
    "description": "Script makes automatic UV unwrap for lightmaps and helps to avoid a pixel sharing issue by islands.",
    "author": "Tomasz Muszynski",
    "blender":(2,80,0),
    "version": (1, 2, 6),
    "support": "COMMUNITY",
    "category": "UV",
    "location": "View3D > Properties Region (N-Panel) > UV / View3D > menu UV / ImageEditor > menu UV",
    "tracker_url": "https://github.com/muchasty/UV-Tools",
    }

    
import bpy
from bpy.props import *

class LightmapAutoUV(bpy.types.Operator):
    """Lightmap Auto UV"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "object.auto_lightmap"        # unique identifier for buttons and menu items to reference.
    bl_label = "Lightmap Auto UV"    # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH')    
    
    
    lightmap_Resolution : IntProperty(name="Lightmap Resolution [px]", min=4, max=65536)
    lightmap_KeepEditMode : BoolProperty(name="Keep Edit Mode")
    lightmap_Overwrite : BoolProperty(name="Auto-LM Overwrite")
    lightmap_Aspect : BoolProperty(name="Keep aspect ratio")
    lightmap_Bounds : BoolProperty(name="Stretch (no-aspect)")
    lightmap_Angle : FloatProperty(name="Angle limit", min=1, max=89)

    
    def execute(self, context):
        bpy.context.active_object.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')         
        try:    
            if self.lightmap_Overwrite==True :           
                bpy.context.active_object.data.uv_layers.remove(bpy.context.active_object.data.uv_layers["SmartUV Lightmap"])
        except:
            pass
        
        
        bpy.context.active_object.data.uv_layers.new(name="SmartUV Lightmap")
        bpy.context.active_object.data.uv_layers["SmartUV Lightmap"].active=True

        computedMargin=4*(1/self.lightmap_Resolution)
        print(self.lightmap_Resolution ," = ",computedMargin)
        bpy.ops.uv.smart_project(angle_limit=self.lightmap_Angle,island_margin=computedMargin, user_area_weight=0, use_aspect=self.lightmap_Aspect, stretch_to_bounds=self.lightmap_Bounds)
        
        bpy.context.scene["lightmap_Resolution"]=self.lightmap_Resolution
        bpy.context.scene["lightmap_KeepEditMode"]=self.lightmap_KeepEditMode
        bpy.context.scene["lightmap_Overwrite"]=self.lightmap_Overwrite
        bpy.context.scene["lightmap_Aspect"]=self.lightmap_Aspect 
        bpy.context.scene["lightmap_Bounds"]=self.lightmap_Bounds
        bpy.context.scene["lightmap_Angle"]=self.lightmap_Angle
    
        if self.lightmap_KeepEditMode==False :    
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.active_object.data.uv_layers[0].active=True
        
    
        return {'FINISHED'}
    
    def invoke(self, context, event):                            
        try:        
            self.lightmap_Resolution=bpy.context.scene["lightmap_Resolution"]
            self.lightmap_KeepEditMode=bpy.context.scene["lightmap_KeepEditMode"]
            self.lightmap_Overwrite=bpy.context.scene["lightmap_Overwrite"]
            self.lightmap_Aspect=bpy.context.scene["lightmap_Aspect"]
            self.lightmap_Bounds=bpy.context.scene["lightmap_Bounds"]
            self.lightmap_Angle=bpy.context.scene["lightmap_Angle"]
        except:
            bpy.context.scene["lightmap_Resolution"]=256    
            bpy.context.scene["lightmap_KeepEditMode"]=False
            bpy.context.scene["lightmap_Overwrite"]=True
            bpy.context.scene["lightmap_Aspect"]=True 
            bpy.context.scene["lightmap_Bounds"]=True
            bpy.context.scene["lightmap_Angle"]=89
        
        
        self.lightmap_Resolution=bpy.context.scene["lightmap_Resolution"]
        self.lightmap_KeepEditMode=bpy.context.scene["lightmap_KeepEditMode"]
        self.lightmap_Overwrite=bpy.context.scene["lightmap_Overwrite"]
        self.lightmap_Aspect=bpy.context.scene["lightmap_Aspect"]
        self.lightmap_Bounds=bpy.context.scene["lightmap_Bounds"]
        self.lightmap_Angle=bpy.context.scene["lightmap_Angle"]
        
        return context.window_manager.invoke_props_dialog(self)
    



    
    

class LightmapAutoUVPanel(bpy.types.Panel):
    bl_label = "Lightmap Auto UV"
    bl_idname = "LIGHTMAPAUTOUV_PT_LightmapAutoUVPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UV"
    global lightmap_Resolution  
    def draw(self, context):
        self.layout.operator("object.auto_lightmap")


        
def menu_LightmapAutoUV(self, context):
    self.layout.operator(LightmapAutoUV.bl_idname)


# ******[ Registering ]******************************************
# ***************************************************************


# = REGISTER ====================================================
def register():
    # classes
    bpy.utils.register_class(LightmapAutoUV)
    bpy.utils.register_class(LightmapAutoUVPanel)   
    # menus    
    bpy.types.VIEW3D_MT_uv_map.append(menu_LightmapAutoUV)
    bpy.types.IMAGE_MT_uvs.append(menu_LightmapAutoUV)


# = unREGISTER ==================================================
def unregister():

    # classes    
    bpy.utils.unregister_class(LightmapAutoUV)
    bpy.utils.unregister_class(LightmapAutoUVPanel)
    # menus
    bpy.types.VIEW3D_MT_uv_map.remove(menu_LightmapAutoUV)
    bpy.types.IMAGE_MT_uvs.remove(menu_LightmapAutoUV)




# ---- Proceed Registering ---------------------------------------    
if __name__ == "__main__":
    register()

#--------------------------------- RUN ---------------------
#bpy.ops.object.auto_lightmap('INVOKE_DEFAULT')





