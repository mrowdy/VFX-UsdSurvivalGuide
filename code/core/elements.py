"""This file contains all code examples for the 'Core Elements' section.
The following mdBook syntax allows us to sparsely import content:
#// ANCHOR: contentId
def example():
    print("here")
#// ANCHOR_END: contentId
"""

"""Path.md"""

#// ANCHOR: pathSummary
from pxr import Sdf
# Prims
prim_path = Sdf.Path("/set/bicycle")
prim_path_str = Sdf.Path("/set/bicycle").pathString # Returns the Python str "/set/bicycle"
# Properties (Attribute/Relationship)
property_path = Sdf.Path("/set/bicycle.size")
property_with_namespace_path = Sdf.Path("/set/bicycle.tire:size")
# Relationship targets
prim_rel_target_path = pxr.Sdf.Path("/set.bikes[/set/bicycles]")           # Prim to prim linking (E.g. path collections)
attribute_rel_target_path = pxr.Sdf.Path("/set.bikes[/set/bicycles].size") # Attribute to attribute linking (E.g. serializing node graph connections to Usd)
#// ANCHOR_END: pathSummary

#// ANCHOR: pathBasics
from pxr import Sdf
path = Sdf.Path("/set/bicycle")
path_name = path.name     # Similar to os.path.basename(), returns the last element of the path
path_empty = path.isEmpty # Property to check if path is empty
# Path validation (E.g. for user created paths)
Sdf.Path.IsValidPathString("/some/_wrong!_/path") # Returns: False, 'Error Message'
# Joint paths (Similar to os.path.join())
path = Sdf.Path("/set/bicycle")
path.AppendPath(Sdf.Path("frame/screws")) # Returns: Sdf.Path("/set/bicycle/frame/screws")
# Manually join individual path elements
path = Sdf.Path(Sdf.childDelimiter.join(["set", "bicycle"])) 
# Get the parent path
parent_path = path.GetParentPath() # Returns Sdf.Path("/set")
parent_path.IsRootPrimPath()       # Returns: True (Root prims are prims that only
                                   #                have a single '/')        
ancestor_range = path.GetAncestorsRange() # Returns an iterator for the parent paths, the same as recursively calling GetParentPath()
# Add child path
child_path = path.AppendChild("wheel") # Returns: Sdf.Path("/set/bicycle/wheel")
# Check if path is a prim path (and not a attribute/relationship path)
path.IsPrimPath() # Returns: True
# Check if path starts with another path
# Important: It actually compares individual path elements (So it is not a str.startswith())
Sdf.Path("/set/cityA/bicycle").HasPrefix(Sdf.Path("/set"))      # Returns: True
Sdf.Path("/set/cityA/bicycle").HasPrefix(Sdf.Path("/set/city")) # Returns: False
Sdf.Path("/set/bicycle").GetCommonPrefix(Sdf.Path("/set"))      # Returns: Sdf.Path("/set")
# Relative/Absolute paths
path = Sdf.Path("/set/cityA/bicycle")
rel_path = path.MakeRelativePath("/set")     # Returns: Sdf.Path('cityA/bicycle')
abs_path = rel_path.MakeAbsolutePath("/set") # Returns: Sdf.Path('/set/cityA/bicycle')
abs_path.IsAbsolutePath()                    # Returns: True -> Checks path[0] == "/"
# Do not use this is performance critical loops
# See for more info: https://openusd.org/release/api/_usd__page__best_practices.html
# This gives you a standard python string
path_str = path.pathString
#// ANCHOR_END: pathBasics

#// ANCHOR: pathSpecialPaths
from pxr import Sdf
# Shortcut for Sdf.Path("/")
root_path = Sdf.Path.absoluteRootPath
root_path == Sdf.Path("/") # Returns: True
# We'll cover in a later section how to rename/remove things in Usd,
# so don't worry about the details how this works yet. Just remember that
# an emptyPath exists and that its usage is to remove something.
src_path = Sdf.Path("/set/bicycle")
dst_path = Sdf.Path.emptyPath
edit = Sdf.BatchNamespaceEdit()
edit.Add(src_path, dst_path)
#// ANCHOR_END: pathSpecialPaths

#// ANCHOR: pathProperties
# Properties (see the next section) are also encoded
# in the path via the "." (Sdf.Path.propertyDelimiter) token
from pxr import Sdf
path = Sdf.Path("/set/bicycle.size")
property_name = path.name # Be aware, this will return 'size' (last element)
# Append property to prim path
Sdf.Path("/set/bicycle").AppendProperty("size") # Returns: Sdf.Path("/set/bicycle.size")
# Properties can also be namespaced with ":" (Sdf.Path.namespaceDelimiter)
path = Sdf.Path("/set/bicycle.tire:size").name 
property_name = path.name                 # Returns: 'tire:size'
property_name = path.ReplaceName("color") # Returns: Sdf.Path("/set/bicycle.color")
# Check if path is a property path (and not a prim path)
path.IsPropertyPath() # Returns: True
# Check if path is a property path (and not a prim path)
Sdf.Path("/set/bicycle.tire:size").IsPrimPropertyPath()  # Returns: True
Sdf.Path("/set/bicycle").IsPrimPropertyPath()            # Returns: False
# Convenience methods
path = Sdf.Path("/set/bicycle").AppendProperty(Sdf.Path.JoinIdentifier(["tire", "size"]))
namespaced_elements = Sdf.Path.TokenizeIdentifier("tire:size")   # Returns: ["tire", "size"]
last_element = Sdf.path.StripNamespace("/set/bicycle.tire:size") # Returns: 'size'
# With GetPrimPath we can strip away all property encodings
path = Sdf.Path("/set/bicycle.tire:size")
prim_path = path.GetPrimPath(path) # Returns: Sdf.Path('/set/bicycle')

# We can't actually differentiate between a attribute and relationship based on the property path.
# Hence the "Property" terminology.
# In practise we rarely use/see this as this is a pretty low level API usecase.
# The only 'common' case, where you will see this is when calling the Sdf.Layer.Traverse function.
# To encode prim relation targets, we can use:
prim_rel_target_path = Sdf.Path("/set.bikes[/set/bicycle]")
prim_rel_target_path.IsTargetPath() # Returns: True
prim_rel_target_path = Sdf.Path("/set.bikes").AppendTarget("/set/bicycle")
# We can also encode attribute relation targets (For example shader node graph connections):
attribute_rel_target_path = pxr.Sdf.Path("/set.bikes[/set/bicycles].size")
attribute_rel_target_path.IsRelationalAttributePath()  # Returns: True
#// ANCHOR_END: pathProperties

#// ANCHOR: pathVariants
# Variants (see the next sections) are also encoded
# in the path via the "{variantSetName=variantName}" syntax.
from pxr import Sdf
path = Sdf.Path("/set/bicycle")
variant_path = path.AppendVariantSelection("style", "blue") # Returns: Sdf.Path('/set/bicycle{style=blue}')
variant_path = Sdf.Path('/set/bicycle{style=blue}frame/screws')
# Property path to prim path with variants
property_path = Sdf.Path('/set/bicycle{style=blue}frame/screws.size')
variant_path = property_path.GetPrimOrPrimVariantSelectionPath() # Returns: Sdf.Path('/set/bicycle{style=blue}frame/screws')
# Typical iteration example:
variant_path = Sdf.Path('/set/bicycle{style=blue}frame/screws')
if variant_path.ContainsPrimVariantSelection():          # Returns: True # For any variant selection in the whole path
    for parent_path in variant_path.GetAncestorRange():
        if parent_path.IsPrimVariantSelectionPath():
            print(parent_path.GetVariantSelection())     # Returns: ('style', 'blue')

# When authoring relationships, we usually want to remove all variant encodings in the path:
variant_path = Sdf.Path('/set/bicycle{style=blue}frame/screws')
prim_rel_target_path = variant_path.StripAllVariantSelections() # Returns: Sdf.Path('/set/bicycle/frame/screws')
#// ANCHOR_END: pathVariants