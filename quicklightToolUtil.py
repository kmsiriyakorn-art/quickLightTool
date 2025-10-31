import maya.cmds as cmds

def create_light_by_role(name, role, color, intens , exp, size):
    """Create an Arnold light with the given role and QColor."""

    light = cmds.shadingNode("aiAreaLight", asLight=True, name=name)
    # Get the transform parent
    parent = cmds.listRelatives(light, parent=True)
    transform = parent[0] if parent else light
    newname = cmds.rename(transform,name)

    # Get RGB from QColor (0-1 float)
    r, g, b = color.redF(), color.greenF(), color.blueF()

    cmds.setAttr(f"{newname}.color", r, g, b, type="double3")

    if role.lower() == "key":
        cmds.setAttr(f"{newname}.translate", -4*size, 2*size, 4*size)
        cmds.setAttr(f"{newname}.rotate", 0, -45, 0)
        cmds.setAttr(f"{newname}.intensity", intens)
        cmds.setAttr(f"{newname}.exposure", exp)
        cmds.setAttr(f"{newname}.scale", size,size,size)
    
    elif role.lower() == "fill":
        cmds.setAttr(f"{newname}.translate", 4*size, 2*size, 4*size)
        cmds.setAttr(f"{newname}.rotate", 0, 45, 0)
        cmds.setAttr(f"{newname}.intensity", intens)
        cmds.setAttr(f"{newname}.exposure", exp)
        cmds.setAttr(f"{newname}.scale", size,size,size)
    
    elif role.lower() == "back":
        cmds.setAttr(f"{newname}.translate", -4*size, 6*size, -5*size)
        cmds.setAttr(f"{newname}.rotate", -20, -135, 0)
        cmds.setAttr(f"{newname}.intensity", intens)
        cmds.setAttr(f"{newname}.exposure", exp)
        cmds.setAttr(f"{newname}.scale", size,size,size)
        cmds.setAttr(f"{newname}.aiSpread", 0.2)

    print(f"Created {role} light '{newname}' with color RGB({r:.2f}, {g:.2f}, {b:.2f})")
    return transform
