#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""QtSimpleTabDialog

\author Yamauchi, Hitoshi
\file
\brief simple tab dialog"""

import sys, numpy
from PyQt4 import QtCore, QtGui

import QtGroupFrame, QtWidgetIO
import NodeListener

# QtSimpleTabDialog
class QtSimpleTabDialog(QtGui.QDialog):
    """QtSimpleTabDialog
    Simple (= one) tab widget dialog, but many tabs in the tab widget
    Most of the user interaction will be done via this dialog.

    This may be also a NodeListener. (But this has a Listener.)
    """

    #------------------------------------------------------------
    # signal: class static
    #------------------------------------------------------------

    # signal update node... connected to
    # QtSceneGraphWidget::slot_node_changed_by_dialog(object)
    # the pyqtSignal's arg is any python object here.
    # \param[in] object event object
    # \param[in] object updated scenegraph node
    # \see NodeListener
    signal_update      = QtCore.pyqtSignal(object, object)


    def __init__(self, parent=None):
        """constructor"""

        super(QtSimpleTabDialog, self).__init__(parent)

        self.setModal(False);
        self.setMinimumWidth(0);

        # main widget: tab
        self.__tab_widget     = QtGui.QTabWidget(self);

        # frame map: groupname -> Qframe (has a QtGroupFrame)
        self.__frame_map      = {}

        # group frame map: groupname -> QtGroupframe (has QIOWIdgets)
        self.__groupframe_map = {}

        # buttons: Apply, Update, OK, Close
        self.__apply_btn  = QtGui.QPushButton('Apply');
        self.__update_btn = QtGui.QPushButton('Update');
        self.__ok_btn     = QtGui.QPushButton('Ok');
        self.__close_btn  = QtGui.QPushButton('Close');

        self.__apply_btn. setDefault(False);
        self.__update_btn.setDefault(False);
        self.__ok_btn.    setDefault(False);
        self.__close_btn. setDefault(True);

        self.__button_box = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal);

        self.__button_box.addButton(self.__apply_btn,
                                    QtGui.QDialogButtonBox.ActionRole)
        self.__button_box.addButton(self.__update_btn,
                                    QtGui.QDialogButtonBox.ActionRole)
        self.__button_box.addButton(self.__ok_btn,
                                    QtGui.QDialogButtonBox.AcceptRole)
        self.__button_box.addButton(self.__close_btn,
                                    QtGui.QDialogButtonBox.RejectRole)

        # button observer
        self.__button_observer  = None

        # associated configurable object (e.g., a scnegraph node) with
        # group name
        self.__assoc_configuable_obj = {}

        # connect signals
        self.__apply_btn. pressed.connect(self.slot_apply)
        self.__update_btn.pressed.connect(self.slot_updated)
        self.__ok_btn.    pressed.connect(self.slot_ok)
        self.__close_btn. pressed.connect(self.slot_closed)

        # layout
        self.__layout = QtGui.QVBoxLayout();
        self.__layout.setObjectName('QtSimpleTabDialog')
        self.__layout.setContentsMargins(0, 0, 0, 0);
        self.__layout.addWidget(self.__tab_widget)
        self.__layout.addWidget(self.__button_box)

        self.setLayout(self.__layout);
        self.resize(420,512);

        self.__node_listener = None


    def get_groupframe_map_keys(self):
        """get groupgrame map keys.
        \return groupframe map key list.
        """
        return self.__groupframe_map.keys()


    # def get_dict(self):
    #     """get QtWidgetIO's dictionary.
    #     \return all tabs QtWidgetIO key value dictinary.
    #     """
    #     for grp_key in self.__groupframe_map.keys():
    #         gfm = self.__groupframe_map[grp_key]
    #         # print grp_key, gfm.get_dict()


    def set_dict(self, _groupname, _iowidget_key, _value):
        raise StandardError('NIN')


    def get_value(self, _groupname, _iowidget_key):
        raise StandardError('NIN')


    def set_button_observer(self, _qtwidgetio_observer):
        """set button observer.
        This replaces former set observer with _qtwidgetio_observer.
        \param[in] _qtwidgetio_observer iowidget observer.
        """
        self.__button_observer = _qtwidgetio_observer

    def set_subject_node(self, _node):
        """set subject node to this listener.
        \param[in] _node a scenegraph node to be listened.
        """
        assert(_node != None)
        assert(_node.get_subject() != None)
        self.__node_listener = \
            NodeListener.NodeListener('QtSimpleTabDialog::nodelistener',
                                      _node,
                                      self)


    def __apply_assoc_config_obj_from_gui(self):
        """apply associated (also registered) configurable objects from
        each group frames. The associated objects state will change.
        """
        for grp in self.__groupframe_map.keys():
            # set all the parameters if associated object found.
            if self.__assoc_configuable_obj[grp] != None:
                grp_dict = self.__groupframe_map[grp].get_dict()
                # print grp_dict
                self.__assoc_configuable_obj[grp].set_config_dict(grp_dict)
            else:
                print 'DEBUG: no configuable object for [' + grp + '] found.'

    def __update_assoc_config_obj_to_gui(self):
        """update GUI by associated (also registered) configurable
        objects data. The GUI is updated. No change the associated
        objects.
        """
        for grp in self.__groupframe_map.keys():
            if self.__assoc_configuable_obj[grp] != None:
                dict = self.__assoc_configuable_obj[grp].get_config_dict()
                # print dict
                self.__groupframe_map[grp].set_dict(dict)
            else:
                print 'DEBUG: no configuable object for [' + grp + '] found.'


    # slot_apply
    def slot_apply(self):
        """slot apply. Set the GUI value to the mode data.
        called when apply button is pushed."""
        print 'DEBUG: slot_apply'
        self.__apply_assoc_config_obj_from_gui()

        if self.__button_observer != None:
            self.__button_observer.update('ApplyButton')


    # slot_updated
    def slot_updated(self):
        """slot updated. Set the model data to GUI.
        called when updated button is pushed."""
        print 'DEBUG: slot_updated.'
        self.__update_assoc_config_obj_to_gui()

        if self.__button_observer != None:
            self.__button_observer.update('UpdateButton')

    # slot_ok
    def slot_ok(self):
        """slot ok.
        Called when ok button is pushed.
        Apply and close the window."""
        self.__apply_assoc_config_obj_from_gui()

        if self.__button_observer != None:
            self.__button_observer.update('OKButton')
        self.accept()

    # slot_closed
    def slot_closed(self):
        """slot closed.
        Called when close button is pushed.
        Changes are canceled and close the window."""
        if self.__button_observer != None:
            self.__button_observer.update('CloseButton')
        self.reject()


    # a signal emitted when dialog is closed
    def closed(self):
        """a signal emitted when dialog is closed"""

        # print 'called QtSimpleTabDialog::closed() '
        pass

    # emits close(), override Dialog's closeEvent
    def closeEvent(self, _close_event):
        """signal emits close(), override Dialog's closeEvent
        and call super class's closeEvent().

        \param[in] _close_event close event"""

        self.closed()
        super(QtSimpleTabDialog, self).closeEvent(_close_event)


    def add_group(self, _group_name):
        """Add a group. This means creating a new tab and called it a group.
        The added group members will be contained in a new tab.
        The group is accessed by frame with the group name.

        Internal Widget/Layout hierarchy is:
        + newTab
          +-- QFrame
              +-- QHBoxLayout
                  +-- QtGroupFrame

        \param[in] _group_name a group name to be added.
        \return the added groupframe
        """
        if self.__frame_map.has_key(_group_name) == True:
            raise StandardError(_group_name + ' has been added.')

        frame     = QtGui.QFrame()
        boxlayout = QtGui.QHBoxLayout(frame)
        boxlayout.addSpacing(10)
        frame.setLayout(boxlayout)

        groupframe = QtGroupFrame.QtGroupFrame(frame, _group_name);
        boxlayout.addWidget(groupframe);

        self.__tab_widget.addTab(frame, _group_name)

        self.__frame_map[_group_name]      = frame
        self.__groupframe_map[_group_name] = groupframe
        self.__assoc_configuable_obj[_group_name] = None

        return groupframe


    def set_associated_configuable_object(self, _groupname, _configuable):
        """set associated configurable object.

        A configurable object must have two methods:
        set_config_dict(), get_config_dict().
        We look up this object by the group name.
        \param[in] _groupname   group name, must exists
        \param[in] _configuable configurable object associated with
        _groupname
        """
        if (not (_groupname in self.__assoc_configuable_obj.keys())):
            raise StandardError('no such group [' + _groupname + '] found.')

        self.__assoc_configuable_obj[_groupname] = _configuable


    def remove_group(self, _group_name):
        """Remove a group. This means removing the tab associated
        with _group_name.
        \param[in] _group_name a group name to be removed.
        """
        if self.__frame_map.has_key(_group_name) == False:
            raise StandardError('no such group [' + _group_name + '].')

        self.__tab_widget.removeTab(
            self.__tab_widget.indexOf(self.__frame_map[_group_name]))
        del self.__frame_map[_group_name]
        del self.__groupframe_map[_group_name]
        del self.__assoc_configuable_obj[_groupname]


    def get_groupframe(self, _group_name):
        """Get a groupframe.
        \param[in] _group_name key of group frame.
        \return a QtGroupFrame associated with _group_name. None when
        no _group_name found.
        """
        return self.__groupframe_map.get(_group_name, None)


# test when called directly
if __name__ == '__main__':
    """test when called directly"""

    app = QtGui.QApplication(sys.argv)

    tab_dialog = QtSimpleTabDialog()

    gf0 = tab_dialog.add_group('testtab0')
    opt0 = {'LABEL': 'Hello'}
    gf0.add(QtWidgetIO.QtLineEditWIO(), 'myLineEdit', 'HelloWorld0', opt0)
    gf0.add(QtWidgetIO.QtComboBoxWIO(), 'myCombobox', 'Green',
            {'LABEL': 'ComboBoxExample', 'ITEMS': ['Red', 'Green', 'Blue']})
    gf0.add(QtWidgetIO.QtToggleButton(), 'myTogglebutton', False,
            {'LABEL': 'Toggle button example'})
    gf0.add(QtWidgetIO.QtColorButton(), 'myColorbutton', numpy.array([1, 0, 0, 1]),
            {'LABEL': 'ColorButton'})


    gf1 = tab_dialog.add_group('testtab1')
    opt1 = {'LABEL': 'This is for tab1.'}
    gf1.add(QtWidgetIO.QtLineEditWIO(), 'myLineEdit', 'HelloWorld1', opt1)


    # communication example.
    #   - as an Observer (QtWidgetIOObserverIF)
    #   - as an configurable object (has members: set_config_dict(), get_config_dict()
    #
    # MyConfigurableObserver has both properties.
    #
    #
    # As an observer:
    #
    #   When one of QtSimpleTabDialog's buttons is pushded, this
    #   object can observe it. Typical use case is you first derive a
    #   class from this QtWidgetIOObserverIF, and set sef to the
    #   dialog.
    #
    # As an configurable object:
    #
    #   One of QtSimpleTabDialog's buttons is pushded, then
    #   set_config_dict/get_config_dict is called associated object
    #   with the group name. and get a dictionary that contains
    #   QtWidgetIO {key, value}s.
    #
    #
    class MyConfigurableObserver(QtWidgetIO.QtWidgetIOObserverIF):
        def __init__(self):
            self.__pushd_num = {'ApplyButton': 0, 'UpdateButton': 0,
                                'OKButton': 0,    'CloseButton': 0  }

        def update(self, _arg):
            """Button observer example method"""
            num = self.__pushd_num[_arg] + 1
            print 'I observe [' + _arg + '] button is ' + str(num) + ' times pushed.'
            self.__pushd_num[_arg] = num

        def set_config_dict(self, _dict):
            """configurable example: OK. Apply."""
            print 'Set to testtab0. myLineEdit: ' + _dict['myLineEdit'] +\
                ', myCombobox: ' + _dict['myCombobox'] +\
                ', myTogglebutton: ' + str(_dict['myTogglebutton']) +\
                ', myColorbutton: '  + str(_dict['myColorbutton'])


        def get_config_dict(self):
            """configurable example: Update."""
            ret = {'myLineEdit': 'Updated text', 'myCombobox': 'Blue' }
            print 'Update to Updated text and Blue!'
            return ret

    # for testtab2, but empty
    class MyConfigurableObserver2(QtWidgetIO.QtWidgetIOObserverIF):
        def __init__(self):
            self.__pushd_num = {'ApplyButton': 0, 'UpdateButton': 0,
                                'OKButton': 0,    'CloseButton': 0  }

        def update(self, _arg):
            """Button observer example method"""
            num = self.__pushd_num[_arg] + 1
            print 'I observe [' + _arg + '] button is ' + str(num) + ' times pushed.'
            self.__pushd_num[_arg] = num

        def set_config_dict(self, _dict):
            """configurable example: OK. Apply."""
            print 'testtab1, no observer is implemented.'


        def get_config_dict(self):
            """configurable example: Update."""
            ret = {}
            return ret

    mco  = MyConfigurableObserver()
    mco2 = MyConfigurableObserver2()

    tab_dialog.set_button_observer(mco)

    # communication 2. configable object
    #
    # You can set a configuable object to associated group.
    # This is associated with testtab0.
    tab_dialog.set_associated_configuable_object('testtab0', mco)
    tab_dialog.set_associated_configuable_object('testtab1', mco2)

    # show time
    tab_dialog.open()
    s = raw_input('Push return to finish: ')
    sys.exit()
