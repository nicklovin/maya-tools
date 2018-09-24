import maya.cmds as mc

aboutText = '''
This tool was created with the intention of making the process of control 
creation and choice significantly easier for the rigger.

Instructions:
    Naming:
        Choose a naming convention for any controls you wish to create.
        All curve controls will default to the name that matches its button 
            unless otherwise specified in the 'Name' textfield.
        The 'Prefix' and 'Suffix' textfields allow additional levels of naming 
            specificity as desired, and will automatically add an underscore.
        If either textfield contains characters, but the 'Name' textfield does 
            not, the control will not be renamed.
        If the 'Override Name' checkbox is on, the tool will automatically read
            the selection (which should be a joint) and use the its name to 
            detemine the name of the new control.  This works best with the 
            suffixes '_JNT' or '_BONE'.  If neither of those suffixes are found,
            the tool will assume the suffix is the last 4 characters (example:
            '_Jnt', '_jnt', etc.) and replace those for the control name.
    Grouping:
        Check the box next to whichever additional group layers you would desire 
            to have above your control.
        'ZERO' will always be the top group, regardless of order the boxes were 
            checked in.
        'Other' allows the rigger to create their own group with their own 
            naming convention, specified in the textfield next to it.
        If 'Other' is check, but nothing is specified in the textfield, a 'NULL' 
            group will be created in the hierarchy
    Curves:
        Click on the button of the desired curve.  Above options should be 
            filled out before creating the curve.
        20 options for curve choices to be created. (More in future edits)
        Most controls are also made with additional CV's to allow the rigger to 
            add an additional curve of preference to certain curves.
    Colors:
        9 Color options for curve clarity.
        First 6 are the most common used colors, with strong distinguishment 
            among sides and similar colors.
        Custom Color option:
            Opens a color editor that allows the user to select any color that
            Maya has available.
    Lock and Hide:
        Check the boxes for all applicable attributes that should be modified.
        Modifications include locking, hiding, unlocking, and unhiding 
            attributes.
        The 'All' checkboxes intuitively will also activate the corresponding 
            checkboxes relating to their position/label.
    Attributes:
        Attribute write-ins commonly used controls and the additional attributes 
            needed for each.
        Any buttons not enabled are not currently connected to a command (coming 
            soon).
        Section still Work-In-Prother_group_valueress, looking for more buttons 
            to add.
        
Tool Created by Nicholas Love

Please send all bugs/glitches and tool requests to 
nicklove.productions@gmail.com

Other tools can be found at https://www.nicholasjameslove.com/

''
Update 06/06/2018:

    Adapted the naming conventions to match those used when rigging at The Mill.
        ZERO replaced offset.
        SDK and others now capitalized.
        SRT replaced attr.
        Added the following: SPACE, OFS, DUMMY
    Numbering conditions reformatted so the number comes before the suffixes.
        New format: PREFIX_NAME_'##'_SUFFIX and PREFIX_NAME_'##'_SUFFIX_GRP
        Allows for easier name-based selections
''
Update 06/21/2018:
    
    Override Name checkbox added in Naming section.
        When checked, the window will ignore any text input into the 3 
            textFields.
        Instead, the window will read the name of the selected object, and base 
                its name off of that.
            Replaces the suffix of the selection with '_CTRL'
            Works best with proper naming conventions on joints:
                '_JNT' and '_BONE' are automatically recother_group_valuenized 
                and adapted.
            If the naming conventions do not align, the window will assume the 
            last 3 characters of the selection are the replaceable suffix.
                ex: '_FKJnt' will be converted to '_FKCTRL'
    Added a custom color button to allow for color selections beyond the 9 
    provided colors.
        Allows total control over color choice, all colors are possible.
    Added a help menu so that the user no longer needs to read through the 
    script editor to learn how to use the window.
        Setup for more menuItems in the future, but not using them yet.
        
''
Update 06/29/2018:
    
    Lock & Hide Attributes menu finally added.
        Options to lock/unlock/hide/show the 10 default attributes.
        Allows for selected attributes to also be locked when selected.
    Change Command options added
        Now the 'Override Name' and 'Other' checkboxes affect if the related 
        textfields are active.
        In the lock and hide section, the 'All' row will activate all checkboxes 
        in that area.
''
Update 07/06/2018:

    PEP8 format update:
        Tool reformatted to match PEP8 standards as work practice and to enhance
            readability for future users.
''
Upcoming updates:
    Update Attributes
        More streamlined
        Option for space switches to work as ENUM, adding new options with each 
        button.
    Rewrite of entire build to be properly optimized and size reduced
    Conversion of UI to PyQt
    Appropriate docstring documentation on each function
        Added once functions are put under control of less functions rather than
        separate for every possible control/color/attribute/etc. setup
    
'''

##################################################


# global variables
attributes = [
    '.tx', '.ty', '.tz',
    '.rx', '.ry', '.rz',
    '.sx', '.sy', '.sz',
    '.v'
]

# Rename Function #


def curve_rename(x, y, z, q):

    curve_prefix = mc.textField('CurvePrefix', query=True, text=True)
    curve_name = mc.textField('CurveName', query=True, text=True)
    curve_suffix = mc.textField('CurveSuffix', query=True, text=True)
    override_value = mc.checkBox('overrideName', query=True, value=True)

    length_prefix = len(curve_prefix)
    length_name = len(curve_name)
    length_suffix = len(curve_suffix)
    length_selection = len(y)
    a = z + 1
    length_string = str(a).zfill(2)

    ovlength_suffix = len(q)
    condition_jnt = ovlength_suffix - 3
    condition_bone = ovlength_suffix - 4
    condition_other = ovlength_suffix - 3
    override_jnt = q[condition_jnt:ovlength_suffix]
    override_bone = q[condition_bone:ovlength_suffix]
    override_other = q[condition_other:ovlength_suffix]

    if override_value == 1:
        if override_jnt == 'JNT':
            mc.rename(x, q.replace('JNT', 'CTRL'))
            print 'JNT'
        elif override_jnt != 'JNT':
            if override_bone == 'BONE':
                mc.rename(x, q.replace('BONE', 'CTRL'))
                print 'BONE'
            elif override_bone != 'BONE':
                mc.rename(x, q.replace(override_other, 'CTRL'))
                print 'OTHER'
    elif override_value == 0:
        if length_selection > 1:
            if length_prefix > 0 and length_name > 0 and length_suffix > 0:
                mc.rename(x, (curve_prefix + '_' + curve_name + '_'
                              + curve_suffix))
            elif length_prefix == 0 and length_name > 0 and length_suffix > 0:
                mc.rename(x, (curve_name + '_' + length_string + '_'
                              + curve_suffix))
            elif length_prefix > 0 and length_name > 0 and length_suffix == 0:
                mc.rename(x, (curve_prefix + '_' + curve_name + '_' +
                              length_string))
            elif length_prefix > 0 and length_name == 0 and length_suffix > 0:
                mc.rename(x, (curve_prefix + '_' + x + '_' + length_string + '_'
                              + curve_suffix))
            elif length_prefix == 0 and length_name > 0 and length_suffix == 0:
                mc.rename(x, curve_name + '_' + length_string)
            elif length_prefix > 0 and length_name == 0 and length_suffix == 0:
                mc.rename(x, (curve_prefix + '_' + x[0] + '_' + length_string))
            elif length_prefix == 0 and length_name == 0 and length_suffix > 0:
                mc.rename(x, (x[0] + '_' + length_string + '_' + curve_suffix))
            else:
                print x
        elif length_selection < 2:
            if length_prefix > 0 and length_name > 0 and length_suffix > 0:
                mc.rename(x, (curve_prefix + '_' + curve_name + '_'
                              + curve_suffix))
            elif length_prefix == 0 and length_name > 0 and length_suffix > 0:
                mc.rename(x, (curve_name + '_' + curve_suffix))
            elif length_prefix > 0 and length_name > 0 and length_suffix == 0:
                mc.rename(x, (curve_prefix + '_' + curve_name))
            elif length_prefix > 0 and length_name == 0 and length_suffix > 0:
                mc.rename(x, (curve_prefix + '_' + x + '_' + curve_suffix))
            elif length_prefix == 0 and length_name > 0 and length_suffix == 0:
                mc.rename(x, curve_name)
            elif length_prefix > 0 and length_name == 0 and length_suffix == 0:
                mc.rename(x, (curve_prefix + '_' + x[0]))
            elif length_prefix == 0 and length_name == 0 and length_suffix > 0:
                mc.rename(x, (x[0] + '_' + curve_suffix))
            else:
                print x

# Grouping Options #


def grp(*arg):
    group_selection = mc.ls(sl=True)

    zero = mc.checkBox('zeroBox', query=True, value=True)
    srt = mc.checkBox('srtBox', query=True, value=True)
    sdk = mc.checkBox('sdkBox', query=True, value=True)
    space = mc.checkBox('spaceBox', query=True, value=True)
    offset = mc.checkBox('ofsBox', query=True, value=True)
    dummy = mc.checkBox('dummyBox', query=True, value=True)
    other = mc.checkBox('otherBox', query=True, value=True)
    other_group_value = mc.textField('otherGrp', query=True, text=True)
    curve_suffix = mc.textField('CurveSuffix', query=True, text=True)
    override_value = mc.checkBox('overrideName', query=True, value=True)
    other_group_length = len(other_group_value)

    if override_value == 1:
        if srt is True:
            mc.group(n=(group_selection[0].replace('CTRL', 'SRT')))
        if sdk is True:
            mc.group(n=(group_selection[0].replace('CTRL', 'SDK')))
        if space is True:
            mc.group(n=(group_selection[0].replace('CTRL', 'SPACE')))
        if dummy is True:
            mc.group(n=(group_selection[0].replace('CTRL', 'DUMMY')))
        if other is True:
            if other_group_length == 0:
                mc.group(n=(group_selection[0].replace('CTRL', 'NULL')))
            else:
                mc.group(n=(group_selection[0].replace('CTRL',
                         other_group_value)))
        if offset is True:
            mc.group(n=(group_selection[0].replace('CTRL', 'OFS')))
        if zero is True:
            mc.group(n=(group_selection[0].replace('CTRL', 'ZERO')))
    elif override_value == 0:
        if srt is True:
            mc.group(n=(group_selection[0].replace(curve_suffix, 'SRT')))
        if sdk is True:
            mc.group(n=(group_selection[0].replace(curve_suffix, 'SDK')))
        if space is True:
            mc.group(n=(group_selection[0].replace(curve_suffix, 'SPACE')))
        if dummy is True:
            mc.group(n=(group_selection[0].replace(curve_suffix, 'DUMMY')))
        if other is True:
            if other_group_length == 0:
                mc.group(n=(group_selection[0].replace(curve_suffix, 'NULL')))
            else:
                mc.group(n=(group_selection[0].replace(curve_suffix,
                         other_group_value)))
        if offset is True:
            mc.group(n=(group_selection[0].replace(curve_suffix, 'OFS')))
        if zero is True:
            mc.group(n=(group_selection[0].replace(curve_suffix, 'ZERO')))

# Snap to Point #


def snap_position(list, size):
    ctrl_selection = mc.ls(sl=True)
    for s in range(size):
        temp_constraint = mc.parentConstraint(list[s], ctrl_selection[0],
                                              mo=False, w=1)
        mc.delete(temp_constraint)


# Curve Creations #


def cir(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        mc.circle(nr=[0, 1, 0], n='circle_01')
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.circle(nr=[0, 1, 0], n='circle_01')
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def square(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        mc.circle(nr=[0, 1, 0], degree=1, sections=4, n='square_01')
        mc.rotate(0, 45, 0)
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.circle(nr=[0, 1, 0], degree=1, sections=4, n='square_01')
            mc.rotate(0, 45, 0)
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def triangle(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        mc.circle(nr=[0, 1, 0], degree=1, sections=3, n='triangle_01')
        mc.rotate(0, -90, 0)
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.circle(nr=[0, 1, 0], degree=1, sections=3, n='triangle_01')
            mc.rotate(0, -90, 0)
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def octagon(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        mc.circle(nr=[0, 1, 0], degree=1, sections=8, n='octagon_01')
        mc.rotate(0, 45, 0)
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.circle(nr=[0, 1, 0], degree=1, sections=8, n='octagon_01')
            mc.rotate(0, 45, 0)
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def sphere(*arg):

    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # Create curves
        c1 = mc.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1, d=3, ut=0, ch=1,
                       n='sphere_01')
        c2 = mc.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1, d=3, ut=0, ch=1)
        mc.rotate(90, 0, 0)
        c3 = mc.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1, d=3, ut=0, ch=1)
        mc.rotate(0, 0, 90)
        # Freeze the rotated curves
        mc.select(c2)
        mc.select(c3, add=True)
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        # Parent shapes of curves 2 and 3 to curve 1
        rc2 = mc.listRelatives(c2, shapes=True)
        mc.parent(rc2[0], c1, r=True, shape=True)
        rc3 = mc.listRelatives(c3, shapes=True)
        mc.parent(rc3[0], c1, r=True, shape=True)
        mc.pickWalk(d='up')
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            # Create curves
            c1 = mc.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1, d=3, ut=0,
                           ch=1, n='sphere_01')
            c2 = mc.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1, d=3, ut=0,
                           ch=1)
            mc.rotate(90, 0, 0)
            c3 = mc.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1, d=3, ut=0,
                           ch=1)
            mc.rotate(0, 0, 90)
            # Freeze the rotated curves
            mc.select(c2)
            mc.select(c3, add=True)
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            # Parent shapes of curves 2 and 3 to curve 1
            rc2 = mc.listRelatives(c2, shapes=True)
            mc.parent(rc2[0], c1, r=True, shape=True)
            rc3 = mc.listRelatives(c3, shapes=True)
            mc.parent(rc3[0], c1, r=True, shape=True)
            mc.pickWalk(d='up')
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            mc.delete(constructionHistory=True)

            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)

            # Delete the transform node of curves 2 and 3
            mc.select(c2[0])
            mc.select(c3[0], add=True)
            mc.delete()


def box(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # box curve line
        mc.curve(d=1, p=[(0.5, 0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5),
                         (0.5, 0.5, -0.5,), (0.5, 0.5, 0.5,), (0.5, -0.5, 0.5,),
                         (0.5, -0.5, -0.5,), (0.5, 0.5, -0.5,),
                         (-0.5, 0.5, -0.5,), (-0.5, -0.5, -0.5,),
                         (-0.5, -0.5, 0.5,), (-0.5, 0.5, 0.5,),
                         (-0.5, -0.5, 0.5,), (0.5, -0.5, 0.5,),
                         (0.5, -0.5, -0.5,), (-0.5, -0.5, -0.5,)], n='box_01')
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            # box curve line
            mc.curve(d=1, p=[(0.5, 0.5, 0.5), (-0.5, 0.5, 0.5),
                             (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5,),
                             (0.5, 0.5, 0.5,), (0.5, -0.5, 0.5,),
                             (0.5, -0.5, -0.5,), (0.5, 0.5, -0.5,),
                             (-0.5, 0.5, -0.5,), (-0.5, -0.5, -0.5,),
                             (-0.5, -0.5, 0.5,), (-0.5, 0.5, 0.5,),
                             (-0.5, -0.5, 0.5,), (0.5, -0.5, 0.5,),
                             (0.5, -0.5, -0.5,), (-0.5, -0.5, -0.5,)],
                     n='box_01')
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def pyramid(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # pyramid curve line
        mc.curve(d=1, p=[(9.27258e-008, -0.353553, -0.707107), (-0.707107,
                         -0.353553, -6.18172e-008), (0, 0.353553, 0),
                         (9.27258e-008, -0.353553, -0.707107), (0.707107,
                         -0.353553, 0), (0, 0.353553, 0), (-3.09086e-008,
                         -0.353553, 0.707107), (0.707107, -0.353553, 0),
                         (-3.09086e-008, -0.353553, 0.707107), (-0.707107,
                         -0.353553, -6.18172e-008)], n='pyramid_01')
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.curve(d=1, p=[(9.27258e-008, -0.353553, -0.707107), (-0.707107,
                             -0.353553, -6.18172e-008), (0, 0.353553, 0),
                             (9.27258e-008, -0.353553, -0.707107), (0.707107,
                             -0.353553, 0), (0, 0.353553, 0), (-3.09086e-008,
                             -0.353553, 0.707107), (0.707107, -0.353553, 0),
                             (-3.09086e-008, -0.353553, 0.707107), (-0.707107,
                             -0.353553, -6.18172e-008)], n='pyramid_01')
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def diamond(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # diamond curve line
        mc.curve(d=1, p=[(0, 1, 0), (1, 0, 0), (0, 0, 1), (0, 1, 0), (0, 0, -1),
                         (-1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0),
                         (0, -1, 0), (0, 0, 1), (1, 0, 0), (0, -1, 0),
                         (0, 0, -1), (1, 0, 0)], n='diamond_01')
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.curve(d=1, p=[(0, 1, 0), (1, 0, 0), (0, 0, 1), (0, 1, 0),
                             (0, 0, -1), (-1, 0, 0), (0, 1, 0), (0, 0, 1),
                             (-1, 0, 0), (0, -1, 0), (0, 0, 1), (1, 0, 0),
                             (0, -1, 0), (0, 0, -1), (1, 0, 0)], n='diamond_01')
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def quad_arrow(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # arrow curve line
        mc.curve(d=1, p=[(1, 0, -1), (1, 0, -3), (2, 0, -3), (0, 0, -5),
                         (-2, 0, -3), (-1, 0, -3), (-1, 0, -1), (-3, 0, -1),
                         (-3, 0, -2), (-5, 0, 0), (-3, 0, 2), (-3, 0, 1),
                         (-1, 0, 1), (-1, 0, 3), (-2, 0, 3), (0, 0, 5),
                         (2, 0, 3), (1, 0, 3), (1, 0, 1), (3, 0, 1),
                         (3, 0, 2), (5, 0, 0), (3, 0, -2), (3, 0, -1),
                         (1, 0, -1)], n='quad_arrow_01')
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.curve(d=1, p=[(1, 0, -1), (1, 0, -3), (2, 0, -3), (0, 0, -5),
                             (-2, 0, -3), (-1, 0, -3), (-1, 0, -1), (-3, 0, -1),
                             (-3, 0, -2), (-5, 0, 0), (-3, 0, 2), (-3, 0, 1),
                             (-1, 0, 1), (-1, 0, 3), (-2, 0, 3), (0, 0, 5),
                             (2, 0, 3), (1, 0, 3), (1, 0, 1), (3, 0, 1),
                             (3, 0, 2), (5, 0, 0), (3, 0, -2), (3, 0, -1),
                             (1, 0, -1)], n='quad_arrow_01')
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def curved_plane(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # plane curve line
        mc.curve(d=3, n='curvedPlane_01', p=[(5, 0, -1), (5, 0, -1), (5, 0, -1),
                                             (2, 3, -1), (-2, 3, -1), (-5, 0,
                                             -1), (-5, 0, -1), (-5, 0, -1), (-5,
                                             0, -1), (-5, 0, 1), (-5, 0, 1),
                                             (-5, 0, 1), (-5, 0, 1), (-2, 3, 1),
                                             (2, 3, 1), (5, 0, 1), (5, 0, 1),
                                             (5, 0, 1), (5, 0, 1), (5, 0, -1)])
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.curve(d=3, n='curvedPlane_01', p=[(5, 0, -1), (5, 0, -1), (5, 0,
                                                 -1), (2, 3, -1), (-2, 3, -1),
                                                 (-5, 0, -1), (-5, 0, -1), (-5,
                                                 0, -1), (-5, 0, -1), (-5, 0,
                                                 1), (-5, 0, 1), (-5, 0, 1),
                                                 (-5, 0, 1), (-2, 3, 1), (2, 3,
                                                 1), (5, 0, 1), (5, 0, 1), (5,
                                                 0, 1), (5, 0, 1), (5, 0, -1)])
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def icosah(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # icosah curve line
        mc.curve(d=1, n='iso_01', p=[(-0.525731, 0.850651, 0), (0.525731,
                                     0.850651, 0), (0, 0.525731, 0.850651),
                                     (-0.525731, 0.850651, 0), (-0.850651, 0,
                                     0.525731), (0, 0.525731, 0.850651), (0,
                                     -0.525731, 0.850651), (-0.850651, 0,
                                     0.525731), (-0.525731, -0.850651, 0), (0,
                                     -0.525731, 0.850651), (0.525731,
                                     -0.850651, 0), (-0.525731, -0.850651, 0),
                                     (0, -0.525731, -0.850651), (0.525731,
                                     -0.850651, 0), (0.850651, 0, -0.525731),
                                     (0, -0.525731, -0.850651), (0, 0.525731,
                                     -0.850651), (0.850651, 0, -0.525731),
                                     (0.525731, 0.850651, 0), (0, 0.525731,
                                     -0.850651), (-0.525731, 0.850651, 0),
                                     (-0.850651, 0, -0.525731), (-0.850651, 0,
                                     0.525731), (-0.525731, -0.850651, 0),
                                     (-0.850651, 0, -0.525731), (0, -0.525731,
                                     -0.850651), (0, 0.525731, -0.850651),
                                     (-0.850651, 0, -0.525731), (-0.525731,
                                     -0.850651, 0), (0.525731, -0.850651, 0),
                                     (0.850651, 0, 0.525731), (0, -0.525731,
                                     0.850651), (0, 0.525731, 0.850651),
                                     (0.850651, 0, 0.525731), (0.525731,
                                     0.850651, 0), (0.850651, 0, -0.525731),
                                     (0.850651, 0, 0.525731)])
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.curve(d=1, p=[(-0.525731, 0.850651, 0), (0.525731, 0.850651, 0),
                             (0, 0.525731, 0.850651), (-0.525731, 0.850651, 0),
                             (-0.850651, 0, 0.525731), (0, 0.525731, 0.850651),
                             (0, -0.525731, 0.850651), (-0.850651, 0,
                             0.525731), (-0.525731, -0.850651, 0), (0,
                             -0.525731, 0.850651), (0.525731, -0.850651, 0),
                             (-0.525731, -0.850651, 0), (0, -0.525731,
                             -0.850651), (0.525731, -0.850651, 0), (0.850651,
                             0, -0.525731), (0, -0.525731, -0.850651), (0,
                             0.525731, -0.850651), (0.850651, 0, -0.525731),
                             (0.525731, 0.850651, 0), (0, 0.525731, -0.850651),
                             (-0.525731, 0.850651, 0), (-0.850651, 0,
                             -0.525731), (-0.850651, 0, 0.525731), (-0.525731,
                             -0.850651, 0), (-0.850651, 0, -0.525731), (0,
                             -0.525731, -0.850651), (0, 0.525731, -0.850651),
                             (-0.850651, 0, -0.525731), (-0.525731, -0.850651,
                             0), (0.525731, -0.850651, 0), (0.850651, 0,
                             0.525731), (0, -0.525731, 0.850651), (0,
                             0.525731, 0.850651), (0.850651, 0, 0.525731),
                             (0.525731, 0.850651, 0), (0.850651, 0, -0.525731),
                             (0.850651, 0, 0.525731)], n='iso_01')
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def lever(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        stand = mc.curve(d=1, p=[(0, 0, 0), (0, 3, 0)], n='lever_01')
        handle = mc.circle(nr=[0, 0, 1])
        mc.move(0, 4, 0)
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        handle_shape = mc.listRelatives(handle, shapes=True)
        mc.parent(handle_shape[0], stand, r=True, s=True)
        mc.pickWalk(d='up')
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
        mc.move(0, 0, 0, ".scalePivot", ".rotatePivot")
        mc.delete(handle[0])
    else:
        for curve_number in range(snap_list_size):
            stand = mc.curve(d=1, p=[(0, 0, 0), (0, 3, 0)], n='lever_01')
            handle = mc.circle(nr=[0, 0, 1])
            mc.move(0, 4, 0)
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            handle_shape = mc.listRelatives(handle, shapes=True)
            mc.parent(handle_shape[0], stand, r=True, s=True)
            mc.pickWalk(d='up')
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            mc.delete(constructionHistory=True)
            grp()
            mc.move(0, 0, 0, ".scalePivot", ".rotatePivot")
            mc.delete(handle[0])
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def arrow(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        mc.curve(d=3,  p=[(-1, 0, -3), (-1, 0, -3), (-1, 0, -3), (-2, 0, -3),
                          (-2, 0, -3), (-2, 0, -3), (-2, 0, -3), (0, 0, -5),
                          (0, 0, -5), (0, 0, -5), (0, 0, -5), (2, 0, -3),
                          (2, 0, -3), (2, 0, -3), (2, 0, -3), (1, 0, -3),
                          (1, 0, -3), (1, 0, -3), (1, 0, -3), (1, 0, -2),
                          (1, 0, -1), (1, 0, 0), (1, 0, 1), (1, 0, 2),
                          (1, 0, 3), (1, 0, 3), (1, 0, 3), (1, 0, 3),
                          (-1, 0, 3), (-1, 0, 3), (-1, 0, 3), (-1, 0, 3),
                          (-1, 0, 2), (-1, 0, 1), (-1, 0, 0), (-1, 0, -1),
                          (-1, 0, -2), (-1, 0, -3)], n='arrow_01')
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.curve(d=3, p=[(-1, 0, -3), (-1, 0, -3), (-1, 0, -3), (-2, 0, -3),
                             (-2, 0, -3), (-2, 0, -3), (-2, 0, -3), (0, 0, -5),
                             (0, 0, -5), (0, 0, -5), (0, 0, -5), (2, 0, -3),
                             (2, 0, -3), (2, 0, -3), (2, 0, -3), (1, 0, -3),
                             (1, 0, -3), (1, 0, -3), (1, 0, -3), (1, 0, -2),
                             (1, 0, -1), (1, 0, 0), (1, 0, 1), (1, 0, 2),
                             (1, 0, 3), (1, 0, 3), (1, 0, 3), (1, 0, 3),
                             (-1, 0, 3), (-1, 0, 3), (-1, 0, 3), (-1, 0, 3),
                             (-1, 0, 2), (-1, 0, 1), (-1, 0, 0), (-1, 0, -1),
                             (-1, 0, -2), (-1, 0, -3)], n='arrow_01')            
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, 
                            pn=True)
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def palm(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        mc.curve(d=3, p=[(-2, 0, 3), (-2, 0, 3), (-2, 0, 3), (0, 0, 2),
                         (2, 0, 3), (2, 0, 3), (2, 0, 3), (2, 0, 3), (4, 0, -5),
                         (4, 0, -5), (4, 0, -5), (4, 0, -5), (0, 0, -7),
                         (-4, 0, -5), (-4, 0, -5), (-4, 0, -5), (-4, 0, -5),
                         (-2, 0, 3)], n='palmCurve_01')
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.curve(d=3, p=[(-2, 0, 3), (-2, 0, 3), (-2, 0, 3), (0, 0, 2),
                             (2, 0, 3), (2, 0, 3), (2, 0, 3), (2, 0, 3),
                             (4, 0, -5), (4, 0, -5), (4, 0, -5), (4, 0, -5),
                             (0, 0, -7), (-4, 0, -5), (-4, 0, -5), (-4, 0, -5),
                             (-4, 0, -5), (-2, 0, 3)], n='palmCurve_01')
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def plus(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        mc.curve(d=1,  p=[(-1, 0, -1), (-1, 0, -3), (1, 0, -3), (1, 0, -1),
                          (3, 0, -1), (3, 0, 1), (1, 0, 1), (1, 0, 3),
                          (-1, 0, 3), (-1, 0, 1), (-3, 0, 1), (-3, 0, -1),
                          (-1, 0, -1)], n='plus_01')
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.curve(d=1, p=[(-1, 0, -1), (-1, 0, -3), (1, 0, -3), (1, 0, -1),
                             (3, 0, -1), (3, 0, 1), (1, 0, 1), (1, 0, 3),
                             (-1, 0, 3), (-1, 0, 1), (-3, 0, 1), (-3, 0, -1),
                             (-1, 0, -1)], n='plus_01')
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def loc(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        mc.spaceLocator()
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.spaceLocator()
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def trapezoid_cube(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        mc.curve(d=1,  p=[(-0.5, 0.5, 0.5), (-1, 0, 1), (1, 0, 1), (0.5, 0.5,
                          0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (-1, 0,
                          -1), (-1, 0, 1), (-0.5, -0.5, 0.5), (-0.5, -0.5,
                          -0.5), (-1, 0, -1), (1, 0, -1), (0.5, -0.5, -0.5),
                          (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (0.5, -0.5,
                          0.5), (0.5, -0.5, -0.5), (1, 0, -1), (0.5, 0.5, -0.5),
                          (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5),
                          (1, 0, 1), (0.5, -0.5, 0.5), (1, 0, 1), (1, 0, -1)],
                 n='trapezoid_cube_01')
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.curve(d=1, p=[(-0.5, 0.5, 0.5), (-1, 0, 1), (1, 0, 1), (0.5, 0.5,
                             0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (-1, 0,
                             -1), (-1, 0, 1), (-0.5, -0.5, 0.5), (-0.5, -0.5,
                             -0.5), (-1, 0, -1), (1, 0, -1), (0.5, -0.5, -0.5),
                             (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (0.5, -0.5,
                             0.5), (0.5, -0.5, -0.5), (1, 0, -1), (0.5, 0.5,
                             -0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5,
                             0.5, 0.5), (1, 0, 1), (0.5, -0.5, 0.5), (1, 0, 1),
                             (1, 0, -1)], n='trapezoid_cube_01')
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def ring(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        mc.curve(d=1,  p=[(0.707107, 0.1, 0.707107), (1, 0.1, 0), (1, -0.1, 0), 
                          (0.707107, -0.1, -0.707107), (0.707107, 0.1, 
                          -0.707107), (0, 0.1, -1), (0, -0.1, -1), (-0.707107, 
                          -0.1, -0.707107), (-0.707107, 0.1, -0.707107), (-1, 
                          0.1, 0), (-1, -0.1, 0), (-0.707107, -0.1, 0.707107), 
                          (-0.707107, 0.1, 0.707107), (0, 0.1, 1), (0, -0.1, 1), 
                          (0.707107, -0.1, 0.707107), (0.707107, 0.1, 0.707107), 
                          (0, 0.1, 1), (0, -0.1, 1), (-0.707107, -0.1, 
                          0.707107), (-0.707107, 0.1, 0.707107), (-1, 0.1, 0), 
                          (-1, -0.1, 0), (-0.707107, -0.1, -0.707107), 
                          (-0.707107, 0.1, -0.707107), (0, 0.1, -1), (0, -0.1, 
                          -1), (0.707107, -0.1, -0.707107), (0.707107, 0.1, 
                          -0.707107), (1, 0.1, 0), (1, -0.1, 0), (0.707107, 
                          -0.1, 0.707107)],  n='ring_01')
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.curve(d=1,
                     p=[(0.707107, 0.1, 0.707107), (1, 0.1, 0), (1, -0.1, 0),
                        (0.707107, -0.1, -0.707107), (0.707107, 0.1,
                        -0.707107), (0, 0.1, -1), (0, -0.1, -1), (-0.707107,
                        -0.1, -0.707107), (-0.707107, 0.1, -0.707107), (-1,
                        0.1, 0), (-1, -0.1, 0), (-0.707107, -0.1, 0.707107),
                        (-0.707107, 0.1, 0.707107), (0, 0.1, 1), (0, -0.1, 1),
                        (0.707107, -0.1, 0.707107), (0.707107, 0.1, 0.707107),
                        (0, 0.1, 1), (0, -0.1, 1), (-0.707107, -0.1,
                        0.707107), (-0.707107, 0.1, 0.707107), (-1, 0.1, 0),
                        (-1, -0.1, 0), (-0.707107, -0.1, -0.707107),
                        (-0.707107, 0.1, -0.707107), (0, 0.1, -1), (0, -0.1,
                        -1), (0.707107, -0.1, -0.707107), (0.707107, 0.1,
                        -0.707107), (1, 0.1, 0), (1, -0.1, 0), (0.707107,
                        -0.1, 0.707107)], n='ring_01')
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def tube(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # creating the curves
        t1 = mc.curve(d=2, p=[(1, 2, 0), (1, 0, 0), (1, -2, 0)])
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        t2 = mc.curve(d=2, p=[(-1, 2, 0), (-1, 0, 0), (-1, -2, 0)])
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        t3 = mc.curve(d=2, p=[(0, 2, 1), (0, 0, 1), (0, -2, 1)])
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        t4 = mc.curve(d=2, p=[(0, 2, -1), (0, 0, -1), (0, -2, -1)])
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        t5 = mc.circle(nr=[0, 1, 0])
        mc.move(0, 2, 0)
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        t6 = mc.circle(nr=[0, 1, 0], n='tube_01')
        mc.move(0, -2, 0)
        # parenting the curves
        mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        rc2 = mc.listRelatives(t1, shapes=True)
        mc.parent(rc2[0], t6, r=True, shape=True)
        rc3 = mc.listRelatives(t2, shapes=True)
        mc.parent(rc3[0], t6, r=True, shape=True)
        rc2 = mc.listRelatives(t3, shapes=True)
        mc.parent(rc2[0], t6, r=True, shape=True)
        rc3 = mc.listRelatives(t4, shapes=True)
        mc.parent(rc3[0], t6, r=True, shape=True)
        rc2 = mc.listRelatives(t5, shapes=True)
        mc.parent(rc2[0], t6, r=True, shape=True)
        # deleting leftover groups
        mc.delete(constructionHistory=True)
        mc.delete(t1)
        mc.delete(t2)
        mc.delete(t3)
        mc.delete(t4)
        mc.delete(t5[0])
        # centering the pivot
        mc.xform('tube_01', cp=True)
        mc.pickWalk(d='up')
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            # creating the curves
            t1 = mc.curve(d=2, p=[(1, 2, 0), (1, 0, 0), (1, -2, 0)])
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, 
                            pn=True)
            t2 = mc.curve(d=2, p=[(-1, 2, 0), (-1, 0, 0), (-1, -2, 0)])
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, 
                            pn=True)
            t3 = mc.curve(d=2, p=[(0, 2, 1), (0, 0, 1), (0, -2, 1)])
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, 
                            pn=True)
            t4 = mc.curve(d=2, p=[(0, 2, -1), (0, 0, -1), (0, -2, -1)])
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, 
                            pn=True)
            t5 = mc.circle(nr=[0, 1, 0])
            mc.move(0, 2, 0)
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, 
                            pn=True)
            t6 = mc.circle(nr=[0, 1, 0], n='tube_01')
            mc.move(0, -2, 0)
            # parenting the curves
            mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, 
                            pn=True)
            rc2 = mc.listRelatives(t1, shapes=True)
            mc.parent(rc2[0], t6, r=True, shape=True)
            rc3 = mc.listRelatives(t2, shapes=True)
            mc.parent(rc3[0], t6, r=True, shape=True)
            rc2 = mc.listRelatives(t3, shapes=True)
            mc.parent(rc2[0], t6, r=True, shape=True)
            rc3 = mc.listRelatives(t4, shapes=True)
            mc.parent(rc3[0], t6, r=True, shape=True)
            rc2 = mc.listRelatives(t5, shapes=True)
            mc.parent(rc2[0], t6, r=True, shape=True)
            # deleting leftover groups
            mc.delete(constructionHistory=True)
            mc.delete(t1)
            mc.delete(t2)
            mc.delete(t3)
            mc.delete(t4)
            mc.delete(t5[0])
            # centering the pivot
            mc.xform(t6, cp=True)
            mc.pickWalk(d='up')
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def half_dome(*arg):
    selection_list = mc.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        mc.circle(nr=[0, 1, 0], n='half_dome_01')
        mc.move(0, 0, 0.783612, '.cv[0]', r=True, os=True, wd=True)
        mc.move(0, 0, 1.108194, '.cv[1]', r=True, os=True, wd=True)
        mc.move(0, 0, 0.783612, '.cv[2]', r=True, os=True, wd=True)
        mc.delete(constructionHistory=True)
        curve_selection_list = mc.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            mc.circle(nr=[0, 1, 0], n='half_dome_01')
            mc.move(0, 0, 0.783612, '.cv[0]', r=True, os=True, wd=True)
            mc.move(0, 0, 1.108194, '.cv[1]', r=True, os=True, wd=True)
            mc.move(0, 0, 0.783612, '.cv[2]', r=True, os=True, wd=True)
            mc.delete(constructionHistory=True)
            curve_selection_list = mc.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number, 
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)

# Color Functions #


def red(*arg):
    sel = mc.ls(sl=True)
    for col in sel:
        mc.setAttr((col + '.overrideEnabled'), 1)
        mc.setAttr((col + '.overrideRGBColors'), 1)
        mc.setAttr((col + ".overrideColorR"), 1)
        mc.setAttr((col + ".overrideColorG"), 0)
        mc.setAttr((col + ".overrideColorB"), 0)


def blue(*arg):
    sel = mc.ls(sl=True)
    for col in sel:
        mc.setAttr((col + '.overrideEnabled'), 1)
        mc.setAttr((col + '.overrideRGBColors'), 1)
        mc.setAttr((col + ".overrideColorR"), 0)
        mc.setAttr((col + ".overrideColorG"), 0)
        mc.setAttr((col + ".overrideColorB"), 1)


def yellow(*arg):
    sel = mc.ls(sl=True)
    for col in sel:
        mc.setAttr((col + '.overrideEnabled'), 1)
        mc.setAttr((col + '.overrideRGBColors'), 1)
        mc.setAttr((col + ".overrideColorR"), 1)
        mc.setAttr((col + ".overrideColorG"), 1)
        mc.setAttr((col + ".overrideColorB"), 0)


def pink(*arg):
    sel = mc.ls(sl=True)
    for col in sel:
        mc.setAttr((col + '.overrideEnabled'), 1)
        mc.setAttr((col + '.overrideRGBColors'), 1)
        mc.setAttr((col + ".overrideColorR"), 1)
        mc.setAttr((col + ".overrideColorG"), .5)
        mc.setAttr((col + ".overrideColorB"), .5)


def cyan(*arg):
    sel = mc.ls(sl=True)
    for col in sel:
        mc.setAttr((col + '.overrideEnabled'), 1)
        mc.setAttr((col + '.overrideRGBColors'), 1)
        mc.setAttr((col + ".overrideColorR"), 0)
        mc.setAttr((col + ".overrideColorG"), 1)
        mc.setAttr((col + ".overrideColorB"), 1)


def orange(*arg):
    sel = mc.ls(sl=True)
    for col in sel:
        mc.setAttr((col + '.overrideEnabled'), 1)
        mc.setAttr((col + '.overrideRGBColors'), 1)
        mc.setAttr((col + ".overrideColorR"), 1)
        mc.setAttr((col + ".overrideColorG"), .5)
        mc.setAttr((col + ".overrideColorB"), 0)


def gray(*arg):
    sel = mc.ls(sl=True)
    for col in sel:
        mc.setAttr((col + '.overrideEnabled'), 1)
        mc.setAttr((col + '.overrideRGBColors'), 1)
        mc.setAttr((col + ".overrideColorR"), .5)
        mc.setAttr((col + ".overrideColorG"), .5)
        mc.setAttr((col + ".overrideColorB"), .5)


def white(*arg):
    sel = mc.ls(sl=True)
    for col in sel:
        mc.setAttr((col + '.overrideEnabled'), 1)
        mc.setAttr((col + '.overrideRGBColors'), 1)
        mc.setAttr((col + ".overrideColorR"), 1)
        mc.setAttr((col + ".overrideColorG"), 1)
        mc.setAttr((col + ".overrideColorB"), 1)


def magenta(*arg):
    sel = mc.ls(sl=True)
    for col in sel:
        mc.setAttr((col + '.overrideEnabled'), 1)
        mc.setAttr((col + '.overrideRGBColors'), 1)
        mc.setAttr((col + ".overrideColorR"), 1)
        mc.setAttr((col + ".overrideColorG"), 0)
        mc.setAttr((col + ".overrideColorB"), 1)


def other_color(*arg):
    sel = mc.ls(sl=True)
    mc.colorEditor()
    if mc.colorEditor(query=True, result=True):
        color_editor = mc.colorEditor(query=True, rgb=True)
        print 'Custom Color Value: ' + str(color_editor)
        for col in sel:
            mc.setAttr((col + '.overrideEnabled'), 1)
            mc.setAttr((col + '.overrideRGBColors'), 1)
            mc.setAttr((col + ".overrideColorR"), color_editor[0])
            mc.setAttr((col + ".overrideColorG"), color_editor[1])
            mc.setAttr((col + ".overrideColorB"), color_editor[2])


def hand_attr(*arg):
    # adding attributes
    mc.addAttr(ci=True, sn='IKFK', ln='IKFK', min=0, max=1, at='double', 
               defaultValue=1)
    mc.addAttr(ci=True, ln='bendy',  at='double',  min=0, max=1, dv=0)
    mc.addAttr(ci=True, sn='_', ln='_', min=0, max=0, en='Masters', at='enum')
    mc.addAttr(ci=True, sn='spread', ln='spread', min=-10, max=10, at='double')
    mc.addAttr(ci=True, sn='masterRot', ln='masterRotation', at='double')
    mc.addAttr(ci=True, sn='offset', ln='offset', at='double')
    mc.addAttr(ci=True, sn='offsetFavor', ln='offsetFavor', min=0, max=1, 
               en='Pinky:Index', at='enum')
    mc.addAttr(ci=True, sn='__', ln='__', min=0, max=0, en='Index', at='enum')
    mc.addAttr(ci=True, sn='indexBase', ln='indexBase', at='double')
    mc.addAttr(ci=True, sn='indexMid', ln='indexMid', at='double')
    mc.addAttr(ci=True, sn='indexEnd', ln='indexEnd', at='double')
    mc.addAttr(ci=True, sn='___', ln='___', min=0, max=0, en='Middle', 
               at='enum')
    mc.addAttr(ci=True, sn='middleBase', ln='middleBase', at='double')
    mc.addAttr(ci=True, sn='middleMid', ln='middleMid', at='double')
    mc.addAttr(ci=True, sn='middleEnd', ln='middleEnd', at='double')
    mc.addAttr(ci=True, sn='____', ln='____', min=0, max=0, en='Ring', 
               at='enum')
    mc.addAttr(ci=True, sn='ringBase', ln='ringBase', at='double')
    mc.addAttr(ci=True, sn='ringMid', ln='ringMid', at='double')
    mc.addAttr(ci=True, sn='ringEnd', ln='ringEnd', at='double')
    mc.addAttr(ci=True, sn='_____', ln='_____', min=0, max=0, en='Pinky', 
               at='enum')
    mc.addAttr(ci=True, sn='pinkyBase', ln='pinkyBase', at='double')
    mc.addAttr(ci=True, sn='pinkyMid', ln='pinkyMid', at='double')
    mc.addAttr(ci=True, sn='pinkyEnd', ln='pinkyEnd', at='double')
    mc.addAttr(ci=True, sn='______', ln='______', min=0, max=0, en='Thumb', 
               at='enum')
    mc.addAttr(ci=True, sn='thumbMid', ln='thumbMid', at='double')
    mc.addAttr(ci=True, sn='thumbEnd', ln='thumbEnd', at='double')
    mc.addAttr(ci=True, sn='_______', ln='_______', min=0, max=0, en='Vis', 
               at='enum')
    mc.addAttr(ci=True, sn='masterVis', ln='masterVis', min=0, max=1, at='long', 
               defaultValue=1)
    mc.addAttr(ci=True, sn='thumbVis', ln='thumbVis', min=0, max=1, at='long', 
               defaultValue=1)
    mc.addAttr(ci=True, sn='indexVis', ln='indexVis', min=0, max=1, at='long', 
               defaultValue=1)
    mc.addAttr(ci=True, sn='middleVis', ln='middleVis', min=0, max=1, at='long', 
               defaultValue=1)
    mc.addAttr(ci=True, sn='pinkyVis', ln='pinkyVis', min=0, max=1, at='long', 
               defaultValue=1)
    # setting keyability
    mc.setAttr('.IKFK', keyable=True)
    mc.setAttr('.bendy', keyable=True)
    mc.setAttr('._', channelBox=True)
    mc.setAttr('.spread', keyable=True)
    mc.setAttr('.masterRot', keyable=True)
    mc.setAttr('.offset', keyable=True)
    mc.setAttr('.offsetFavor', keyable=True)
    mc.setAttr('.__', channelBox=True)
    mc.setAttr('.indexBase', keyable=True)
    mc.setAttr('.indexMid', keyable=True)
    mc.setAttr('.indexEnd', keyable=True)
    mc.setAttr('.___', channelBox=True)
    mc.setAttr('.middleBase', keyable=True)
    mc.setAttr('.middleMid', keyable=True)
    mc.setAttr('.middleEnd', keyable=True)
    mc.setAttr('.____', channelBox=True)
    mc.setAttr('.ringBase', keyable=True)
    mc.setAttr('.ringMid', keyable=True)
    mc.setAttr('.ringEnd', keyable=True)
    mc.setAttr('._____', channelBox=True)
    mc.setAttr('.pinkyBase', keyable=True)
    mc.setAttr('.pinkyMid', keyable=True)
    mc.setAttr('.pinkyEnd', keyable=True)
    mc.setAttr('.______', channelBox=True)
    mc.setAttr('.thumbMid', keyable=True)
    mc.setAttr('.thumbEnd', keyable=True)
    mc.setAttr('._______', channelBox=True)
    mc.setAttr('.masterVis', keyable=True)
    mc.setAttr('.thumbVis', keyable=True)
    mc.setAttr('.indexVis', keyable=True)
    mc.setAttr('.middleVis', keyable=True)
    mc.setAttr('.pinkyVis', keyable=True)
    # lock and hide unnecessary attributes
    for attr in attributes:
        mc.setAttr(attr, lock=True, keyable=False)


def reverse_foot_attr(*arg):
    # adding attributes
    mc.addAttr(ci=True, sn='_', ln='_', min=0, max=0, en='Controls', at='enum')
    mc.addAttr(ci=True, ln='ballRoll',  at='double',  dv=0)
    mc.addAttr(ci=True, ln='footBank',  at='double',  dv=0)
    mc.addAttr(ci=True, ln='toeBend',  at='double',  dv=0)
    mc.addAttr(ci=True, ln='toePivot',  at='double',  dv=0)
    mc.addAttr(ci=True, ln='toeRoll',  at='double',  dv=0)
    mc.addAttr(ci=True, ln='heelPivot',  at='double',  dv=0)
    mc.addAttr(ci=True, ln='heelRoll',  at='double',  dv=0)
    mc.addAttr(ci=True, sn='stretch', ln='stretch', min=0, max=1, at='long', 
               defaultValue=0)
    mc.addAttr(ci=True, ln='bendy',  at='double',  min=0, max=1, dv=0)
    # setting keyability
    mc.setAttr('._', channelBox=True)
    mc.setAttr('.ballRoll', keyable=True)
    mc.setAttr('.footBank', keyable=True)
    mc.setAttr('.toeBend', keyable=True)
    mc.setAttr('.toePivot', keyable=True)
    mc.setAttr('.toeRoll', keyable=True)
    mc.setAttr('.heelPivot', keyable=True)
    mc.setAttr('.heelRoll', keyable=True)
    mc.setAttr('.stretch', keyable=True)
    mc.setAttr('.bendy', keyable=True)
    # lock and hide unnecessary attributes
    mc.setAttr('.sx', lock=True, keyable=False)
    mc.setAttr('.sy', lock=True, keyable=False)
    mc.setAttr('.sz', lock=True, keyable=False)
    mc.setAttr('.v', lock=True, keyable=False)


def foot_switch(*arg):
    # adding attributes
    mc.addAttr(ci=True, sn='IKFK', ln='IKFK', min=0, max=1, at='double', 
               defaultValue=1)
    mc.addAttr(ci=True, sn='toeControls', ln='toeControls', min=0, max=1,
               at='long', dv=1)
    # setting keyability
    mc.setAttr('.IKFK', keyable=True)
    mc.setAttr('.toeControls', channelBox=True)
    # lock and hide unnecessary attributes
    for attr in attributes:
        mc.setAttr(attr, lock=True, keyable=False)


def sync_phoneme_attr(*arg):
    # adding attributes
    mc.addAttr(ci=True, sn='_', ln='_', min=0, max=1, en='Sync', at='enum')
    mc.addAttr(ci=True, sn='__', ln='__', min=0, max=0, en='Open', at='enum')
    mc.addAttr(ci=True, sn='A', ln='A', min=0, max=1, at='double')
    mc.addAttr(ci=True, sn='E', ln='E', min=0, max=1, at='double')
    mc.addAttr(ci=True, sn='I', ln='I', min=0, max=1, at='double')
    mc.addAttr(ci=True, sn='O_H', ln='O_H', min=0, max=1, at='double')
    mc.addAttr(ci=True, sn='U_W', ln='U_W', min=0, max=1, at='double')
    mc.addAttr(ci=True, sn='L', ln='L', min=0, max=1, at='double')
    mc.addAttr(ci=True, sn='S_D_G_e_General', ln='S_D_G_e_General', min=0, 
               max=1, at='double')
    mc.addAttr(ci=True, sn='___', ln='___', min=0, max=0, en='Closed', 
               at='enum')
    mc.addAttr(ci=True, sn='F_V', ln='F_V', min=0, max=1, at='double')
    mc.addAttr(ci=True, sn='M_P_B', ln='M_P_B', min=0, max=1, at='double')
    mc.addAttr(ci=True, sn='____', ln='____', min=0, max=0, en='Tongue', 
               at='enum')
    mc.addAttr(ci=True, sn='upDown', ln='upDown', min=-2, max=10, at='double')
    mc.addAttr(ci=True, sn='leftRight', ln='leftRight', min=-5, max=5, 
               at='double')
    # setting keyability
    mc.setAttr('._', channelBox=True)
    mc.setAttr('.__', channelBox=True)
    mc.setAttr('.A', keyable=True)
    mc.setAttr('.E', keyable=True)
    mc.setAttr('.I', keyable=True)
    mc.setAttr('.O_H', keyable=True)
    mc.setAttr('.U_W', keyable=True)
    mc.setAttr('.L', keyable=True)
    mc.setAttr('.S_D_G_e_General', keyable=True)
    mc.setAttr('.___', channelBox=True)
    mc.setAttr('.F_V', keyable=True)
    mc.setAttr('.M_P_B', keyable=True)
    mc.setAttr('.____', channelBox=True)
    mc.setAttr('.upDown', keyable=True)
    mc.setAttr('.leftRight', keyable=True)
    # lock and hide unnecessary attributes
    for attr in attributes:
        mc.setAttr(attr, lock=True, keyable=False)


def world_space(*arg):
    # check if a Space enum separator already exists, add if false
    attribute_selection = mc.ls(sl=True)
    q = mc.attributeQuery('_________', node=attribute_selection[0], exists=True)
    if q is False:
        mc.addAttr(ci=True, sn='_________', ln='_________', min=0, max=1, 
                   en='Spaces', at='enum')
        mc.setAttr('._________', cb=True)
    # add the new attribute
    mc.addAttr(ci=True, sn='world', ln='world', min=0, max=1, at='double')
    mc.setAttr('.world', k=True)


def head_space(*arg):
    # check if a Space enum separator already exists, add if false
    attribute_selection = mc.ls(sl=True)
    q = mc.attributeQuery('_________', node=attribute_selection[0], exists=True)
    if q is False:
        mc.addAttr(ci=True, sn='_________', ln='_________', min=0, max=1,
                   en='Spaces', at='enum')
        mc.setAttr('._________', cb=True)
    # add the new attribute
    mc.addAttr(ci=True, sn='head', ln='head', min=0, max=1, at='double')
    mc.setAttr('.head', k=True)


def hand_space(*arg):
    # check if a Space enum separator already exists, add if false
    attribute_selection = mc.ls(sl=True)
    q = mc.attributeQuery('_________', node=attribute_selection[0], exists=True)
    if q is False:
        mc.addAttr(ci=True, sn='_________', ln='_________', min=0, max=1,
                   en='Spaces', at='enum')
        mc.setAttr('._________', cb=True)
        # add the new attribute
    mc.addAttr(ci=True, sn='hand', ln='hand', min=0, max=1, at='double')
    mc.setAttr('.hand', k=True)


def foot_space(*arg):
    # check if a Space enum separator already exists, add if false
    attribute_selection = mc.ls(sl=True)
    q = mc.attributeQuery('_________', node=attribute_selection[0], exists=True)
    if q is False:
        mc.addAttr(ci=True, sn='_________', ln='_________', min=0, max=1,
                   en='Spaces', at='enum')
        mc.setAttr('._________', cb=True)
    # add the new attribute
    mc.addAttr(ci=True, sn='foot', ln='foot', min=0, max=1, at='double')
    mc.setAttr('.foot', k=True)


def cog_space(*arg):
    # check if a Space enum separator already exists, add if false
    attribute_selection = mc.ls(sl=True)
    q = mc.attributeQuery('_________', node=attribute_selection[0], exists=True)
    if q is False:
        mc.addAttr(ci=True, sn='_________', ln='_________', min=0, max=1,
                   en='Spaces', at='enum')
        mc.setAttr('._________', cb=True)
    # add the new attribute
    mc.addAttr(ci=True, sn='Cother_group_value', ln='Cother_group_value', min=0, 
               max=1, at='double')
    mc.setAttr('.Cother_group_value', k=True)


def about_window(*arg):
    window_name = 'aboutWin'
    window_title = 'About Rigging Control Curves'
    # check if window exists
    if mc.window(window_name, exists=True):
        mc.deleteUI(window_name, window=True)
    # setup window
    mc.window(window_name, title=window_title, sizeable=True)
    mc.scrollLayout()
    mc.columnLayout(adjustableColumn=True)

    mc.text(label=aboutText, al='left')
    mc.showWindow(window_name)
    mc.window(window_name, edit=True, width=425, height=400)


def naming_enable(*arg):
    name_box_value = mc.checkBox('overrideName', q=True, v=True)
    if name_box_value is False:
        mc.textField('CurvePrefix', e=True, en=1)
        mc.textField('CurveName', e=True, en=1)
        mc.textField('CurveSuffix', e=True, en=1)
    if name_box_value is True:
        mc.textField('CurvePrefix', e=True, en=0)
        mc.textField('CurveName', e=True, en=0)
        mc.textField('CurveSuffix', e=True, en=0)


def grp_enable(*arg):
    grp_box_value = mc.checkBox('otherBox', q=True, v=True)
    mc.textField('otherGrp', e=True, en=grp_box_value)


def lock_attr(*arg):
    selection_list = mc.ls(sl=True)

    for attr in attributes:
        if mc.checkBox(attr.replace('.', '').upper(), q=True, v=True) is True:
            mc.setAttr(selection_list[0] + attr, lock=True)


def unlock_attr(*arg):
    selection_list = mc.ls(sl=True)

    for attr in attributes:
        if mc.checkBox(attr.replace('.', '').upper(), q=True, v=True) is True:
            mc.setAttr(selection_list[0] + attr, lock=False)


def hide_attr(*arg):
    selection_list = mc.ls(sl=True)

    for attr in attributes:
        if mc.checkBox(attr.replace('.', '').upper(), q=True, v=True) is True:
            mc.setAttr(selection_list[0] + attr, keyable=False, 
                       channelBox=False)


def show_attr(*arg):
    selection_list = mc.ls(sl=True)

    for attr in attributes:
        if mc.checkBox(attr.replace('.', '').upper(), q=True, v=True) is True:
            mc.setAttr(selection_list[0] + attr, keyable=True)


def lock_hide_attr(*arg):
    lock_attr()
    hide_attr()


def unlock_show_attr(*arg):
    unlock_attr()
    show_attr()


def change_attr_box(*arg):
    translation = mc.checkBox('allT', q=True, v=True)
    rotation = mc.checkBox('allR', q=True, v=True)
    scaling = mc.checkBox('allS', q=True, v=True)
    all = mc.checkBox('allBox', q=True, v=True)

    mc.checkBox('TX', e=True, v=translation)
    mc.checkBox('TY', e=True, v=translation)
    mc.checkBox('TZ', e=True, v=translation)

    mc.checkBox('RX', e=True, v=rotation)
    mc.checkBox('RY', e=True, v=rotation)
    mc.checkBox('RZ', e=True, v=rotation)

    mc.checkBox('SX', e=True, v=scaling)
    mc.checkBox('SY', e=True, v=scaling)
    mc.checkBox('SZ', e=True, v=scaling)


def check_all(*arg):
    all = mc.checkBox('allBox', q=True, v=True)

    mc.checkBox('allT', e=True, v=all)
    mc.checkBox('allR', e=True, v=all)
    mc.checkBox('allS', e=True, v=all)
    mc.checkBox('V', e=True, v=all)
    change_attr_box()


# The Actual Window #


def nick_curves_mill():
    # assign window names
    window_name = 'crvWin'
    window_title = 'Rigging Control Curves'
    # check if window exists
    if mc.window(window_name, exists=True):
        mc.deleteUI(window_name, window=True)
    # setup window
    mc.window(window_name, title=window_title, sizeable=True)
    mc.columnLayout(adjustableColumn=True)
    # menuBar
    mc.menuBarLayout()
    mc.menu(label='File')
    mc.menuItem(label='Test')
    mc.menu(label='Help', helpMenu=True)
    mc.menuItem(label='About...', c=about_window)
    #
    mc.columnLayout(adjustableColumn=True)
    # Naming Layout
    mc.frameLayout(label='Naming Conventions', mw=4, mh=4,
                   bgc=[0.18, 0.21, 0.25])
    mc.rowColumnLayout(numberOfColumns=3, 
                       columnWidth=[(1, 100), (2, 150), (3, 100)])
    mc.text('Prefix')
    mc.text('Name')
    mc.text('Suffix')
    mc.textField('CurvePrefix')
    mc.textField('CurveName')
    mc.textField('CurveSuffix')
    mc.checkBox('overrideName', label='Override Name', cc=naming_enable)
    mc.setParent('..')
    mc.setParent('..')
    # Group Layout
    mc.frameLayout(label='Grouping', mw=4, mh=4, bgc=[0.18, 0.21, 0.25])
    mc.rowColumnLayout(numberOfColumns=3, 
                       columnWidth=[(1, 115), (2, 115), (3, 115)])
    mc.checkBox('zeroBox', label='ZERO')
    mc.checkBox('srtBox', label='SRT')
    mc.checkBox('sdkBox', label='SDK')
    mc.checkBox('spaceBox', label='SPACE')
    mc.checkBox('ofsBox', label='OFS')
    mc.checkBox('dummyBox', label='DUMMY')
    mc.checkBox('otherBox', label='Other', cc=grp_enable)
    mc.textField('otherGrp', w=200, en=False)
    mc.setParent('..')
    mc.setParent('..')
    # Curves Layout
    mc.frameLayout(label='Curves', mw=4, mh=4, bgc=[0.18, 0.21, 0.25])
    mc.rowColumnLayout(numberOfColumns=4,
                       columnWidth=[(1, 85), (2, 85), (3, 85), (4, 85)])
    mc.button(label='Circle', command=cir)
    mc.button(label='Square', command=square)
    mc.button(label='Triangle', command=triangle)
    mc.button(label='Octagon', command=octagon)
    mc.button(label='Sphere', command=sphere)
    mc.button(label='Box', command=box)
    mc.button(label='Pyramid', command=pyramid)
    mc.button(label='Diamond', command=diamond)
    mc.button(label='Quad Arrow', command=quad_arrow)
    mc.button(label='Curved Plane', command=curved_plane)
    mc.button(label='Icosah', command=icosah)
    mc.button(label='Lever', command=lever)
    mc.button(label='Arrow', command=arrow)
    mc.button(label='Palm', command=palm)
    mc.button(label='Plus', command=plus)
    mc.button(label='Locator', command=loc)
    mc.button(label='Trap Cube', command=trapezoid_cube)
    mc.button(label='Ring', command=ring)
    mc.button(label='Tube', command=tube)
    mc.button(label='Half Dome', command=half_dome)
    mc.setParent('..')
    mc.setParent('..')
    # Color Options
    mc.frameLayout(label='Colors', mw=4, mh=4, bgc=[0.18, 0.21, 0.25])
    mc.rowColumnLayout(numberOfColumns=3,
                       columnWidth=[(1, 100), (2, 150), (3, 100)])
    mc.button(command=red, label='', bgc=[1, 0, 0])
    mc.button(command=yellow, label='', bgc=[1, 1, 0])
    mc.button(command=blue, label='', bgc=[0, 0, 1])
    mc.button(command=pink, label='', bgc=[1, .5, .5])
    mc.button(command=orange, label='', bgc=[1, .5, 0])
    mc.button(command=cyan, label='', bgc=[0, 1, 1])
    mc.button(command=gray, label='', bgc=[.5, .5, .5])
    mc.button(command=white, label='', bgc=[1, 1, 1])
    mc.button(command=magenta, label='', bgc=[1, 0, 1])
    mc.setParent('..')
    mc.columnLayout(columnAlign='center')
    mc.button(command=other_color, label='Choose Custom Color', w=350, h=30)
    mc.setParent('..')
    mc.setParent('..')

    # Lock/Unlock/Hide Attribute Options
    mc.frameLayout(label='Lock & Hide Attributes', mw=4, mh=4, 
                   bgc=[0.18, 0.21, 0.25])
    mc.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 150), (2, 200)])
    mc.rowColumnLayout(numberOfColumns=5, columnWidth=[(1, 50), (2, 25), 
                       (3, 25), (4, 25), (5, 25)], columnAlign=[(1, 'right'), 
                       (2, 'left'), (3, 'left'), (4, 'left'), (5, 'left')])
    mc.text('space1', label='')
    mc.text('X')
    mc.text('Y')
    mc.text('Z')
    mc.text('All')
    mc.separator()
    mc.separator()
    mc.separator()
    mc.separator()
    mc.separator()
    mc.text('T  ')
    mc.checkBox('TX', label='')
    mc.checkBox('TY', label='')
    mc.checkBox('TZ', label='')
    mc.checkBox('allT', label='', cc=change_attr_box)
    mc.separator()
    mc.separator()
    mc.separator()
    mc.separator()
    mc.separator()
    mc.text('R  ')
    mc.checkBox('RX', label='')
    mc.checkBox('RY', label='')
    mc.checkBox('RZ', label='')
    mc.checkBox('allR', label='', cc=change_attr_box)
    mc.separator()
    mc.separator()
    mc.separator()
    mc.separator()
    mc.separator()
    mc.text('S  ')
    mc.checkBox('SX', label='')
    mc.checkBox('SY', label='')
    mc.checkBox('SZ', label='')
    mc.checkBox('allS', label='', cc=change_attr_box)
    mc.separator()
    mc.separator()
    mc.separator()
    mc.separator()
    mc.separator()
    mc.text('Visibility  ')
    mc.checkBox('V', label='')
    mc.text('space2', label='')
    mc.text('space3', label='')
    mc.checkBox('allBox', label='', cc=check_all)
    mc.setParent('..')
    mc.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 100), (2, 100)])
    mc.columnLayout()
    mc.button(label='Lock', c=lock_attr, w=100)
    mc.button(label='Unlock', c=unlock_attr, w=100)
    mc.button(label='Hide', c=hide_attr, w=100)
    mc.button(label='Show', c=show_attr, w=100)
    mc.setParent('..')
    mc.columnLayout()
    mc.button(label='Lock and Hide', c=lock_hide_attr, w=100, h=45)
    mc.button(label='Unlock and Show', c=unlock_show_attr, w=100, h=45)
    mc.setParent('..')
    mc.setParent('..')
    mc.setParent('..')
    mc.setParent('..')
    # Attribute Options  ## Needs updating
    mc.frameLayout(label='Attribute Presets', cll=True, cl=True, mw=4, mh=4, 
                   bgc=[0.18, 0.21, 0.25])
    mc.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 175), (2, 175)])
    mc.button(label='Hand Attributes', command=hand_attr)
    mc.button(label='IK Reverse Foot', command=reverse_foot_attr)
    mc.button(label='Foot Switch', command=foot_switch)
    mc.button(label='Sync Phonemes', command=sync_phoneme_attr)
    mc.button(label='World Space', command=world_space)
    mc.button(label='Head Space', command=head_space)
    mc.button(label='Hand Space', command=hand_space)
    mc.button(label='Foot Space', command=foot_space)
    mc.button(label='Cother_group_value Space', command=cog_space)
    mc.setParent('..')
    mc.setParent('..')

    mc.showWindow(window_name)
    mc.window(window_name, edit=True, width=200, height=210)


nick_curves_mill()
