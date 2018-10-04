import maya.cmds as mc

def spaceConnection(A, B, C, D, E, F, G, H):
    sel = mc.ls(sl=True)
    #r = len(sel)
    i0 = A + '_'
    i1 = B + '_'
    i2 = C + '_'
    i3 = D + '_'
    i4 = E + '_'
    i5 = F + '_'
    f1 = '.' + H
    
    for s in sel:
        i = len(s)
        j = i - 4
        a = 0
        for space in range(6):
            b = str(a)
            if a == 0 and len(i0) > 1:
                name = s[:j] + i0 + s[j:]
                cndName = name.replace('CTRL', 'SPACE_CND')
                conName = s.replace('CTRL', 'SPACE_parentConstraint1')
                CND = mc.createNode('condition', n=cndName)
                mc.setAttr(CND + '.secondTerm', 0)
                mc.setAttr(CND + '.colorIfTrueR', 1)
                mc.setAttr(CND + '.colorIfFalseR', 0)
                mc.connectAttr(s + f1, CND + '.firstTerm', f=True)
                if G == 0:
                    mc.connectAttr(CND + '.outColorR', conName + '.C_global_SPACEW' + b)
                elif G == 1:
                    mc.connectAttr(CND + '.outColorR', conName + '.' + i0 + 'SPACEW' + b)
            elif a == 1 and len(i1) > 1:
                name = s[:j] + i1 + s[j:]
                cndName = name.replace('CTRL', 'SPACE_CND')
                conName = s.replace('CTRL', 'SPACE_parentConstraint1')
                CND = mc.createNode('condition', n=cndName)
                mc.setAttr(CND + '.secondTerm', 1)
                mc.setAttr(CND + '.colorIfTrueR', 1)
                mc.setAttr(CND + '.colorIfFalseR', 0)
                mc.connectAttr(s + f1, CND + '.firstTerm', f=True)
                mc.connectAttr(CND + '.outColorR', conName + '.' + i1 + 'SPACEW' + b)
            elif a == 2 and len(i2) > 1:
                name = s[:j] + i2 + s[j:]
                cndName = name.replace('CTRL', 'SPACE_CND')
                conName = s.replace('CTRL', 'SPACE_parentConstraint1')
                CND = mc.createNode('condition', n=cndName)
                mc.setAttr(CND + '.secondTerm', 2)
                mc.setAttr(CND + '.colorIfTrueR', 1)
                mc.setAttr(CND + '.colorIfFalseR', 0)
                mc.connectAttr(s + f1, CND + '.firstTerm', f=True)
                mc.connectAttr(CND + '.outColorR', conName + '.' + i2 + 'SPACEW' + b)
            elif a == 3 and len(i3) > 1:
                name = s[:j] + i3 + s[j:]
                cndName = name.replace('CTRL', 'SPACE_CND')
                conName = s.replace('CTRL', 'SPACE_parentConstraint1')
                CND = mc.createNode('condition', n=cndName)
                mc.setAttr(CND + '.secondTerm', 1)
                mc.setAttr(CND + '.colorIfTrueR', 1)
                mc.setAttr(CND + '.colorIfFalseR', 0)
                mc.connectAttr(s + f1, CND + '.firstTerm', f=True)
                mc.connectAttr(CND + '.outColorR', conName + '.' + i3 + 'SPACEW' + b)
            elif a == 4 and len(i4) > 1:
                name = s[:j] + i4 + s[j:]
                cndName = name.replace('CTRL', 'SPACE_CND')
                conName = s.replace('CTRL', 'SPACE_parentConstraint1')
                CND = mc.createNode('condition', n=cndName)
                mc.setAttr(CND + '.secondTerm', 2)
                mc.setAttr(CND + '.colorIfTrueR', 1)
                mc.setAttr(CND + '.colorIfFalseR', 0)
                mc.connectAttr(s + f1, CND + '.firstTerm', f=True)
                mc.connectAttr(CND + '.outColorR', conName + '.' + i4 + 'SPACEW' + b)         
            elif a == 5 and len(i5) > 1:
                name = s[:j] + i1 + s[j:]
                cndName = name.replace('CTRL', 'SPACE_CND')
                conName = s.replace('CTRL', 'SPACE_parentConstraint1')
                CND = mc.createNode('condition', n=cndName)
                mc.setAttr(CND + '.secondTerm', 1)
                mc.setAttr(CND + '.colorIfTrueR', 1)
                mc.setAttr(CND + '.colorIfFalseR', 0)
                mc.connectAttr(s + f1, CND + '.firstTerm', f=True)
                mc.connectAttr(CND + '.outColorR', conName + '.' + i4 + 'SPACEW' + b)
            
            a = a + 1
        
def setSpaces(*arg):
    s0 = mc.textField('s0', query=True, text=True)
    s1 = mc.textField('s1', query=True, text=True)
    s2 = mc.textField('s2', query=True, text=True)
    s3 = mc.textField('s3', query=True, text=True)
    s4 = mc.textField('s4', query=True, text=True)
    s5 = mc.textField('s5', query=True, text=True)
    ov = mc.checkBoxGrp('worldOverride', query=True, v1=True)
    a1 = mc.textField('a1', query=True, text=True)
    spaceConnection(s0, s1, s2, s3, s4, s5, ov, a1)

def nickSpaceSwitch(*arg):
    #assign window names
    winName = 'spaceWin'
    winTitle = 'Space Window'
    #check if window exists
    if mc.window(winName, exists=True):
        mc.deleteUI(winName, window=True)
    #setup window
    mc.window(winName, title=winTitle, sizeable=True)
    mc.columnLayout(adjustableColumn=True)
    mc.columnLayout(adjustableColumn=True)
    #Attribute Name
    mc.frameLayout(l='Space Names', mw=4, mh=4, bgc=[0.18, 0.21, 0.25])
    mc.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,125),(2,175)])
    mc.text('Space Attribute Name:')
    mc.textField('a1', tx='follow')
    mc.setParent( '..' )
    mc.setParent( '..' )
    #Naming Layout
    mc.frameLayout(l='Space Names', mw=4, mh=4, bgc=[0.18, 0.21, 0.25])
    mc.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,50),(2,250)])
    mc.text('Space 0:')
    mc.textField('s0', tx='WORLD')
    mc.text('Space 1:')
    mc.textField('s1')
    mc.text('Space 2:')
    mc.textField('s2')
    mc.text('Space 3:')
    mc.textField('s3')
    mc.text('Space 4:')
    mc.textField('s4')
    mc.text('Space 5:')
    mc.textField('s5')
    mc.setParent( '..' )
    mc.setParent( '..' )
    #Override Checkbox
    mc.columnLayout(adjustableColumn=True)
    mc.checkBoxGrp('worldOverride', l='World Space Override')
    mc.setParent( '..' )
    mc.setParent( '..' )
    #Perform action button
    mc.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,150),(2,150)])
    mc.text('')
    mc.text(' ')
    mc.text('Select the control with the "follow" attribute, then press the button', ww=True)
    mc.button(l='Make Connections', c=setSpaces)
    mc.setParent( '..' )
    mc.setParent( '..' )
    
    mc.showWindow(winName)
    mc.window(winName, edit=True, width=200, height=210)

