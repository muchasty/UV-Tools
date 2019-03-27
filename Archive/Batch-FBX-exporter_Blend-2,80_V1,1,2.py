bl_info = {
    "name": "Batch FBX exporter",
    "description": "Tools to batch export fbx files",
    "author": "Tomasz Muszynski based on work of Patrick Jezek",
    "blender": (2, 80, 0),
    "version": (1, 1, 2),
    "support": "COMMUNITY",
    "category": "Import-Export",
    "location": "View3D > Properties Region (N-Panel) > Export",
    "tracker_url": "https://github.com/muchasty/UV-Tools", 
}

import bpy
import os
from bpy.props import *
from mathutils import *
from math import *


class BatchExportPanel(bpy.types.Panel):

    bl_idname = "BatchFBXexporter"
    bl_label = "Batch FBX exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Export"
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout

        # batch export
        col = layout.column(align=True)
        col.label(text="Batch FBX exporter:")
        col.prop(context.scene, 'pea_batch_export_path')
        row = col.row(align=True)
        row.operator("pea.batch_export", text=" Batch Export WORLD origin", icon='WORLD').selforigin=False
        row = layout.row()
        #row.prop(context.scene, "obj_individual_origin")
        row = layout.row()
        row.operator("pea.batch_export", text=" Batch Export SELF origin", icon='OBJECT_DATA').selforigin=True
 
class PeaBatchExport(bpy.types.Operator):
    bl_idname = "pea.batch_export"
    bl_label = "Choose Directory"
    obj_origin_point = (0.0, 0.0, 0.0)
    
    selforigin : BoolProperty() 
    
    def execute(self, context):
        print ("execute Pea_batch_export")
        print("selforigin=",self.selforigin)

        
        basedir = os.path.dirname(bpy.data.filepath)
        if not basedir:
            raise Exception("Blend file is not saved")

        if context.scene.pea_batch_export_path == "":
            raise Exception("Export path not set")

        # get selected objects
        mesh=[]
        col = bpy.context.selected_objects

        # convert path to windows friendly notation
        dir = os.path.dirname(bpy.path.abspath(context.scene.pea_batch_export_path))

        #OBJ_origin=bpy.context.scene.obj_individual_origin 
        OBJ_origin=self.selforigin
        CUR_loc=Vector(bpy.context.scene.cursor.location)
        for obj in col:
            # cursor to origin
            bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
            
            # INDIVIDUAL ORIGIN issue:
            # Use individual origin ?
            current_location = Vector(obj.location)
            obj_origin_point =  current_location
            if OBJ_origin==True :
                print("ATTENTION: Using individual objects origins ! : ",obj_origin_point)
                obj.location=bpy.context.scene.cursor.location
            
            # select only current object
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            # freeze location, rotation and scale
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

            bpy.ops.object.mode_set(mode='OBJECT')
            # store mesh            
            mesh.append(obj)
            # use mesh name for file name
            name = bpy.path.clean_name(obj.name)
            fn = os.path.join(dir, name)
            print("exporting: " + fn)
            # export fbx
            bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, axis_forward='-Z', axis_up='Y',mesh_smooth_type='FACE')
            
            # INDIVIDUAL ORIGIN issue:
            # placing object to the its original location
            if OBJ_origin==True :
                obj.location = Vector(obj_origin_point )
                print("INDIVIDUAL ORIGIN: placing object in the original location : ",obj_origin_point)
                
              
            bpy.context.scene.cursor.location = Vector(CUR_loc)
            
        print("--[ FINISHED ]-----------------------------------------------")      
        return {'FINISHED'}
    

        



# registers
def register():
    bpy.types.Scene.pea_batch_export_path = bpy.props.StringProperty (
        name="Export Path",
        default="",
        description="Define the path where to export",
        subtype='DIR_PATH'
    )
    bpy.types.Scene.obj_individual_origin = bpy.props.BoolProperty(
        name="Use individual origins",
        description="Using individual origin as pivot point",
        default = False)


    bpy.utils.register_class(BatchExportPanel)
    bpy.utils.register_class(PeaBatchExport)



def unregister():
    del bpy.types.Scene.pea_batch_export_path
    del bpy.types.Scene.obj_individual_origin
    bpy.utils.unregister_class(BatchExportPanel)
    bpy.utils.unregister_class(PeaBatchExport)


if __name__ == "__main__":
    register()