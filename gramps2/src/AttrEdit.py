#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2000  Donald N. Allingham
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
The AttrEdit module provides the AddressEditor class. This provides a
mechanism for the user to edit address information.
"""

__author__ = "Donald N. Allingham"
__version__ = "$Revision$"

#-------------------------------------------------------------------------
#
# GTK/Gnome modules
#
#-------------------------------------------------------------------------
import gtk.glade

#-------------------------------------------------------------------------
#
# gramps modules
#
#-------------------------------------------------------------------------
import const
import Utils
import Sources
import AutoComp

from RelLib import Attribute

from intl import gettext as _

#-------------------------------------------------------------------------
#
# AttributeEditor class
#
#-------------------------------------------------------------------------
class AttributeEditor:
    """
    Displays a dialog that allows the user to edit an attribute.
    """
    def __init__(self,parent,attrib,title,list):
        """
        Displays the dialog box.

        parent - The class that called the Address editor.
        attrib - The attribute that is to be edited
        title - The title of the dialog box
        list - list of options for the pop down menu
        """

        self.parent = parent
        self.attrib = attrib
        self.top = gtk.glade.XML(const.dialogFile, "attr_edit")
        self.window = self.top.get_widget("attr_edit")
        self.type_field  = self.top.get_widget("attr_type")
        self.slist  = self.top.get_widget("slist")
        self.value_field = self.top.get_widget("attr_value")
        self.note_field = self.top.get_widget("attr_note")
        self.attrib_menu = self.top.get_widget("attr_menu")
        self.source_field = self.top.get_widget("attr_source")
        self.priv = self.top.get_widget("priv")
        
        if attrib:
            self.srcreflist = self.attrib.getSourceRefList()
        else:
            self.srcreflist = []

        self.sourcetab = Sources.SourceTab(self.srcreflist,self.parent,self.top,
                                           self.slist,
                                           self.top.get_widget('add_src'),
                                           self.top.get_widget('del_src'))

        title = _("Attribute Editor for %s") % title
        self.top.get_widget("attrTitle").set_text(title)

        AutoComp.AutoEntry(self.attrib_menu.entry,list)

        if attrib != None:
            self.type_field.set_text(attrib.getType())
            self.value_field.set_text(attrib.getValue())
            self.priv.set_active(attrib.getPrivacy())

            self.note_field.get_buffer().set_text(attrib.getNote())

        self.top.signal_autoconnect({
            "destroy_passed_object" : Utils.destroy_passed_object,
            "on_attr_edit_ok_clicked" : self.on_ok_clicked,
            "on_add_src_clicked" : self.add_source,
            "on_del_src_clicked" : self.del_source,
            })

    def add_source(self,obj):
        pass

    def del_source(self,obj):
        pass

    def on_ok_clicked(self,obj):
        """
        Called when the OK button is pressed. Gets data from the
        form and updates the Attribute data structure.
        """
        type = self.type_field.get_text()
        value = self.value_field.get_text()

        buf = self.note_field.get_buffer()
        note = buf.get_text(buf.get_start_iter(),buf.get_end_iter(),gtk.FALSE)
        priv = self.priv.get_active()

        if self.attrib == None:
            self.attrib = Attribute()
            self.parent.alist.append(self.attrib)

        self.attrib.setSourceRefList(self.srcreflist)
        self.update(type,value,note,priv)
        
        self.parent.redraw_attr_list()
        Utils.destroy_passed_object(obj)

    def check(self,get,set,data):
        """Compares a data item, updates if necessary, and sets the
        parents lists_changed flag"""
        if get() != data:
            set(data)
            self.parent.lists_changed = 1
            
    def update(self,type,value,note,priv):
        """Compares the data items, and updates if necessary"""
        ntype = const.save_pattr(type)
        self.check(self.attrib.getType,self.attrib.setType,ntype)
        self.check(self.attrib.getValue,self.attrib.setValue,value)
        self.check(self.attrib.getNote,self.attrib.setNote,note)
        self.check(self.attrib.getPrivacy,self.attrib.setPrivacy,priv)

