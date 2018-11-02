# vim:ts=4:et
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import bpy
from mathutils import Vector, Quaternion
from bpy_extras.io_utils import ImportHelper
from bpy.props import BoolProperty, StringProperty

from .importerror import MuImportError
#from . import import_mu

def import_mu_op(self, context, filepath, create_colliders, force_armature):
    operator = self
    undo = bpy.context.user_preferences.edit.use_global_undo
    bpy.context.user_preferences.edit.use_global_undo = False

    collection = bpy.context.layer_collection.collection
    try:
        from . import import_mu
        obj = import_mu(collection, filepath, create_colliders, force_armature)
    except MuImportError as e:
        operator.report({'ERROR'}, e.message)
        return {'CANCELLED'}
    else:
        for o in bpy.context.scene.objects:
            o.select_set('DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.location = context.scene.cursor_location
        obj.rotation_quaternion = Quaternion((1, 0, 0, 0))
        obj.scale = Vector((1, 1, 1))
        obj.select_set('SELECT')
        return {'FINISHED'}
    finally:
        bpy.context.user_preferences.edit.use_global_undo = undo

class KSPMU_OT_ImportMu(bpy.types.Operator, ImportHelper):
    '''Load a KSP Mu (.mu) File'''
    bl_idname = "import_object.ksp_mu"
    bl_label = "Import Mu"
    bl_description = """Import a KSP .mu model."""
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".mu"
    filter_glob: StringProperty(default="*.mu", options={'HIDDEN'})

    create_colliders: BoolProperty(name="Create Colliders",
            description="Disable to import only visual and hierarchy elements",
                                    default=True)
    force_armature: BoolProperty(name="Force Armature",
            description="Enable to force use of an armature to hold the model"
                        " hierarchy", default=False)

    def execute(self, context):
        keywords = self.as_keywords (ignore=("filter_glob",))
        return import_mu_op(self, context, **keywords)
