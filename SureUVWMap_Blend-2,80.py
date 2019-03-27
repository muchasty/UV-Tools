bl_info = {
    "name": "Sure UVW Map",
    "author": "TomaszMuszynski (UI adaptation), Alexander Milovsky (Functionality)",
    "version": (0, 6, 7),
    "blender": (2, 80, 0),
    "location": "View3D > Properties Region (N-Panel) > UV / View3D > menu UV / ImageEditor > menu UV",
    "description": "Box / Best Planar UVW Map (Make Material With Raster Texture First!)",
    "support": "COMMUNITY",
    "category": "UV",
    "location": "View3D > Properties Region (N-Panel) > UV",
    "tracker_url": "https://github.com/muchasty/UV-Tools",
    }

import bpy
from bpy.props import BoolProperty, FloatProperty, StringProperty, FloatVectorProperty
from math import sin, cos, pi
from mathutils import Vector



# globals for Box Mapping
all_scale_def = 1
tex_aspect = 1.0
x_offset_def = 0
y_offset_def = 0
z_offset_def = 0
x_rot_def = 0
y_rot_def = 0
z_rot_def = 0


# globals for Best Planar Mapping
xoffset_def = 0
yoffset_def = 0
zrot_def = 0

# Preview flag
preview_flag = True




#**************************************************************************************************************************
#**************************************************************************************************************************
#**************************************************************************************************************************
# BOX MAPPING
#**************************************************************************************************************************
def box_map():    
    #print('** Boxmap **')
    global all_scale_def,x_offset_def,y_offset_def,z_offset_def,x_rot_def,y_rot_def,z_rot_def, tex_aspect
    obj = bpy.context.active_object
    mesh = obj.data

    is_editmode = (obj.mode == 'EDIT')

    # if in EDIT Mode switch to OBJECT
    if is_editmode:
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    # if no UVtex - create it
    if not mesh.uv_layers:
        uvtex = bpy.ops.mesh.uv_texture_add()
    uvtex = mesh.uv_layers.active
    #uvtex.active_render = True
    
    img = None    
    aspect = 1.0
    mat = obj.active_material
    try:
        if mat:
            img = mat.active_texture
            aspect = img.image.size[0]/img.image.size[1]
    except:
        pass
    aspect = aspect * tex_aspect

                
    
    #
    # Main action
    #
    if all_scale_def:
        sc = 1.0/all_scale_def
    else:
        sc = 1.0   

    sx = 1 * sc
    sy = 1 * sc
    sz = 1 * sc
    ofx = x_offset_def
    ofy = y_offset_def
    ofz = z_offset_def
    rx = x_rot_def / 180 * pi
    ry = y_rot_def / 180 * pi
    rz = z_rot_def / 180 * pi
    
    crx = cos(rx)
    srx = sin(rx)
    cry = cos(ry)
    sry = sin(ry)
    crz = cos(rz)
    srz = sin(rz)
    ofycrx = ofy * crx
    ofzsrx = ofz * srx
    
    ofysrx = ofy * srx
    ofzcrx = ofz * crx
    
    ofxcry = ofx * cry
    ofzsry = ofz * sry
    
    ofxsry = ofx * sry
    ofzcry = ofz * cry
    
    ofxcry = ofx * cry
    ofzsry = ofz * sry
    
    ofxsry = ofx * sry
    ofzcry = ofz * cry
    
    ofxcrz = ofx * crz
    ofysrz = ofy * srz
    
    ofxsrz = ofx * srz
    ofycrz = ofy * crz
    
    #uvs = mesh.uv_loop_layers[mesh.uv_loop_layers.active_index].data
    uvs = mesh.uv_layers.active.data
    for i, pol in enumerate(mesh.polygons):
        if not is_editmode or mesh.polygons[i].select:
            for j, loop in enumerate(mesh.polygons[i].loop_indices):
                v_idx = mesh.loops[loop].vertex_index
                #print('before[%s]:' % v_idx)
                #print(uvs[loop].uv)
                n = mesh.polygons[i].normal
                co = mesh.vertices[v_idx].co
                x = co.x * sx
                y = co.y * sy
                z = co.z * sz
                if abs(n[0]) > abs(n[1]) and abs(n[0]) > abs(n[2]):
                    # X
                    if n[0] >= 0:
                        uvs[loop].uv[0] =  y * crx + z * srx                    - ofycrx - ofzsrx
                        uvs[loop].uv[1] = -y * aspect * srx + z * aspect * crx  + ofysrx - ofzcrx
                    else:
                        uvs[loop].uv[0] = -y * crx + z * srx                    + ofycrx - ofzsrx
                        uvs[loop].uv[1] =  y * aspect * srx + z * aspect * crx  - ofysrx - ofzcrx
                elif abs(n[1]) > abs(n[0]) and abs(n[1]) > abs(n[2]):
                    # Y
                    if n[1] >= 0:
                        uvs[loop].uv[0] =  -x * cry + z * sry                   + ofxcry - ofzsry
                        uvs[loop].uv[1] =   x * aspect * sry + z * aspect * cry - ofxsry - ofzcry
                    else:
                        uvs[loop].uv[0] =   x * cry + z * sry                   - ofxcry - ofzsry
                        uvs[loop].uv[1] =  -x * aspect * sry + z * aspect * cry + ofxsry - ofzcry
                else:
                    # Z
                    if n[2] >= 0:
                        uvs[loop].uv[0] =   x * crz + y * srz +                 - ofxcrz - ofysrz
                        uvs[loop].uv[1] =  -x * aspect * srz + y * aspect * crz + ofxsrz - ofycrz
                    else:
                        uvs[loop].uv[0] =  -y * srz - x * crz                   + ofxcrz - ofysrz
                        uvs[loop].uv[1] =   y * aspect * crz - x * aspect * srz - ofxsrz - ofycrz
    
    # Back to EDIT Mode
    if is_editmode:
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        




#**************************************************************************************************************************
#**************************************************************************************************************************        
#**************************************************************************************************************************
# Best Planar Mapping
#**************************************************************************************************************************
def best_planar_map():
    global all_scale_def,xoffset_def,yoffset_def,zrot_def, tex_aspect
    
    obj = bpy.context.active_object
    mesh = obj.data

    is_editmode = (obj.mode == 'EDIT')

    # if in EDIT Mode switch to OBJECT
    if is_editmode:
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    # if no UVtex - create it
    if not mesh.uv_layers:
        uvtex = bpy.ops.mesh.uv_texture_add()
    uvtex = mesh.uv_layers.active
    #uvtex.active_render = True
    
    img = None    
    aspect = 1.0
    mat = obj.active_material
    try:
        if mat:
            img = mat.active_texture
            aspect = img.image.size[0]/img.image.size[1]
    except:
        pass
    aspect = aspect * tex_aspect
                
    
    #
    # Main action
    #
    if all_scale_def:
        sc = 1.0/all_scale_def
    else:
        sc = 1.0   

    # Calculate Average Normal
    v = Vector((0,0,0))
    cnt = 0
    for f in mesh.polygons:  
        if f.select:
            cnt += 1
            v = v + f.normal
    
    zv = Vector((0,0,1))
    q = v.rotation_difference(zv)
            

    sx = 1 * sc
    sy = 1 * sc
    sz = 1 * sc
    ofx = xoffset_def
    ofy = yoffset_def
    rz = zrot_def / 180 * pi

    cosrz = cos(rz)
    sinrz = sin(rz)

    #uvs = mesh.uv_loop_layers[mesh.uv_loop_layers.active_index].data
    uvs = mesh.uv_layers.active.data
    for i, pol in enumerate(mesh.polygons):
        if not is_editmode or mesh.polygons[i].select:
            for j, loop in enumerate(mesh.polygons[i].loop_indices):
                v_idx = mesh.loops[loop].vertex_index

                n = pol.normal
                co = q @ (mesh.vertices[v_idx].co)
                
                x = co.x * sx
                y = co.y * sy
                z = co.z * sz
                uvs[loop].uv[0] =  x * cosrz - y * sinrz + xoffset_def
                uvs[loop].uv[1] =  aspect*(- x * sinrz - y * cosrz) + yoffset_def



    # Back to EDIT Mode
    if is_editmode:
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)






#**************************************************************************************************************************
#**************************************************************************************************************************
#**************************************************************************************************************************
# SureUVMOperator
#**************************************************************************************************************************

class SureUVWOperator(bpy.types.Operator):
    bl_idname = "object.sureuvw_operator"
    bl_label = "Sure UVW Map"
    bl_context = "data"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOL_PROPS"

    
    bl_options = {'REGISTER', 'UNDO'}

    
    action : StringProperty()  

    size : FloatProperty(name="Size", default=1.0, precision=4)
    rot : FloatVectorProperty(name="XYZ Rotation")
    offset : FloatVectorProperty(name="XYZ offset", precision=4)

    zrot : FloatProperty(name="Z rotation", default=0.0)
    xoffset : FloatProperty(name="X offset", default=0.0, precision=4)
    yoffset : FloatProperty(name="Y offset", default=0.0, precision=4)
    texaspect : FloatProperty(name="Texture aspect", default=1.0, precision=4)

    flag90 : BoolProperty()
    flag90ccw : BoolProperty()


    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH')

    def execute(self, context):
        #print('** execute **')
        #print(self.action)
        global all_scale_def,x_offset_def,y_offset_def,z_offset_def,x_rot_def,y_rot_def,z_rot_def, xoffset_def, yoffset_def, zrot_def, tex_aspect
                
        all_scale_def = self.size
        tex_aspect = self.texaspect
        
        x_offset_def = self.offset[0]
        y_offset_def = self.offset[1]
        z_offset_def = self.offset[2]
        x_rot_def = self.rot[0]
        y_rot_def = self.rot[1]
        z_rot_def = self.rot[2]

        xoffset_def = self.xoffset
        yoffset_def = self.yoffset
        zrot_def = self.zrot

        
        if self.flag90:
          self.zrot += 90
          zrot_def += 90
          self.flag90 = False

        if self.flag90ccw:
          self.zrot += -90
          zrot_def += -90
          self.flag90ccw = False

        
        if self.action == 'bestplanar':
            best_planar_map()
        elif self.action == 'box':
            box_map()

        
        #print('finish execute')
        return {'FINISHED'}

    def invoke(self, context, event):
        #print('** invoke **')
        #print(self.action)
        global all_scale_def,x_offset_def,y_offset_def,z_offset_def,x_rot_def,y_rot_def,z_rot_def, xoffset_def, yoffset_def, zrot_def, tex_aspect

        self.size = all_scale_def
        self.texaspect = tex_aspect
        self.offset[0] = x_offset_def
        self.offset[1] = y_offset_def
        self.offset[2] = z_offset_def
        self.rot[0] = x_rot_def
        self.rot[1] = y_rot_def
        self.rot[2] = z_rot_def

        
        self.xoffset = xoffset_def
        self.yoffset = yoffset_def
        self.zrot = zrot_def
        
            

        if self.action == 'bestplanar':
            best_planar_map()
        elif self.action == 'box':
            box_map()

            
        #print('finish invoke')
        return {'FINISHED'}


    def draw(self, context):
        if self.action == 'bestplanar' or self.action == 'rotatecw' or self.action == 'rotateccw':
            self.action = 'bestplanar'
   
            print("planar-draw")
                        
            layout = self.layout
                      
            layout.label(text="Size - "+self.action)
            layout.prop(self,'size',text="")
            layout.label(text="Z rotation")
            col = layout.column()
            col.prop(self,'zrot',text="")
            row = layout.row()
            row.prop(self,'flag90ccw',text="-90 (CCW)")
            row.prop(self,'flag90',text="+90 (CW)")
            layout.label(text="XY offset")
            col = layout.column()
            col.prop(self,'xoffset', text="")
            col.prop(self,'yoffset', text="")

            layout.label(text="Texture aspect")
            layout.prop(self,'texaspect', text="")

            #layout.prop(self,'preview_flag', text="Interactive Preview")
            #layout.operator("object.sureuvw_operator",text="Done").action='doneplanar'
            
        elif self.action == 'box':  

            print("boxmap-draw")

            layout = self.layout
            layout.use_property_split = True # Active single-column layout

            layout.label(text="UV Islands Modifiers:")
            layout.label(text="Scale")
            layout.prop(self,'size',text="")
            layout.label(text="XYZ rotation")
            col = layout.column()
            col.prop(self,'rot', text="")
            layout.label(text="XYZ offset")
            col = layout.column()
            col.prop(self,'offset', text="")
            layout.label(text="Aspect Ratio")

            layout.prop(self,'texaspect', text="")

            #layout.prop(self,'preview_flag', text="Interactive Preview")        
            #layout.operator("object.sureuvw_operator",text="Done").action='donebox'







#**************************************************************************************************************************
#**************************************************************************************************************************
#**************************************************************************************************************************
# SureUVMPanel
#**************************************************************************************************************************
    
class SureUVWPanel(bpy.types.Panel):
    bl_idname = "SUREUVW_PT_object_sureuvw_operator"
    bl_label = "Sure UVW Mapping"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UV"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH')


    def draw(self, context):
        
        layout = self.layout
        obj = context.active_object
        

        

        layout.label(text="UVW Mapping:")

        layout.operator(SureUVWOperator.bl_idname,text="UVW Box Map").action='box'
        layout.operator(SureUVWOperator.bl_idname,text="Best Planar Map").action='bestplanar'
        layout.label(text="1. Make Material With Raster Texture!")
        layout.label(text="2. Set Texture Mapping Coords: UV!")
        layout.label(text="3. Use Addon buttons")



def menu_SureUVW_BOX(self, context):
    self.layout.operator(SureUVWOperator.bl_idname,text="Sure UVW BOX").action='box'

def menu_SureUVW_BestPlanar(self, context):
    self.layout.operator(SureUVWOperator.bl_idname,text="Sure UVW Best Planar").action='bestplanar'    

#**************************************************************************************************************************
#**************************************************************************************************************************
#**************************************************************************************************************************
# Registration
#**************************************************************************************************************************
def register():
    #classes
    bpy.utils.register_class(SureUVWOperator)
    bpy.utils.register_class(SureUVWPanel)
    # menus    
    bpy.types.VIEW3D_MT_uv_map.append(menu_SureUVW_BOX)
    bpy.types.IMAGE_MT_uvs.append(menu_SureUVW_BOX)
    bpy.types.VIEW3D_MT_uv_map.append(menu_SureUVW_BestPlanar)
    bpy.types.IMAGE_MT_uvs.append(menu_SureUVW_BestPlanar)

def unregister():
    #classes
    bpy.utils.unregister_class(SureUVWOperator)
    bpy.utils.unregister_class(SureUVWPanel)
    # menus    
    bpy.types.VIEW3D_MT_uv_map.remove(menu_SureUVW_BOX)
    bpy.types.IMAGE_MT_uvs.remove(menu_SureUVW_BOX)
    bpy.types.VIEW3D_MT_uv_map.remove(menu_SureUVW_BestPlanar)
    bpy.types.IMAGE_MT_uvs.remove(menu_SureUVW_BestPlanar)



if __name__ == "__main__":
    register()
