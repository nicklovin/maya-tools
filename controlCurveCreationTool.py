import maya.cmds as cmds

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


def set_curve_name(input_object, override_value, input_prefix,
                   input_name, input_suffix, padding, *args):
    """

    Args:
        input_object (list[str]): List of objects or single object input for the
            function to rename.  If list, function will run procedure for each
            item.  If no input given, input defaults to selection.
        override_value(int/bool): Value of the override name checkbox.  Used to
            ignore input parameters and create new names based on the
            input_object.
        input_prefix (str): Assign a prefix for the new object(s).
        input_name (str): Assign a base name for the new object(s).
        input_suffix (str): Assign a suffix for the new object(s).
        padding (int): String padding for the renaming if a list is provided and
            override_value is 1/True.
        *args:

    Returns:
        One of the following:
            new_name (str): New object name as a string
            name_list (list[str]): List of all the new object names.

    """

    # Check for input_object
    if not input_object:
        input_object = cmds.ls(selection=True)

    # If no input or selection, return with warning
    if not input_object:
        cmds.warning('No input given for naming function!  Add input or '
                     'selection.')
        return

    # If input is iterable (list), loop procedure to affect all input objects
    if input_object is list:  # if not correct, do isIterable
        name_list = []
        i = 1
        if override_value == 1:
            for obj in input_object:
                index = str(i).zfill(padding)
                kill_length = obj.rfind('_')
                new_name = cmds.rename(obj,
                                       obj.replace(obj[kill_length:],
                                                   '_%s_CTRL' % index))
                name_list.append(new_name)
                i = i + 1
            return name_list

        for obj in input_object:
            new_name = ''
            index = str(i).zfill(padding)

            if input_prefix:
                new_name += '%s_' % input_prefix

            if input_name:
                new_name += '%s_%s' % (input_name, index)
            else:
                new_name += '%s_%s' % (obj, index)

            if input_suffix:
                new_name += '_%s' % input_suffix

            cmds.rename(obj, new_name)

            name_list.append(new_name)
            i = i + 1

        return name_list

    # If input is not iterable (str), run procedure once
    else:
        if override_value == 1:
            kill_length = input_object.rfind('_')
            new_name = cmds.rename(input_object,
                                   input_object.replace(input_object[kill_length:], '_CTRL'))
            return new_name

        new_name = ''

        if input_prefix:
            new_name += '%s_' % input_prefix

        if input_name:
            new_name += input_name
        else:
            new_name += input_object

        if input_suffix:
            new_name += '_%s' % input_suffix

        cmds.rename(input_object, new_name)

        return new_name

# Clean Rename above, old reference below


def curve_rename(input_object, selection_list, iteration, selection_name):

    curve_prefix = cmds.textField('CurvePrefix', query=True, text=True)
    curve_name = cmds.textField('CurveName', query=True, text=True)
    curve_suffix = cmds.textField('CurveSuffix', query=True, text=True)
    override_value = cmds.checkBox('overrideName', query=True, value=True)

    length_prefix = len(curve_prefix)
    length_name = len(curve_name)
    length_suffix = len(curve_suffix)
    length_selection = len(selection_list)
    a = iteration + 1
    length_string = str(a).zfill(2)

    if override_value == 1:
        kill_length = selection_name.rfind('_')
        cmds.rename(input_object,
                  selection_name.replace(selection_name[kill_length:], '_CTRL'))

    elif override_value == 0:
        if length_selection > 1:
            if length_prefix > 0 and length_name > 0 and length_suffix > 0:
                cmds.rename(input_object, (curve_prefix + '_' + curve_name + '_'
                                         + length_string + '_' + curve_suffix))
            elif length_prefix == 0 and length_name > 0 and length_suffix > 0:
                cmds.rename(input_object, (curve_name + '_' + length_string + '_'
                                         + curve_suffix))
            elif length_prefix > 0 and length_name > 0 and length_suffix == 0:
                cmds.rename(input_object, (curve_prefix + '_' + curve_name + '_' +
                                         length_string))
            elif length_prefix > 0 and length_name == 0 and length_suffix > 0:
                cmds.rename(input_object, (curve_prefix + '_' + input_object + '_'
                                         + length_string + '_' + curve_suffix))
            elif length_prefix == 0 and length_name > 0 and length_suffix == 0:
                cmds.rename(input_object, curve_name + '_' + length_string)
            elif length_prefix > 0 and length_name == 0 and length_suffix == 0:
                cmds.rename(input_object, (curve_prefix + '_' + input_object[0] +
                                         '_' + length_string))
            elif length_prefix == 0 and length_name == 0 and length_suffix > 0:
                cmds.rename(input_object, (input_object[0] + '_' + length_string
                                         + '_' + curve_suffix))
            else:
                print input_object
        elif length_selection < 2:
            if length_prefix > 0 and length_name > 0 and length_suffix > 0:
                cmds.rename(input_object, (curve_prefix + '_' + curve_name + '_'
                                         + curve_suffix))
            elif length_prefix == 0 and length_name > 0 and length_suffix > 0:
                cmds.rename(input_object, (curve_name + '_' + curve_suffix))
            elif length_prefix > 0 and length_name > 0 and length_suffix == 0:
                cmds.rename(input_object, (curve_prefix + '_' + curve_name))
            elif length_prefix > 0 and length_name == 0 and length_suffix > 0:
                cmds.rename(input_object, (curve_prefix + '_' + selection_name + '_'
                                         + curve_suffix))
            elif length_prefix == 0 and length_name > 0 and length_suffix == 0:
                cmds.rename(input_object, curve_name)
            elif length_prefix > 0 and length_name == 0 and length_suffix == 0:
                cmds.rename(input_object, (curve_prefix + '_' + input_object[0]))
            elif length_prefix == 0 and length_name == 0 and length_suffix > 0:
                cmds.rename(input_object, (input_object[0] + '_' + curve_suffix))
            else:
                print input_object

# Grouping Options #

# On GUI, make a buildable widget system that shows the group hierarchy properly
# and can be moved around to accommodate the order of groups.  If
# slide-reordering is possible, do that.


def build_hierarchy(input_object, override_suffix, ):
    if not input_object:
        input_object = cmds.ls(selection=True)

    if not input_object:
        cmds.warning('No input provided for the hierarchy building procedure!  '
                     'Input a str, list, or select objects to be used as inputs')
        return

    # May need GUI rebuild in Qt to understand how to write group function...

    # return list of groups in descending order starting with parent


def grp(*arg):
    group_selection = cmds.ls(sl=True)

    zero = cmds.checkBox('zeroBox', query=True, value=True)
    srt = cmds.checkBox('srtBox', query=True, value=True)
    sdk = cmds.checkBox('sdkBox', query=True, value=True)
    space = cmds.checkBox('spaceBox', query=True, value=True)
    offset = cmds.checkBox('ofsBox', query=True, value=True)
    dummy = cmds.checkBox('dummyBox', query=True, value=True)
    other = cmds.checkBox('otherBox', query=True, value=True)
    other_group_value = cmds.textField('otherGrp', query=True, text=True)
    curve_suffix = cmds.textField('CurveSuffix', query=True, text=True)
    override_value = cmds.checkBox('overrideName', query=True, value=True)
    other_group_length = len(other_group_value)

    if override_value == 1:
        if srt is True:
            cmds.group(n=(group_selection[0].replace('CTRL', 'SRT')))
        if sdk is True:
            cmds.group(n=(group_selection[0].replace('CTRL', 'SDK')))
        if space is True:
            cmds.group(n=(group_selection[0].replace('CTRL', 'SPACE')))
        if dummy is True:
            cmds.group(n=(group_selection[0].replace('CTRL', 'DUMMY')))
        if other is True:
            if other_group_length == 0:
                cmds.group(n=(group_selection[0].replace('CTRL', 'NULL')))
            else:
                cmds.group(n=(group_selection[0].replace('CTRL',
                         other_group_value)))
        if offset is True:
            cmds.group(n=(group_selection[0].replace('CTRL', 'OFS')))
        if zero is True:
            cmds.group(n=(group_selection[0].replace('CTRL', 'ZERO')))
    elif override_value == 0:
        if srt is True:
            cmds.group(n=(group_selection[0] + '_SRT'))
        if sdk is True:
            cmds.group(n=(group_selection[0] + '_SDK'))
        if space is True:
            cmds.group(n=(group_selection[0] + '_SPACE'))
        if dummy is True:
            cmds.group(n=(group_selection[0] + '_DUMMY'))
        if other is True:
            if other_group_length == 0:
                cmds.group(n=(group_selection[0] + '_NULL'))
            else:
                cmds.group(n=(group_selection[0] + other_group_value))
        if offset is True:
            cmds.group(n=(group_selection[0] + '_OFS'))
        if zero is True:
            cmds.group(n=(group_selection[0] + '_ZERO'))

# Snap to Point #


def snap_to_selection(input_list, ):
    # input_list will have either hierarchy parents or single controls)
    selection = cmds.ls(selection=True)

    # run for each parent of inputs... might involve lists of lists



def snap_position(list, size):
    ctrl_selection = cmds.ls(sl=True)
    for s in range(size):
        temp_constraint = cmds.parentConstraint(list[s], ctrl_selection[0],
                                                mo=False, w=1)
        cmds.delete(temp_constraint)


# Curve Creations #


def cir(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        cmds.circle(nr=[0, 1, 0], n='circle_01')
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.circle(nr=[0, 1, 0], n='circle_01')
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def square(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        cmds.circle(nr=[0, 1, 0], degree=1, sections=4, n='square_01')
        cmds.rotate(0, 45, 0)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.circle(nr=[0, 1, 0], degree=1, sections=4, n='square_01')
            cmds.rotate(0, 45, 0)
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def triangle(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        cmds.circle(nr=[0, 1, 0], degree=1, sections=3, n='triangle_01')
        cmds.rotate(0, -90, 0)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.circle(nr=[0, 1, 0], degree=1, sections=3, n='triangle_01')
            cmds.rotate(0, -90, 0)
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def octagon(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        cmds.circle(nr=[0, 1, 0], degree=1, sections=8, n='octagon_01')
        cmds.rotate(0, 45, 0)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.circle(nr=[0, 1, 0], degree=1, sections=8, n='octagon_01')
            cmds.rotate(0, 45, 0)
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def sphere(*arg):

    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # Create curves
        c1 = cmds.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1, d=3, ut=0, ch=1,
                       n='sphere_01')
        c2 = cmds.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1, d=3, ut=0, ch=1)
        cmds.rotate(90, 0, 0)
        c3 = cmds.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1, d=3, ut=0, ch=1)
        cmds.rotate(0, 0, 90)
        # Freeze the rotated curves
        cmds.select(c2)
        cmds.select(c3, add=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        # Parent shapes of curves 2 and 3 to curve 1
        rc2 = cmds.listRelatives(c2, shapes=True)
        cmds.parent(rc2[0], c1, r=True, shape=True)
        rc3 = cmds.listRelatives(c3, shapes=True)
        cmds.parent(rc3[0], c1, r=True, shape=True)
        cmds.pickWalk(d='up')
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            # Create curves
            c1 = cmds.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1, d=3, ut=0,
                           ch=1, n='sphere_01')
            c2 = cmds.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1, d=3, ut=0,
                           ch=1)
            cmds.rotate(90, 0, 0)
            c3 = cmds.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1, d=3, ut=0,
                           ch=1)
            cmds.rotate(0, 0, 90)
            # Freeze the rotated curves
            cmds.select(c2)
            cmds.select(c3, add=True)
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            # Parent shapes of curves 2 and 3 to curve 1
            rc2 = cmds.listRelatives(c2, shapes=True)
            cmds.parent(rc2[0], c1, r=True, shape=True)
            rc3 = cmds.listRelatives(c3, shapes=True)
            cmds.parent(rc3[0], c1, r=True, shape=True)
            cmds.pickWalk(d='up')
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            cmds.delete(constructionHistory=True)

            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)

            # Delete the transform node of curves 2 and 3
            cmds.select(c2[0])
            cmds.select(c3[0], add=True)
            cmds.delete()


def box(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # box curve line
        cmds.curve(d=1, p=[(0.5, 0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5),
                         (0.5, 0.5, -0.5,), (0.5, 0.5, 0.5,), (0.5, -0.5, 0.5,),
                         (0.5, -0.5, -0.5,), (0.5, 0.5, -0.5,),
                         (-0.5, 0.5, -0.5,), (-0.5, -0.5, -0.5,),
                         (-0.5, -0.5, 0.5,), (-0.5, 0.5, 0.5,),
                         (-0.5, -0.5, 0.5,), (0.5, -0.5, 0.5,),
                         (0.5, -0.5, -0.5,), (-0.5, -0.5, -0.5,)], n='box_01')
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            # box curve line
            cmds.curve(d=1, p=[(0.5, 0.5, 0.5), (-0.5, 0.5, 0.5),
                             (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5,),
                             (0.5, 0.5, 0.5,), (0.5, -0.5, 0.5,),
                             (0.5, -0.5, -0.5,), (0.5, 0.5, -0.5,),
                             (-0.5, 0.5, -0.5,), (-0.5, -0.5, -0.5,),
                             (-0.5, -0.5, 0.5,), (-0.5, 0.5, 0.5,),
                             (-0.5, -0.5, 0.5,), (0.5, -0.5, 0.5,),
                             (0.5, -0.5, -0.5,), (-0.5, -0.5, -0.5,)],
                     n='box_01')
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def pyramid(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # pyramid curve line
        cmds.curve(d=1, p=[(9.27258e-008, -0.353553, -0.707107), (-0.707107,
                         -0.353553, -6.18172e-008), (0, 0.353553, 0),
                         (9.27258e-008, -0.353553, -0.707107), (0.707107,
                         -0.353553, 0), (0, 0.353553, 0), (-3.09086e-008,
                         -0.353553, 0.707107), (0.707107, -0.353553, 0),
                         (-3.09086e-008, -0.353553, 0.707107), (-0.707107,
                         -0.353553, -6.18172e-008)], n='pyramid_01')
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.curve(d=1, p=[(9.27258e-008, -0.353553, -0.707107), (-0.707107,
                             -0.353553, -6.18172e-008), (0, 0.353553, 0),
                             (9.27258e-008, -0.353553, -0.707107), (0.707107,
                             -0.353553, 0), (0, 0.353553, 0), (-3.09086e-008,
                             -0.353553, 0.707107), (0.707107, -0.353553, 0),
                             (-3.09086e-008, -0.353553, 0.707107), (-0.707107,
                             -0.353553, -6.18172e-008)], n='pyramid_01')
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def diamond(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # diamond curve line
        cmds.curve(d=1, p=[(0, 1, 0), (1, 0, 0), (0, 0, 1), (0, 1, 0), (0, 0, -1),
                         (-1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0),
                         (0, -1, 0), (0, 0, 1), (1, 0, 0), (0, -1, 0),
                         (0, 0, -1), (1, 0, 0)], n='diamond_01')
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.curve(d=1, p=[(0, 1, 0), (1, 0, 0), (0, 0, 1), (0, 1, 0),
                             (0, 0, -1), (-1, 0, 0), (0, 1, 0), (0, 0, 1),
                             (-1, 0, 0), (0, -1, 0), (0, 0, 1), (1, 0, 0),
                             (0, -1, 0), (0, 0, -1), (1, 0, 0)], n='diamond_01')
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def quad_arrow(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # arrow curve line
        cmds.curve(d=1, p=[(1, 0, -1), (1, 0, -3), (2, 0, -3), (0, 0, -5),
                         (-2, 0, -3), (-1, 0, -3), (-1, 0, -1), (-3, 0, -1),
                         (-3, 0, -2), (-5, 0, 0), (-3, 0, 2), (-3, 0, 1),
                         (-1, 0, 1), (-1, 0, 3), (-2, 0, 3), (0, 0, 5),
                         (2, 0, 3), (1, 0, 3), (1, 0, 1), (3, 0, 1),
                         (3, 0, 2), (5, 0, 0), (3, 0, -2), (3, 0, -1),
                         (1, 0, -1)], n='quad_arrow_01')
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.curve(d=1, p=[(1, 0, -1), (1, 0, -3), (2, 0, -3), (0, 0, -5),
                             (-2, 0, -3), (-1, 0, -3), (-1, 0, -1), (-3, 0, -1),
                             (-3, 0, -2), (-5, 0, 0), (-3, 0, 2), (-3, 0, 1),
                             (-1, 0, 1), (-1, 0, 3), (-2, 0, 3), (0, 0, 5),
                             (2, 0, 3), (1, 0, 3), (1, 0, 1), (3, 0, 1),
                             (3, 0, 2), (5, 0, 0), (3, 0, -2), (3, 0, -1),
                             (1, 0, -1)], n='quad_arrow_01')
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def curved_plane(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # plane curve line
        cmds.curve(d=3, n='curvedPlane_01', p=[(5, 0, -1), (5, 0, -1), (5, 0, -1),
                                             (2, 3, -1), (-2, 3, -1), (-5, 0,
                                             -1), (-5, 0, -1), (-5, 0, -1), (-5,
                                             0, -1), (-5, 0, 1), (-5, 0, 1),
                                             (-5, 0, 1), (-5, 0, 1), (-2, 3, 1),
                                             (2, 3, 1), (5, 0, 1), (5, 0, 1),
                                             (5, 0, 1), (5, 0, 1), (5, 0, -1)])
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.curve(d=3, n='curvedPlane_01', p=[(5, 0, -1), (5, 0, -1), (5, 0,
                                                 -1), (2, 3, -1), (-2, 3, -1),
                                                 (-5, 0, -1), (-5, 0, -1), (-5,
                                                 0, -1), (-5, 0, -1), (-5, 0,
                                                 1), (-5, 0, 1), (-5, 0, 1),
                                                 (-5, 0, 1), (-2, 3, 1), (2, 3,
                                                 1), (5, 0, 1), (5, 0, 1), (5,
                                                 0, 1), (5, 0, 1), (5, 0, -1)])
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def icosah(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # icosah curve line
        cmds.curve(d=1, n='iso_01', p=[(-0.525731, 0.850651, 0), (0.525731,
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
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.curve(d=1, p=[(-0.525731, 0.850651, 0), (0.525731, 0.850651, 0),
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
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def lever(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        stand = cmds.curve(d=1, p=[(0, 0, 0), (0, 3, 0)], n='lever_01')
        handle = cmds.circle(nr=[0, 0, 1])
        cmds.move(0, 4, 0)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        handle_shape = cmds.listRelatives(handle, shapes=True)
        cmds.parent(handle_shape[0], stand, r=True, s=True)
        cmds.pickWalk(d='up')
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
        cmds.move(0, 0, 0, ".scalePivot", ".rotatePivot")
        cmds.delete(handle[0])
    else:
        for curve_number in range(snap_list_size):
            stand = cmds.curve(d=1, p=[(0, 0, 0), (0, 3, 0)], n='lever_01')
            handle = cmds.circle(nr=[0, 0, 1])
            cmds.move(0, 4, 0)
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            handle_shape = cmds.listRelatives(handle, shapes=True)
            cmds.parent(handle_shape[0], stand, r=True, s=True)
            cmds.pickWalk(d='up')
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            cmds.delete(constructionHistory=True)
            grp()
            cmds.move(0, 0, 0, ".scalePivot", ".rotatePivot")
            cmds.delete(handle[0])
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def arrow(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        cmds.curve(d=3,  p=[(-1, 0, -3), (-1, 0, -3), (-1, 0, -3), (-2, 0, -3),
                          (-2, 0, -3), (-2, 0, -3), (-2, 0, -3), (0, 0, -5),
                          (0, 0, -5), (0, 0, -5), (0, 0, -5), (2, 0, -3),
                          (2, 0, -3), (2, 0, -3), (2, 0, -3), (1, 0, -3),
                          (1, 0, -3), (1, 0, -3), (1, 0, -3), (1, 0, -2),
                          (1, 0, -1), (1, 0, 0), (1, 0, 1), (1, 0, 2),
                          (1, 0, 3), (1, 0, 3), (1, 0, 3), (1, 0, 3),
                          (-1, 0, 3), (-1, 0, 3), (-1, 0, 3), (-1, 0, 3),
                          (-1, 0, 2), (-1, 0, 1), (-1, 0, 0), (-1, 0, -1),
                          (-1, 0, -2), (-1, 0, -3)], n='arrow_01')
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.curve(d=3, p=[(-1, 0, -3), (-1, 0, -3), (-1, 0, -3), (-2, 0, -3),
                             (-2, 0, -3), (-2, 0, -3), (-2, 0, -3), (0, 0, -5),
                             (0, 0, -5), (0, 0, -5), (0, 0, -5), (2, 0, -3),
                             (2, 0, -3), (2, 0, -3), (2, 0, -3), (1, 0, -3),
                             (1, 0, -3), (1, 0, -3), (1, 0, -3), (1, 0, -2),
                             (1, 0, -1), (1, 0, 0), (1, 0, 1), (1, 0, 2),
                             (1, 0, 3), (1, 0, 3), (1, 0, 3), (1, 0, 3),
                             (-1, 0, 3), (-1, 0, 3), (-1, 0, 3), (-1, 0, 3),
                             (-1, 0, 2), (-1, 0, 1), (-1, 0, 0), (-1, 0, -1),
                             (-1, 0, -2), (-1, 0, -3)], n='arrow_01')
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def palm(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        cmds.curve(d=3, p=[(-2, 0, 3), (-2, 0, 3), (-2, 0, 3), (0, 0, 2),
                         (2, 0, 3), (2, 0, 3), (2, 0, 3), (2, 0, 3), (4, 0, -5),
                         (4, 0, -5), (4, 0, -5), (4, 0, -5), (0, 0, -7),
                         (-4, 0, -5), (-4, 0, -5), (-4, 0, -5), (-4, 0, -5),
                         (-2, 0, 3)], n='palmCurve_01')
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.curve(d=3, p=[(-2, 0, 3), (-2, 0, 3), (-2, 0, 3), (0, 0, 2),
                             (2, 0, 3), (2, 0, 3), (2, 0, 3), (2, 0, 3),
                             (4, 0, -5), (4, 0, -5), (4, 0, -5), (4, 0, -5),
                             (0, 0, -7), (-4, 0, -5), (-4, 0, -5), (-4, 0, -5),
                             (-4, 0, -5), (-2, 0, 3)], n='palmCurve_01')
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def plus(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        cmds.curve(d=1,  p=[(-1, 0, -1), (-1, 0, -3), (1, 0, -3), (1, 0, -1),
                          (3, 0, -1), (3, 0, 1), (1, 0, 1), (1, 0, 3),
                          (-1, 0, 3), (-1, 0, 1), (-3, 0, 1), (-3, 0, -1),
                          (-1, 0, -1)], n='plus_01')
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.curve(d=1, p=[(-1, 0, -1), (-1, 0, -3), (1, 0, -3), (1, 0, -1),
                             (3, 0, -1), (3, 0, 1), (1, 0, 1), (1, 0, 3),
                             (-1, 0, 3), (-1, 0, 1), (-3, 0, 1), (-3, 0, -1),
                             (-1, 0, -1)], n='plus_01')
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def loc(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        cmds.spaceLocator()
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.spaceLocator()
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def trapezoid_cube(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        cmds.curve(d=1,  p=[(-0.5, 0.5, 0.5), (-1, 0, 1), (1, 0, 1), (0.5, 0.5,
                          0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (-1, 0,
                          -1), (-1, 0, 1), (-0.5, -0.5, 0.5), (-0.5, -0.5,
                          -0.5), (-1, 0, -1), (1, 0, -1), (0.5, -0.5, -0.5),
                          (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (0.5, -0.5,
                          0.5), (0.5, -0.5, -0.5), (1, 0, -1), (0.5, 0.5, -0.5),
                          (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5),
                          (1, 0, 1), (0.5, -0.5, 0.5), (1, 0, 1), (1, 0, -1)],
                 n='trapezoid_cube_01')
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.curve(d=1, p=[(-0.5, 0.5, 0.5), (-1, 0, 1), (1, 0, 1), (0.5, 0.5,
                             0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (-1, 0,
                             -1), (-1, 0, 1), (-0.5, -0.5, 0.5), (-0.5, -0.5,
                             -0.5), (-1, 0, -1), (1, 0, -1), (0.5, -0.5, -0.5),
                             (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (0.5, -0.5,
                             0.5), (0.5, -0.5, -0.5), (1, 0, -1), (0.5, 0.5,
                             -0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5,
                             0.5, 0.5), (1, 0, 1), (0.5, -0.5, 0.5), (1, 0, 1),
                             (1, 0, -1)], n='trapezoid_cube_01')
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def ring(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        cmds.curve(d=1,  p=[(0.707107, 0.1, 0.707107), (1, 0.1, 0), (1, -0.1, 0),
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
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.curve(d=1,
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
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def tube(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        # creating the curves
        t1 = cmds.curve(d=2, p=[(1, 2, 0), (1, 0, 0), (1, -2, 0)])
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        t2 = cmds.curve(d=2, p=[(-1, 2, 0), (-1, 0, 0), (-1, -2, 0)])
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        t3 = cmds.curve(d=2, p=[(0, 2, 1), (0, 0, 1), (0, -2, 1)])
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        t4 = cmds.curve(d=2, p=[(0, 2, -1), (0, 0, -1), (0, -2, -1)])
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        t5 = cmds.circle(nr=[0, 1, 0])
        cmds.move(0, 2, 0)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        t6 = cmds.circle(nr=[0, 1, 0], n='tube_01')
        cmds.move(0, -2, 0)
        # parenting the curves
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        rc2 = cmds.listRelatives(t1, shapes=True)
        cmds.parent(rc2[0], t6, r=True, shape=True)
        rc3 = cmds.listRelatives(t2, shapes=True)
        cmds.parent(rc3[0], t6, r=True, shape=True)
        rc2 = cmds.listRelatives(t3, shapes=True)
        cmds.parent(rc2[0], t6, r=True, shape=True)
        rc3 = cmds.listRelatives(t4, shapes=True)
        cmds.parent(rc3[0], t6, r=True, shape=True)
        rc2 = cmds.listRelatives(t5, shapes=True)
        cmds.parent(rc2[0], t6, r=True, shape=True)
        # deleting leftover groups
        cmds.delete(constructionHistory=True)
        cmds.delete(t1)
        cmds.delete(t2)
        cmds.delete(t3)
        cmds.delete(t4)
        cmds.delete(t5[0])
        # centering the pivot
        cmds.xform('tube_01', cp=True)
        cmds.pickWalk(d='up')
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            # creating the curves
            t1 = cmds.curve(d=2, p=[(1, 2, 0), (1, 0, 0), (1, -2, 0)])
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            t2 = cmds.curve(d=2, p=[(-1, 2, 0), (-1, 0, 0), (-1, -2, 0)])
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            t3 = cmds.curve(d=2, p=[(0, 2, 1), (0, 0, 1), (0, -2, 1)])
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            t4 = cmds.curve(d=2, p=[(0, 2, -1), (0, 0, -1), (0, -2, -1)])
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            t5 = cmds.circle(nr=[0, 1, 0])
            cmds.move(0, 2, 0)
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            t6 = cmds.circle(nr=[0, 1, 0], n='tube_01')
            cmds.move(0, -2, 0)
            # parenting the curves
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False,
                            pn=True)
            rc2 = cmds.listRelatives(t1, shapes=True)
            cmds.parent(rc2[0], t6, r=True, shape=True)
            rc3 = cmds.listRelatives(t2, shapes=True)
            cmds.parent(rc3[0], t6, r=True, shape=True)
            rc2 = cmds.listRelatives(t3, shapes=True)
            cmds.parent(rc2[0], t6, r=True, shape=True)
            rc3 = cmds.listRelatives(t4, shapes=True)
            cmds.parent(rc3[0], t6, r=True, shape=True)
            rc2 = cmds.listRelatives(t5, shapes=True)
            cmds.parent(rc2[0], t6, r=True, shape=True)
            # deleting leftover groups
            cmds.delete(constructionHistory=True)
            cmds.delete(t1)
            cmds.delete(t2)
            cmds.delete(t3)
            cmds.delete(t4)
            cmds.delete(t5[0])
            # centering the pivot
            cmds.xform(t6, cp=True)
            cmds.pickWalk(d='up')
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)


def half_dome(*arg):
    selection_list = cmds.ls(sl=True)
    snap_list_size = len(selection_list)
    if snap_list_size == 0:
        cmds.circle(nr=[0, 1, 0], n='half_dome_01')
        cmds.move(0, 0, 0.783612, '.cv[0]', r=True, os=True, wd=True)
        cmds.move(0, 0, 1.108194, '.cv[1]', r=True, os=True, wd=True)
        cmds.move(0, 0, 0.783612, '.cv[2]', r=True, os=True, wd=True)
        cmds.delete(constructionHistory=True)
        curve_selection_list = cmds.ls(sl=True)
        curve_rename(curve_selection_list, selection_list, 0, 'null')
        grp()
    else:
        for curve_number in range(snap_list_size):
            cmds.circle(nr=[0, 1, 0], n='half_dome_01')
            cmds.move(0, 0, 0.783612, '.cv[0]', r=True, os=True, wd=True)
            cmds.move(0, 0, 1.108194, '.cv[1]', r=True, os=True, wd=True)
            cmds.move(0, 0, 0.783612, '.cv[2]', r=True, os=True, wd=True)
            cmds.delete(constructionHistory=True)
            curve_selection_list = cmds.ls(sl=True)
            selection_name = selection_list[curve_number]
            curve_rename(curve_selection_list, selection_list, curve_number,
                         selection_name)
            grp()
            selection_size = curve_number + 1
            snap_position(selection_list, selection_size)

# Color Functions #


def red(*arg):
    sel = cmds.ls(sl=True)
    for col in sel:
        cmds.setAttr((col + '.overrideEnabled'), 1)
        cmds.setAttr((col + '.overrideRGBColors'), 1)
        cmds.setAttr((col + ".overrideColorR"), 1)
        cmds.setAttr((col + ".overrideColorG"), 0)
        cmds.setAttr((col + ".overrideColorB"), 0)


def blue(*arg):
    sel = cmds.ls(sl=True)
    for col in sel:
        cmds.setAttr((col + '.overrideEnabled'), 1)
        cmds.setAttr((col + '.overrideRGBColors'), 1)
        cmds.setAttr((col + ".overrideColorR"), 0)
        cmds.setAttr((col + ".overrideColorG"), 0)
        cmds.setAttr((col + ".overrideColorB"), 1)


def yellow(*arg):
    sel = cmds.ls(sl=True)
    for col in sel:
        cmds.setAttr((col + '.overrideEnabled'), 1)
        cmds.setAttr((col + '.overrideRGBColors'), 1)
        cmds.setAttr((col + ".overrideColorR"), 1)
        cmds.setAttr((col + ".overrideColorG"), 1)
        cmds.setAttr((col + ".overrideColorB"), 0)


def pink(*arg):
    sel = cmds.ls(sl=True)
    for col in sel:
        cmds.setAttr((col + '.overrideEnabled'), 1)
        cmds.setAttr((col + '.overrideRGBColors'), 1)
        cmds.setAttr((col + ".overrideColorR"), 1)
        cmds.setAttr((col + ".overrideColorG"), .5)
        cmds.setAttr((col + ".overrideColorB"), .5)


def cyan(*arg):
    sel = cmds.ls(sl=True)
    for col in sel:
        cmds.setAttr((col + '.overrideEnabled'), 1)
        cmds.setAttr((col + '.overrideRGBColors'), 1)
        cmds.setAttr((col + ".overrideColorR"), 0)
        cmds.setAttr((col + ".overrideColorG"), 1)
        cmds.setAttr((col + ".overrideColorB"), 1)


def orange(*arg):
    sel = cmds.ls(sl=True)
    for col in sel:
        cmds.setAttr((col + '.overrideEnabled'), 1)
        cmds.setAttr((col + '.overrideRGBColors'), 1)
        cmds.setAttr((col + ".overrideColorR"), 1)
        cmds.setAttr((col + ".overrideColorG"), .5)
        cmds.setAttr((col + ".overrideColorB"), 0)


def gray(*arg):
    sel = cmds.ls(sl=True)
    for col in sel:
        cmds.setAttr((col + '.overrideEnabled'), 1)
        cmds.setAttr((col + '.overrideRGBColors'), 1)
        cmds.setAttr((col + ".overrideColorR"), .5)
        cmds.setAttr((col + ".overrideColorG"), .5)
        cmds.setAttr((col + ".overrideColorB"), .5)


def white(*arg):
    sel = cmds.ls(sl=True)
    for col in sel:
        cmds.setAttr((col + '.overrideEnabled'), 1)
        cmds.setAttr((col + '.overrideRGBColors'), 1)
        cmds.setAttr((col + ".overrideColorR"), 1)
        cmds.setAttr((col + ".overrideColorG"), 1)
        cmds.setAttr((col + ".overrideColorB"), 1)


def magenta(*arg):
    sel = cmds.ls(sl=True)
    for col in sel:
        cmds.setAttr((col + '.overrideEnabled'), 1)
        cmds.setAttr((col + '.overrideRGBColors'), 1)
        cmds.setAttr((col + ".overrideColorR"), 1)
        cmds.setAttr((col + ".overrideColorG"), 0)
        cmds.setAttr((col + ".overrideColorB"), 1)


def other_color(*arg):
    sel = cmds.ls(sl=True)
    cmds.colorEditor()
    if cmds.colorEditor(query=True, result=True):
        color_editor = cmds.colorEditor(query=True, rgb=True)
        print 'Custom Color Value: ' + str(color_editor)
        for col in sel:
            cmds.setAttr((col + '.overrideEnabled'), 1)
            cmds.setAttr((col + '.overrideRGBColors'), 1)
            cmds.setAttr((col + ".overrideColorR"), color_editor[0])
            cmds.setAttr((col + ".overrideColorG"), color_editor[1])
            cmds.setAttr((col + ".overrideColorB"), color_editor[2])


def hand_attr(*arg):
    # adding attributes
    cmds.addAttr(ci=True, sn='IKFK', ln='IKFK', min=0, max=1, at='double',
               defaultValue=1)
    cmds.addAttr(ci=True, ln='bendy',  at='double',  min=0, max=1, dv=0)
    cmds.addAttr(ci=True, sn='_', ln='_', min=0, max=0, en='Masters', at='enum')
    cmds.addAttr(ci=True, sn='spread', ln='spread', min=-10, max=10, at='double')
    cmds.addAttr(ci=True, sn='masterRot', ln='masterRotation', at='double')
    cmds.addAttr(ci=True, sn='offset', ln='offset', at='double')
    cmds.addAttr(ci=True, sn='offsetFavor', ln='offsetFavor', min=0, max=1,
               en='Pinky:Index', at='enum')
    cmds.addAttr(ci=True, sn='__', ln='__', min=0, max=0, en='Index', at='enum')
    cmds.addAttr(ci=True, sn='indexBase', ln='indexBase', at='double')
    cmds.addAttr(ci=True, sn='indexMid', ln='indexMid', at='double')
    cmds.addAttr(ci=True, sn='indexEnd', ln='indexEnd', at='double')
    cmds.addAttr(ci=True, sn='___', ln='___', min=0, max=0, en='Middle',
               at='enum')
    cmds.addAttr(ci=True, sn='middleBase', ln='middleBase', at='double')
    cmds.addAttr(ci=True, sn='middleMid', ln='middleMid', at='double')
    cmds.addAttr(ci=True, sn='middleEnd', ln='middleEnd', at='double')
    cmds.addAttr(ci=True, sn='____', ln='____', min=0, max=0, en='Ring',
               at='enum')
    cmds.addAttr(ci=True, sn='ringBase', ln='ringBase', at='double')
    cmds.addAttr(ci=True, sn='ringMid', ln='ringMid', at='double')
    cmds.addAttr(ci=True, sn='ringEnd', ln='ringEnd', at='double')
    cmds.addAttr(ci=True, sn='_____', ln='_____', min=0, max=0, en='Pinky',
               at='enum')
    cmds.addAttr(ci=True, sn='pinkyBase', ln='pinkyBase', at='double')
    cmds.addAttr(ci=True, sn='pinkyMid', ln='pinkyMid', at='double')
    cmds.addAttr(ci=True, sn='pinkyEnd', ln='pinkyEnd', at='double')
    cmds.addAttr(ci=True, sn='______', ln='______', min=0, max=0, en='Thumb',
               at='enum')
    cmds.addAttr(ci=True, sn='thumbMid', ln='thumbMid', at='double')
    cmds.addAttr(ci=True, sn='thumbEnd', ln='thumbEnd', at='double')
    cmds.addAttr(ci=True, sn='_______', ln='_______', min=0, max=0, en='Vis',
               at='enum')
    cmds.addAttr(ci=True, sn='masterVis', ln='masterVis', min=0, max=1, at='long',
               defaultValue=1)
    cmds.addAttr(ci=True, sn='thumbVis', ln='thumbVis', min=0, max=1, at='long',
               defaultValue=1)
    cmds.addAttr(ci=True, sn='indexVis', ln='indexVis', min=0, max=1, at='long',
               defaultValue=1)
    cmds.addAttr(ci=True, sn='middleVis', ln='middleVis', min=0, max=1, at='long',
               defaultValue=1)
    cmds.addAttr(ci=True, sn='pinkyVis', ln='pinkyVis', min=0, max=1, at='long',
               defaultValue=1)
    # setting keyability
    cmds.setAttr('.IKFK', keyable=True)
    cmds.setAttr('.bendy', keyable=True)
    cmds.setAttr('._', channelBox=True)
    cmds.setAttr('.spread', keyable=True)
    cmds.setAttr('.masterRot', keyable=True)
    cmds.setAttr('.offset', keyable=True)
    cmds.setAttr('.offsetFavor', keyable=True)
    cmds.setAttr('.__', channelBox=True)
    cmds.setAttr('.indexBase', keyable=True)
    cmds.setAttr('.indexMid', keyable=True)
    cmds.setAttr('.indexEnd', keyable=True)
    cmds.setAttr('.___', channelBox=True)
    cmds.setAttr('.middleBase', keyable=True)
    cmds.setAttr('.middleMid', keyable=True)
    cmds.setAttr('.middleEnd', keyable=True)
    cmds.setAttr('.____', channelBox=True)
    cmds.setAttr('.ringBase', keyable=True)
    cmds.setAttr('.ringMid', keyable=True)
    cmds.setAttr('.ringEnd', keyable=True)
    cmds.setAttr('._____', channelBox=True)
    cmds.setAttr('.pinkyBase', keyable=True)
    cmds.setAttr('.pinkyMid', keyable=True)
    cmds.setAttr('.pinkyEnd', keyable=True)
    cmds.setAttr('.______', channelBox=True)
    cmds.setAttr('.thumbMid', keyable=True)
    cmds.setAttr('.thumbEnd', keyable=True)
    cmds.setAttr('._______', channelBox=True)
    cmds.setAttr('.masterVis', keyable=True)
    cmds.setAttr('.thumbVis', keyable=True)
    cmds.setAttr('.indexVis', keyable=True)
    cmds.setAttr('.middleVis', keyable=True)
    cmds.setAttr('.pinkyVis', keyable=True)
    # lock and hide unnecessary attributes
    for attr in attributes:
        cmds.setAttr(attr, lock=True, keyable=False)


def reverse_foot_attr(*arg):
    # adding attributes
    cmds.addAttr(ci=True, sn='_', ln='_', min=0, max=0, en='Controls', at='enum')
    cmds.addAttr(ci=True, ln='ballRoll',  at='double',  dv=0)
    cmds.addAttr(ci=True, ln='footBank',  at='double',  dv=0)
    cmds.addAttr(ci=True, ln='toeBend',  at='double',  dv=0)
    cmds.addAttr(ci=True, ln='toePivot',  at='double',  dv=0)
    cmds.addAttr(ci=True, ln='toeRoll',  at='double',  dv=0)
    cmds.addAttr(ci=True, ln='heelPivot',  at='double',  dv=0)
    cmds.addAttr(ci=True, ln='heelRoll',  at='double',  dv=0)
    cmds.addAttr(ci=True, sn='stretch', ln='stretch', min=0, max=1, at='long',
               defaultValue=0)
    cmds.addAttr(ci=True, ln='bendy',  at='double',  min=0, max=1, dv=0)
    # setting keyability
    cmds.setAttr('._', channelBox=True)
    cmds.setAttr('.ballRoll', keyable=True)
    cmds.setAttr('.footBank', keyable=True)
    cmds.setAttr('.toeBend', keyable=True)
    cmds.setAttr('.toePivot', keyable=True)
    cmds.setAttr('.toeRoll', keyable=True)
    cmds.setAttr('.heelPivot', keyable=True)
    cmds.setAttr('.heelRoll', keyable=True)
    cmds.setAttr('.stretch', keyable=True)
    cmds.setAttr('.bendy', keyable=True)
    # lock and hide unnecessary attributes
    cmds.setAttr('.sx', lock=True, keyable=False)
    cmds.setAttr('.sy', lock=True, keyable=False)
    cmds.setAttr('.sz', lock=True, keyable=False)
    cmds.setAttr('.v', lock=True, keyable=False)


def foot_switch(*arg):
    # adding attributes
    cmds.addAttr(ci=True, sn='IKFK', ln='IKFK', min=0, max=1, at='double',
               defaultValue=1)
    cmds.addAttr(ci=True, sn='toeControls', ln='toeControls', min=0, max=1,
               at='long', dv=1)
    # setting keyability
    cmds.setAttr('.IKFK', keyable=True)
    cmds.setAttr('.toeControls', channelBox=True)
    # lock and hide unnecessary attributes
    for attr in attributes:
        cmds.setAttr(attr, lock=True, keyable=False)


def sync_phoneme_attr(*arg):
    # adding attributes
    cmds.addAttr(ci=True, sn='_', ln='_', min=0, max=1, en='Sync', at='enum')
    cmds.addAttr(ci=True, sn='__', ln='__', min=0, max=0, en='Open', at='enum')
    cmds.addAttr(ci=True, sn='A', ln='A', min=0, max=1, at='double')
    cmds.addAttr(ci=True, sn='E', ln='E', min=0, max=1, at='double')
    cmds.addAttr(ci=True, sn='I', ln='I', min=0, max=1, at='double')
    cmds.addAttr(ci=True, sn='O_H', ln='O_H', min=0, max=1, at='double')
    cmds.addAttr(ci=True, sn='U_W', ln='U_W', min=0, max=1, at='double')
    cmds.addAttr(ci=True, sn='L', ln='L', min=0, max=1, at='double')
    cmds.addAttr(ci=True, sn='S_D_G_e_General', ln='S_D_G_e_General', min=0,
               max=1, at='double')
    cmds.addAttr(ci=True, sn='___', ln='___', min=0, max=0, en='Closed',
               at='enum')
    cmds.addAttr(ci=True, sn='F_V', ln='F_V', min=0, max=1, at='double')
    cmds.addAttr(ci=True, sn='M_P_B', ln='M_P_B', min=0, max=1, at='double')
    cmds.addAttr(ci=True, sn='____', ln='____', min=0, max=0, en='Tongue',
               at='enum')
    cmds.addAttr(ci=True, sn='upDown', ln='upDown', min=-2, max=10, at='double')
    cmds.addAttr(ci=True, sn='leftRight', ln='leftRight', min=-5, max=5,
               at='double')
    # setting keyability
    cmds.setAttr('._', channelBox=True)
    cmds.setAttr('.__', channelBox=True)
    cmds.setAttr('.A', keyable=True)
    cmds.setAttr('.E', keyable=True)
    cmds.setAttr('.I', keyable=True)
    cmds.setAttr('.O_H', keyable=True)
    cmds.setAttr('.U_W', keyable=True)
    cmds.setAttr('.L', keyable=True)
    cmds.setAttr('.S_D_G_e_General', keyable=True)
    cmds.setAttr('.___', channelBox=True)
    cmds.setAttr('.F_V', keyable=True)
    cmds.setAttr('.M_P_B', keyable=True)
    cmds.setAttr('.____', channelBox=True)
    cmds.setAttr('.upDown', keyable=True)
    cmds.setAttr('.leftRight', keyable=True)
    # lock and hide unnecessary attributes
    for attr in attributes:
        cmds.setAttr(attr, lock=True, keyable=False)


def world_space(*arg):
    # check if a Space enum separator already exists, add if false
    attribute_selection = cmds.ls(sl=True)
    q = cmds.attributeQuery('_________', node=attribute_selection[0], exists=True)
    if q is False:
        cmds.addAttr(ci=True, sn='_________', ln='_________', min=0, max=1,
                   en='Spaces', at='enum')
        cmds.setAttr('._________', cb=True)
    # add the new attribute
    cmds.addAttr(ci=True, sn='world', ln='world', min=0, max=1, at='double')
    cmds.setAttr('.world', k=True)


def head_space(*arg):
    # check if a Space enum separator already exists, add if false
    attribute_selection = cmds.ls(sl=True)
    q = cmds.attributeQuery('_________', node=attribute_selection[0], exists=True)
    if q is False:
        cmds.addAttr(ci=True, sn='_________', ln='_________', min=0, max=1,
                   en='Spaces', at='enum')
        cmds.setAttr('._________', cb=True)
    # add the new attribute
    cmds.addAttr(ci=True, sn='head', ln='head', min=0, max=1, at='double')
    cmds.setAttr('.head', k=True)


def hand_space(*arg):
    # check if a Space enum separator already exists, add if false
    attribute_selection = cmds.ls(sl=True)
    q = cmds.attributeQuery('_________', node=attribute_selection[0], exists=True)
    if q is False:
        cmds.addAttr(ci=True, sn='_________', ln='_________', min=0, max=1,
                   en='Spaces', at='enum')
        cmds.setAttr('._________', cb=True)
        # add the new attribute
    cmds.addAttr(ci=True, sn='hand', ln='hand', min=0, max=1, at='double')
    cmds.setAttr('.hand', k=True)


def foot_space(*arg):
    # check if a Space enum separator already exists, add if false
    attribute_selection = cmds.ls(sl=True)
    q = cmds.attributeQuery('_________', node=attribute_selection[0], exists=True)
    if q is False:
        cmds.addAttr(ci=True, sn='_________', ln='_________', min=0, max=1,
                   en='Spaces', at='enum')
        cmds.setAttr('._________', cb=True)
    # add the new attribute
    cmds.addAttr(ci=True, sn='foot', ln='foot', min=0, max=1, at='double')
    cmds.setAttr('.foot', k=True)


def cog_space(*arg):
    # check if a Space enum separator already exists, add if false
    attribute_selection = cmds.ls(sl=True)
    q = cmds.attributeQuery('_________', node=attribute_selection[0], exists=True)
    if q is False:
        cmds.addAttr(ci=True, sn='_________', ln='_________', min=0, max=1,
                   en='Spaces', at='enum')
        cmds.setAttr('._________', cb=True)
    # add the new attribute
    cmds.addAttr(ci=True, sn='Cother_group_value', ln='Cother_group_value', min=0,
               max=1, at='double')
    cmds.setAttr('.Cother_group_value', k=True)


def about_window(*arg):
    window_name = 'aboutWin'
    window_title = 'About Rigging Control Curves'
    # check if window exists
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name, window=True)
    # setup window
    cmds.window(window_name, title=window_title, sizeable=True)
    cmds.scrollLayout()
    cmds.columnLayout(adjustableColumn=True)

    cmds.text(label=aboutText, al='left')
    cmds.showWindow(window_name)
    cmds.window(window_name, edit=True, width=425, height=400)


def naming_enable(*arg):
    name_box_value = cmds.checkBox('overrideName', q=True, v=True)
    if name_box_value is False:
        cmds.textField('CurvePrefix', e=True, en=1)
        cmds.textField('CurveName', e=True, en=1)
        cmds.textField('CurveSuffix', e=True, en=1)
    if name_box_value is True:
        cmds.textField('CurvePrefix', e=True, en=0)
        cmds.textField('CurveName', e=True, en=0)
        cmds.textField('CurveSuffix', e=True, en=0)


def grp_enable(*arg):
    grp_box_value = cmds.checkBox('otherBox', q=True, v=True)
    cmds.textField('otherGrp', e=True, en=grp_box_value)


def lock_attr(*arg):
    selection_list = cmds.ls(sl=True)

    for attr in attributes:
        if cmds.checkBox(attr.replace('.', '').upper(), q=True, v=True) is True:
            cmds.setAttr(selection_list[0] + attr, lock=True)


def unlock_attr(*arg):
    selection_list = cmds.ls(sl=True)

    for attr in attributes:
        if cmds.checkBox(attr.replace('.', '').upper(), q=True, v=True) is True:
            cmds.setAttr(selection_list[0] + attr, lock=False)


def hide_attr(*arg):
    selection_list = cmds.ls(sl=True)

    for attr in attributes:
        if cmds.checkBox(attr.replace('.', '').upper(), q=True, v=True) is True:
            cmds.setAttr(selection_list[0] + attr, keyable=False,
                       channelBox=False)


def show_attr(*arg):
    selection_list = cmds.ls(sl=True)

    for attr in attributes:
        if cmds.checkBox(attr.replace('.', '').upper(), q=True, v=True) is True:
            cmds.setAttr(selection_list[0] + attr, keyable=True)


def lock_hide_attr(*arg):
    lock_attr()
    hide_attr()


def unlock_show_attr(*arg):
    unlock_attr()
    show_attr()


def change_attr_box(*arg):
    translation = cmds.checkBox('allT', q=True, v=True)
    rotation = cmds.checkBox('allR', q=True, v=True)
    scaling = cmds.checkBox('allS', q=True, v=True)
    all = cmds.checkBox('allBox', q=True, v=True)

    cmds.checkBox('TX', e=True, v=translation)
    cmds.checkBox('TY', e=True, v=translation)
    cmds.checkBox('TZ', e=True, v=translation)

    cmds.checkBox('RX', e=True, v=rotation)
    cmds.checkBox('RY', e=True, v=rotation)
    cmds.checkBox('RZ', e=True, v=rotation)

    cmds.checkBox('SX', e=True, v=scaling)
    cmds.checkBox('SY', e=True, v=scaling)
    cmds.checkBox('SZ', e=True, v=scaling)


def check_all(*arg):
    all = cmds.checkBox('allBox', q=True, v=True)

    cmds.checkBox('allT', e=True, v=all)
    cmds.checkBox('allR', e=True, v=all)
    cmds.checkBox('allS', e=True, v=all)
    cmds.checkBox('V', e=True, v=all)
    change_attr_box()


# The Actual Window #


def nick_curves_mill():
    # assign window names
    window_name = 'crvWin'
    window_title = 'Rigging Control Curves'
    # check if window exists
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name, window=True)
    # setup window
    cmds.window(window_name, title=window_title, sizeable=True)
    cmds.columnLayout(adjustableColumn=True)
    # menuBar
    cmds.menuBarLayout()
    cmds.menu(label='File')
    cmds.menuItem(label='Test')
    cmds.menu(label='Help', helpMenu=True)
    cmds.menuItem(label='About...', c=about_window)
    #
    cmds.columnLayout(adjustableColumn=True)
    # Naming Layout
    cmds.frameLayout(label='Naming Conventions', mw=4, mh=4,
                   bgc=[0.18, 0.21, 0.25])
    cmds.rowColumnLayout(numberOfColumns=3,
                       columnWidth=[(1, 100), (2, 150), (3, 100)])
    cmds.text('Prefix')
    cmds.text('Name')
    cmds.text('Suffix')
    cmds.textField('CurvePrefix')
    cmds.textField('CurveName')
    cmds.textField('CurveSuffix')
    cmds.checkBox('overrideName', label='Override Name', cc=naming_enable)
    cmds.setParent('..')
    cmds.setParent('..')
    # Group Layout
    cmds.frameLayout(label='Grouping', mw=4, mh=4, bgc=[0.18, 0.21, 0.25])
    cmds.rowColumnLayout(numberOfColumns=3,
                       columnWidth=[(1, 115), (2, 115), (3, 115)])
    cmds.checkBox('zeroBox', label='ZERO')
    cmds.checkBox('srtBox', label='SRT')
    cmds.checkBox('sdkBox', label='SDK')
    cmds.checkBox('spaceBox', label='SPACE')
    cmds.checkBox('ofsBox', label='OFS')
    cmds.checkBox('dummyBox', label='DUMMY')
    cmds.checkBox('otherBox', label='Other', cc=grp_enable)
    cmds.textField('otherGrp', w=200, en=False)
    cmds.setParent('..')
    cmds.setParent('..')
    # Curves Layout
    cmds.frameLayout(label='Curves', mw=4, mh=4, bgc=[0.18, 0.21, 0.25])
    cmds.rowColumnLayout(numberOfColumns=4,
                       columnWidth=[(1, 85), (2, 85), (3, 85), (4, 85)])
    cmds.button(label='Circle', command=cir)
    cmds.button(label='Square', command=square)
    cmds.button(label='Triangle', command=triangle)
    cmds.button(label='Octagon', command=octagon)
    cmds.button(label='Sphere', command=sphere)
    cmds.button(label='Box', command=box)
    cmds.button(label='Pyramid', command=pyramid)
    cmds.button(label='Diamond', command=diamond)
    cmds.button(label='Quad Arrow', command=quad_arrow)
    cmds.button(label='Curved Plane', command=curved_plane)
    cmds.button(label='Icosah', command=icosah)
    cmds.button(label='Lever', command=lever)
    cmds.button(label='Arrow', command=arrow)
    cmds.button(label='Palm', command=palm)
    cmds.button(label='Plus', command=plus)
    cmds.button(label='Locator', command=loc)
    cmds.button(label='Trap Cube', command=trapezoid_cube)
    cmds.button(label='Ring', command=ring)
    cmds.button(label='Tube', command=tube)
    cmds.button(label='Half Dome', command=half_dome)
    cmds.setParent('..')
    cmds.setParent('..')
    # Color Options
    cmds.frameLayout(label='Colors', mw=4, mh=4, bgc=[0.18, 0.21, 0.25])
    cmds.rowColumnLayout(numberOfColumns=3,
                       columnWidth=[(1, 100), (2, 150), (3, 100)])
    cmds.button(command=red, label='', bgc=[1, 0, 0])
    cmds.button(command=yellow, label='', bgc=[1, 1, 0])
    cmds.button(command=blue, label='', bgc=[0, 0, 1])
    cmds.button(command=pink, label='', bgc=[1, .5, .5])
    cmds.button(command=orange, label='', bgc=[1, .5, 0])
    cmds.button(command=cyan, label='', bgc=[0, 1, 1])
    cmds.button(command=gray, label='', bgc=[.5, .5, .5])
    cmds.button(command=white, label='', bgc=[1, 1, 1])
    cmds.button(command=magenta, label='', bgc=[1, 0, 1])
    cmds.setParent('..')
    cmds.columnLayout(columnAlign='center')
    cmds.button(command=other_color, label='Choose Custom Color', w=350, h=30)
    cmds.setParent('..')
    cmds.setParent('..')

    # Lock/Unlock/Hide Attribute Options
    cmds.frameLayout(label='Lock & Hide Attributes', mw=4, mh=4,
                   bgc=[0.18, 0.21, 0.25])
    cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 150), (2, 200)])
    cmds.rowColumnLayout(numberOfColumns=5, columnWidth=[(1, 50), (2, 25),
                       (3, 25), (4, 25), (5, 25)], columnAlign=[(1, 'right'),
                       (2, 'left'), (3, 'left'), (4, 'left'), (5, 'left')])
    cmds.text('space1', label='')
    cmds.text('X')
    cmds.text('Y')
    cmds.text('Z')
    cmds.text('All')
    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.text('T  ')
    cmds.checkBox('TX', label='')
    cmds.checkBox('TY', label='')
    cmds.checkBox('TZ', label='')
    cmds.checkBox('allT', label='', cc=change_attr_box)
    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.text('R  ')
    cmds.checkBox('RX', label='')
    cmds.checkBox('RY', label='')
    cmds.checkBox('RZ', label='')
    cmds.checkBox('allR', label='', cc=change_attr_box)
    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.text('S  ')
    cmds.checkBox('SX', label='')
    cmds.checkBox('SY', label='')
    cmds.checkBox('SZ', label='')
    cmds.checkBox('allS', label='', cc=change_attr_box)
    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.separator()
    cmds.text('Visibility  ')
    cmds.checkBox('V', label='')
    cmds.text('space2', label='')
    cmds.text('space3', label='')
    cmds.checkBox('allBox', label='', cc=check_all)
    cmds.setParent('..')
    cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 100), (2, 100)])
    cmds.columnLayout()
    cmds.button(label='Lock', c=lock_attr, w=100)
    cmds.button(label='Unlock', c=unlock_attr, w=100)
    cmds.button(label='Hide', c=hide_attr, w=100)
    cmds.button(label='Show', c=show_attr, w=100)
    cmds.setParent('..')
    cmds.columnLayout()
    cmds.button(label='Lock and Hide', c=lock_hide_attr, w=100, h=45)
    cmds.button(label='Unlock and Show', c=unlock_show_attr, w=100, h=45)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    # Attribute Options  ## Needs updating
    cmds.frameLayout(label='Attribute Presets', cll=True, cl=True, mw=4, mh=4,
                   bgc=[0.18, 0.21, 0.25])
    cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 175), (2, 175)])
    cmds.button(label='Hand Attributes', command=hand_attr)
    cmds.button(label='IK Reverse Foot', command=reverse_foot_attr)
    cmds.button(label='Foot Switch', command=foot_switch)
    cmds.button(label='Sync Phonemes', command=sync_phoneme_attr)
    cmds.button(label='World Space', command=world_space)
    cmds.button(label='Head Space', command=head_space)
    cmds.button(label='Hand Space', command=hand_space)
    cmds.button(label='Foot Space', command=foot_space)
    cmds.button(label='Cother_group_value Space', command=cog_space)
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.showWindow(window_name)
    cmds.window(window_name, edit=True, width=200, height=210)
