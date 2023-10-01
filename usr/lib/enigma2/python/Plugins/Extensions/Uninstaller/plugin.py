#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryPixmapAlphaTest
from Components.MultiContent import MultiContentEntryText
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.Screen import Screen
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from enigma import RT_HALIGN_LEFT, RT_VALIGN_CENTER
from enigma import eListboxPythonMultiContent
from enigma import eTimer, getDesktop
from enigma import loadPNG, gFont
import os
global cmdx
cmdx = 'opkg list_installed | grep enigma2-plugin > /tmp/ipkdb 2>&1 &'
myfile = '/tmp/ipkdb'
version = '1.0'
# dpkg -l | grep g
# apt list --installed
# apt-get remove
# dpkg -r $paketname
screenwidth = getDesktop(0).size()


def main(session, **kwargs):
    session.open(Uninstaller)


def Plugins(**kwargs):
    return PluginDescriptor(name=_("Uninstaller"), description=_("Choose and uninstall an addon package"), where=PluginDescriptor.WHERE_PLUGINMENU, icon="icon.png", fnc=main)


class packList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        if screenwidth.width() == 2560:
            self.l.setItemHeight(60)
            textfont = int(48)
            self.l.setFont(0, gFont('Regular', textfont))
        elif screenwidth.width() == 1920:
            self.l.setItemHeight(45)
            textfont = int(32)
            self.l.setFont(0, gFont('Regular', textfont))
        else:
            self.l.setItemHeight(45)
            textfont = int(24)
            self.l.setFont(0, gFont('Regular', textfont))


def pakage_entry(name):
    res = [name]
    pngs = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/pic.png".format('Uninstaller'))
    if screenwidth.width() == 2560:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 15), size=(30, 30), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(80, 0), size=(1200, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    elif screenwidth.width() == 1920:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 8), size=(30, 30), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(70, 0), size=(1000, 42), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(3, 5), size=(30, 30), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(50, 0), size=(1000, 40), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res


class Uninstaller(Screen):
    skin = '''
            <screen name="Uninstaller" position="center,center" size="1220,600" title="Uninstaller by Lululla">
                <widget name="list" position="10,66" size="1200,500" scrollbarMode="showOnDemand" zPosition="2" />
                <widget name="info" position="11,5" zPosition="4" size="1193,55" font="Regular; 32" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />
            </screen>
            '''

    if screenwidth.width() == 2560:
        skin = '''
                <screen name="Uninstaller" position="center,center" size="1980,1200" title="Uninstaller by Lululla">
                    <widget name="list" position="30,156" size="1900,1000" scrollbarMode="showOnDemand" zPosition="2" />
                    <widget name="info" position="11,5" zPosition="4" size="1937,123" font="Regular; 54" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />
                </screen>
                '''

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skin = Uninstaller.skin
        title = 'Uninstaller v.%s by Lululla' % version
        self.setTitle(title)
        self['list'] = packList([])
        self['info'] = Label()
        self['actions'] = ActionMap(['OkCancelActions'], {'ok': self.okClicked,
                                                          'cancel': self.close}, -1)
        txt = _('Wait Please...')
        self['info'].setText(txt)
        self.timerw = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timerw_conn = self.timerw.timeout.connect(self.UploadList)
        else:
            self.timerw.callback.append(self.UploadList)
        self.timerw.start(100, 1)
        # self.onShown.append(self.UploadList)

    def UploadList(self):
        if os.path.exists(myfile):
            os.remove(myfile)
        self.list = []
        # del self.list[:]
        # for x in self.list:
            # print('xxxx= ', x)
            # del self.list[0:x]
        self.delay()
        os.system('sleep 5')
        if os.path.exists(myfile):
            with open(myfile) as file_:
                for line in file_:
                    if line.startswith('enigma2-plugin-'):
                        line = str(line)
                        print(line)
                    self.list.append(pakage_entry(line[:-1]))
                # self.list.sort()
            if len(self.list) > -1:
                self.list.sort(key=lambda x: x, reverse=False)
                # self["list"].list = self.list
                self["list"].setList(self.list)
                txt = _('Please Select the Package to Remove')
                self['info'].setText(txt)
            else:
                txt = _('Please advise on forum board for issue!')
                self['info'].setText(txt)                
        else:
            txt = _('Error Unknow')
            self['info'].setText(txt)
        '''
        # if os.path.exists('/var/volatile/tmp/ipkdb'):
            # with open('/tmp/ipkdb') as file_:
                # for line in file_:
                    # line = str(line)
                    # print(line)
                    # self.list.append(pakage_entry(line[:-1]))
            # file_.close()
            # self.list.sort()
            # self['list'].setList(self.list)
            # txt = _('Please Select the Package to Remove')
            # self['info'].setText(txt)
        # else:
            # txt = _('Error Unknow')
            # self['info'].setText(txt)
        '''

    def delay(self):
        global cmdx
        path = ('/var/lib/opkg/info')
        if os.path.exists(myfile):
            os.remove(myfile)
        if os.path.exists('/var/lib/dpkg/info'):
            # cmdx = 'dpkg -l | grep enigma2-plugin > /tmp/ipkdb 2>&1 &'
            # cmdx = 'apt list --installed > /tmp/ipkdb 2>&1 &'
            path = ('/var/lib/dpkg/info')
            
        # else:
            # path = ('/var/lib/opkg/info')
        with open(myfile, 'w') as f:
            for root, dirs, files in os.walk(path):
                if files is not None:
                    for name in files:
                        if name.startswith('enigma2-plugin') and name.endswith('.list'):
                            print(str(name))
                            name = name.replace('.list', '')
                            f.write(str(name) + '\n')
            f.close()
            
            
        # else:
            # cmdx = 'opkg list_installed | grep enigma2-plugin > /tmp/ipkdb 2>&1 &'
            # file_ = os.popen(cmdx).read()
            # with open(myfile, 'w') as f:
                # f.write(file_)
                # f.seek(0)
                # f.close()
        return

    def okClicked(self):
        ires = self['list'].getSelectionIndex()
        print('ires 1: ', ires)
        if ires is not None:
            self.ipk = self.list[ires][0]
            print('self.ipk 1: ', self.ipk)
            # n1 = self.ipk.find('_', 0)
            # self.ipk = self.ipk[:n1]
            self.session.openWithCallback(self.test, ChoiceBox, title=_('Select method:'), list=[(_('Remove'), 'rem'), (_('Force Remove'), 'force')])
        else:
            return
        return

    def test(self, answer):
        try:
            cmd = ' '
            title = ' '
            add = str(self.ipk)
            if answer[1] == 'rem':
                if os.path.exists('/var/lib/dpkg/info'):
                    cmd = 'apt-get purge --auto-remove --assume-yes ' + add
                    title = _('Removing dpkg %s' % add)
                else:
                    cmd = 'opkg remove ' + add
                    title = _('Removing ipk %s' % add)
            elif answer[1] == 'force':
                if os.path.exists('/var/lib/dpkg/info'):
                    cmd = 'dpkg -r --force-depends ' + add
                    title = _('Removing dpkg %s' % add)
                else:
                    cmd = 'opkg remove --force-depends ' + add
                    title = _('Force Removing ipk %s' % add)
            self.session.open(Console, _(title), [cmd])
            self.close()
        except Exception as e:
            print('error ', e)
            self.close()
