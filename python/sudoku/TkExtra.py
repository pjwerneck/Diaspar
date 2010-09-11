#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ***************************************************************************
#  *   Copyright (C) 2008 by Pedro Werneck                                   *
#  *   pjwerneck@gmail.com                                                   *
#  *                                                                         *
#  *   This program is free software; you can redistribute it and/or modify  *
#  *   it under the terms of the GNU General Public License as published by  *
#  *   the Free Software Foundation; either version 2 of the License, or     *
#  *   (at your option) any later version.                                   *
#  *                                                                         *
#  *   This program is distributed in the hope that it will be useful,       *
#  *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#  *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#  *   GNU General Public License for more details.                          *
#  *                                                                         *
#  *   You should have received a copy of the GNU General Public License     *
#  *   along with this program; if not, write to the                         *
#  *   Free Software Foundation, Inc.,                                       *
#  *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
#  ***************************************************************************



import select
import socket
import itertools

from Tkinter import *

from errno import EINTR, EBADF, EWOULDBLOCK

class LabeledEntry(Entry):
    """An Entry with and attached label"""
    def __init__(self, master, **kw):
        fkw = {}
        lkw = {'name':'label'}
        skw = {'side':'left', 'padx':0, 'pady':0}

        fmove = ('name',)
        lmove = ('text', 'textvariable', 'anchor')
        smove = ('side', 'padx', 'pady', 'expand', 'fill')

        for k in kw.keys():
            if k in fmove:
                fkw[k] = kw[k]
                del kw[k]
            elif k in lmove:
                lkw[k] = kw[k]
                del kw[k]
            elif k in smove:
                skw[k] = kw[k]
                del kw[k]
            elif k == 'side':
                side = kw['side']
                del kw['side']
                
        self.body = Frame(master, **fkw)
        self.label = Label(self.body, **lkw)
        self.label.pack(side='left')
        Entry.__init__(self, self.body, **kw)
        self.pack(**skw)



        methods = (Pack.__dict__.keys() +
                   Grid.__dict__.keys() +
                   Place.__dict__.keys())              
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.body, m))        
        


class Notebook(Frame):
    
    def __init__(self, *args, **kwds):
        Frame.__init__(self, *args, **kwds)
        self.tabs = []
        self.frames = []
        self.current_frame = None
        self.cover = None
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback

    def set_frames(self, *frames):
        self.buttonsframe = Frame(self)
        self.emptyframe = Frame(self)
        
        for name, frame in frames:
            self._add_new_frame(name, frame)

        height = sum(x.winfo_reqheight() for x in self.tabs)/len(self.tabs)
        self.buttonsframe['height'] = height - 3
        width = sum(x.winfo_reqwidth() for x in self.tabs)
        self.buttonsframe['width'] = width
        
        self.buttonsframe.pack(anchor=NW, padx=1, pady=0)

        self.cover = Frame(self, height=1)
        self.change_frame(0)
    
    def _add_new_frame(self, name, frame):
        if frame is None:
            frame = self.emptyframe

        self.frames.append(frame)

        i = len(self.tabs)
        
        def command():
            self.change_frame(i)

        tab = Button(self.buttonsframe, text=name, bd=1, command=command,
                     width=10)
        curwidth = sum(b.winfo_reqwidth()-3 for b in self.tabs)
        tab.place(relx=0.0, x=curwidth)

        #tab.bind('<Enter>', self._enter)
        #tab.bind('<Leave>', self._leave)

        self.tabs.append(tab)

    def _enter(self, event=None):
        i = self.tabs.index(event.widget)
        
    def _leave(self, event=None):
        i = self.tabs.index(event.widget)

    def change_frame(self, i):
        for tab in self.tabs[:i]:
            tab.lower()
            tab['bg'] = 'gray'
        for tab in self.tabs[i+1:]:
            tab.lower()
            tab['bg'] = 'gray'
        
        tab = self.tabs[i]
        tab.lift()
        tab['bg'] = '#d9d9d9'

        if self.current_frame is not None:
            self.current_frame.forget()
        frame = self.current_frame = self.frames[i]
        frame.pack(expand=1, fill=BOTH, padx=2, pady=0)

        self.cover['width'] = tab.winfo_reqwidth()-4
        self.cover.place(anchor=S, relx=0.5, rely=1.0, in_=tab)
        if self.callback is not None:
            self.callback(i)
        
        
class MultiListbox(Frame):
    def __init__(self, master, lists, **kw):
        Frame.__init__(self, master)

        self.lists = []
        self.headers = []
        bopts = dict(bd=2, relief=RIDGE, height=1)
        fopts = dict(orient=VERTICAL)

        self.panel = panel = PanedWindow(self, showhandle=0, sashpad=0,
                                         opaqueresize=0)
        panel.pack(expand=1, fill=BOTH, side=LEFT)
        
        for i, (text, width) in enumerate(lists):
            frame = Frame(self)
            panel.add(frame, sticky=N+S+E+W)

            header = Button(frame, text=text, bd=2,  relief=RIDGE,
                            height=1,
                            command=lambda i=i:self._sort_column(i))
            header.pack(fill=X)
            self.headers.append(header)

            
            listbox = Listbox(frame, width=width, borderwidth=0,
                         selectborderwidth=0, exportselection=FALSE, **kw)
            
            listbox.pack(expand=YES, fill=BOTH)
            self.lists.append(listbox)

            #Events
            listbox.bind('<B1-Motion>', self._select)
            listbox.bind('<B2-Motion>', self._b2motion)
            listbox.bind('<Button-1>', self._select_single)
            listbox.bind('<Control-Button-1>', self._select)
            listbox.bind('<Button-2>', self._button2)

            listbox.bind('<Button-4>', self._wheelscroll)
            listbox.bind('<Button-5>', self._wheelscroll)
            listbox.bind('<Leave>', lambda e: 'break')
            
        scroll = Scrollbar(self, orient=VERTICAL, command=self._scroll,
                           width=12, bd=1)
        scroll.pack(expand=0, fill=Y, side=RIGHT)
        listbox['yscrollcommand'] = scroll.set

        self._last_selected = None
        self._sorted_by = None

    def bind(self, event, action):
        for listbox in self.lists:
            listbox.bind(event, action)

    def _select_single(self, event):
        y = event.y
        state = event.state
        row = self.lists[0].nearest(y)
            
        self.selection_clear(0, END)
        self.selection_set(row)

        return 'break'

    def _select(self, event):
        y = event.y
        state = event.state
        row = self.lists[0].nearest(y)
        if state == 272:
            if row == self._last_selected:
                return 'break'
            
        if self.selection_includes(row):
            self.selection_clear(row)
            self._last_selected = row
        else:
            self.selection_set(row)
            self._last_selected = row
        return 'break'

    def _button2(self, event):
        x, y = event.x, event.y
        for l in self.lists: l.scan_mark(x, y)
        return 'break'

    def _b2motion(self, event):
        x, y = event.x, event.y
        for l in self.lists: l.scan_dragto(x, y)
        return 'break'

    def _wheelscroll(self, event):
        button = event.num
        a = -(9 - 2*button)
        for l in self.lists:
            l.yview(SCROLL, a, UNITS)
        return 'break'

    def _scroll(self, *args):
        for l in self.lists:
            l.yview(*args)
        return 'break'

    def _sort_column(self, column):
        header = self.headers[column]
        
        #save current selection
        self.curselection()
        size = self.size()
        selected = [False for x in xrange(size)]
        for x in self.curselection():
            selected[int(x)] = True

        # get data
        data = self.get(0, END)

        # no data, no need to sort...
        if not data:
            return

        col = zip(*data)[column]
        decorated = zip(col, data, selected)

        # sort all lists by this column. If it's already sorted by
        # this column, revert it
        if self._sorted_by == column:
            decorated.reverse()
            if header["relief"] == SUNKEN:
                header["relief"] = RAISED
            elif header["relief"] == RAISED:
                header["relief"] = SUNKEN

        else:
            decorated.sort()
            header["relief"] = SUNKEN
            
            if self._sorted_by is not None:
                self.headers[self._sorted_by]["relief"] = RIDGE

        self._sorted_by = column
        
        col, final, selected  = zip(*decorated)

        # delete all items and reinsert sorted
        self.delete(0, END)
        self.insert(0, *final)

        # restore selectioon
        selected = list(selected)
        i = 0
        while 1:
            try:
                x = selected.index(True, i)
                self.selection_set(x)
                i = x+1
                    
            except ValueError:
                break
            
    def curselection(self):
        return self.lists[0].curselection()

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    def get(self, first, last=None):
        result = [l.get(first, last) for l in self.lists]
        if last:
            result = map(None, *result)
        return result
            
    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, *elements):
        data = zip(*elements)
        for i, l in enumerate(self.lists):
            l.insert(index, *data[i])

    def move(self, source, dest):
        data = self.get(source)
        self.delete(source)
        self.insert(dest, data)

    def swap(self, x, y):
        datax = self.get(x)
        datay = self.get(y)
        self.delete(x)
        self.insert(x, datay)
        self.delete(y)
        self.insert(y, datax)

    def size(self):
        return self.lists[0].size()

    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)

    def setstate(self, state):
        for l in self.lists:
            l['state'] = state
        for h in self.headers:
            h['state'] = state

    


class ScrolledListbox(Listbox):
    def __init__(self, master, **kw):
        fkw = {}
        for k in kw.keys():
            if k == 'name':
                fkw[k] = kw[k]
                del kw[k]
        self.body = Frame(master, **fkw)
        self.vbar = Scrollbar(self.body, name='vbar', width=12, bd=1)
        self.vbar.pack(side='right', fill='y')
        Listbox.__init__(self, self.body, **kw)
        self.pack(side='left', fill='both', expand=1)
        self['yscrollcommand'] = self.vbar.set
        self.vbar['command'] = self.yview
                
        methods = (Pack.__dict__.keys() +
                   Grid.__dict__.keys() +
                   Place.__dict__.keys())
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.body, m))


class ButtonBar(Frame):
    """A ButtonBar

    ButtonBar.buttons > dictionary with all the widgets"""

    def __init__(self, master, **kw):
        """Standard Frame widget options"""
        self.buttons = {}
        self.checkboxes = {}
        self.variables = {}
        self.count = 0
        Frame.__init__(self, master, **kw)
        
    def add_button(self, name, **kw):
        """Standard Button widget options. You may provide
        an additional side argument to be applied to the
        pack function. It defaults to LEFT.

        add_button(name, **kw)"""
        pkw = {'side':'left'}
        if 'side' in kw:
            pkw['side'] = kw['side']
        kw['relief'] = FLAT
        self.buttons[name] = button = Button(self, **kw)
        button.bind('<Enter>', self._button_enter)
        button.bind('<Leave>', self._button_leave)
        
        self.buttons[name].pack(**pkw)

    def add_spinbox(self, name, **kw):
        pkw = {'side':'left'}
        if 'side' in kw:
            pkw['side'] = kw['side']
        
        self.buttons[name] = box = Spinbox(self, **kw)
        self.buttons[name].pack(**pkw)

    def add_entry(self, name, **kw):
        pkw = {'side':'left'}
        if 'side' in kw:
            pkw['side'] = kw['side']
        
        self.buttons[name] = Entry(self, **kw)
        self.buttons[name].pack(**pkw)
        

    def _button_enter(self, event=None):
        if event.widget['state'] != DISABLED:
            event.widget['relief'] = RAISED

    def _button_leave(self, event=None):
        #if event.widget['state'] != DISABLED:
        event.widget['relief'] = FLAT

    def add_checkbox(self, name, **kw):
        """Standard Checkbox widget options. You may provide
        an additional side argument to be applied to the
        pack function. It defaults to LEFT.

        A intvariable with the same name is added to the variables
        dictionary if not passed

        add_button(name, **kw)"""
        pkw = {'side':'left'}
        if 'side' in kw:
            pkw['side'] = kw['side']

        if 'variable' not in kw:
            kw['variable'] = self.variables[name] = IntVar()
            
        self.buttons[name] = Checkbutton(self, **kw)
        self.buttons[name].pack(**pkw)

    def add_separator(self, **kw):
        """Add a 1 pixel spacer, or

        Standard Label widget options. The padx and pady
        options are applied to the pack geometry manager,
        not to the Label. As in add_button, you may provide
        a side option.
        If you just need a simple separator, just give an width
        option with a negative size in pixels, ex: width=-1,
        will insert a 1 pixel spacer,

        add_separator()
        add_separator(**kw)"""
        pkw = {'side':'left', 'padx':0, 'pady':0}
        name = self.count
        if not kw:
            self.buttons[name] = Label(self, width=-1)
            self.buttons[name].pack(**pkw)
        else:
            for k in kw.keys():
                if k in pkw:
                    pkw[k] = kw[k]
                    del kw[k]
            self.buttons[name] = Label(self, **kw)
            self.buttons[name].pack(**pkw)
        self.count += 1

    def delete(self, id):
        """Delete an slave, button or label. By it's name, if it's
        a button or by it's index if it's a label

        delete(id)"""
        button = self.buttons[id]
        button.pack_forget()
        button.destroy()
        del self.buttons[id], button

class StatusBar(Label):
    """
    A StatusBar widget is just like a Label widget, but have an
    internal StringVar in case a textvariable is not supplied and
    methods to control timeout and priority of text.

    StatusBar.default  -> Default message ('text' option)
    StatusBar.clock    -> Alarm id of current message.
    StatusBar.priority -> Priority of current message
    """

    def __init__(self, master, **kw):
        """
        Construct a StatusBar widget with the parent MASTER.
       
        Valid resource names: anchor, background, bd, bg,
        borderwidth, cursor, fg, font, foreground, height,
        justify, padx, pady, relief, takefocus, text,
        underline, width, wraplength.
        """
        if kw:
            for k in ('image', 'bitmap'):
                if k in kw:
                    raise KeyError, "StatusBar doesn't accept a %s option" % (k,)

            if not 'anchor' in kw:
                kw['anchor'] = 'w'

            if 'textvariable' in kw:
                self.current = kw['textvariable']
            else:
                self.current = StringVar()
                kw['textvariable'] = self.current

            if 'text' in kw:
                self.default = kw['text']
                del kw['text']
            else:
                self.default = ''

        kw['relief'] = SUNKEN
            
        self.current.set(self.default)
        self.clock = None
        self.priority = None

        Label.__init__(self, master, **kw)

    def set(self, text, timeout=None, priority=None, beep=None):
        """
        set(text[, timeout[, priority[, beep]]])

        Display 'text' for 'timeout', if 'priority' is higher or equal
        than the 'priority' of current message. Default message priority
        is None.

        Beep once if beep is true.
        
        """
        if not isinstance(text, str):
            text = str(text)
        if priority >= self.priority:
            if beep:
                self.bell()
            if self.clock is not None:
                self.after_cancel(self.clock)
                self.clock = None
            self.current.set(text)
            self.priority = priority
            if isinstance(timeout, (int, float)):
                self.clock = self.after(int(timeout * 1000), self.reset)
            elif timeout is None:
                    self.clock = None
            else:
                raise TypeError, "timeout should be 'int', 'float' or None"

    def reset(self):
        """resets the statusbar to the default state"""
        self.current.set(self.default)
        self.priority, self.clock = None, None


    


### Select mix in


_read  = {}
_write = {}
_error = {}

_modes = [_read, _write, _error]
_select = select.select

_tags = itertools.count()

INPUT_READ = 0
INPUT_WRITE = 1
INPUT_EXCEPTION = 2

class _Wrapper(object):
    
    def __init__(self, source, callback):
        self.source = source
        self.fileno = source.fileno
        self.close = source.close
        self.callback = callback

class TkSelectMixIn:

    def input_add(self, source, mode, callback):

        if mode not in (0, 1, 2):
            raise ValueError("invalid mode")

        tag = _tags.next()
        _modes[mode][tag] = _Wrapper(source, callback)

        return tag

    def input_remove(self, tag):
        for mode in _modes:
            if tag in mode:
                mode.pop(tag)
                break

    def _check(self):
        for mode in _modes:
            remove = []
            for tag, source in mode.iteritems():
                try:
                    _select([source], [source], [source], 0)
                except:
                    remove.append(tag)
                    source.close()
            for tag in remove:
                mode.pop(tag)
        
    def _select(self,
              _read=_read,
              _write=_write,
              _error=_error,
              _select=_select):

        if not _read:
            self.after(100, self._select)
            return

        while 1:

            try:
                ready = _select(_read.values(), _write.values(),
                                _error.values(), 0)
                break
            except ValueError:
                print 'value error'
                self._check()
            except TypeError:
                print 'type erro'
                self._check()
            except socket.error, reason:
                print 'socket error', reason
                code, msg = reason.args
                if code == EINTR:
                    return
                if code == EBADF:
                    self._check()
                else:
                    raise

        for condition, mode in enumerate(ready):
            for source in mode:
                source.callback(source.source, condition)

        self.after(100, self._select)
        
    def start(self):
        self.after(100, self._select)


