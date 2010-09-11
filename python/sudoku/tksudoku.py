
import random
import pickle
import Tkinter
import TkExtra
from Tkconstants import *
import datetime
import itertools
import math


LIGHT = '#ebebff'
DARK = '#d8d8ff'
SELECT = '#ffbbbb'
HIGHLIGHT = '#bbffbb'
TEXT = '#488ecf'
READONLY = '#48a08e'
GIVEN = '#222222'
WRONG = '#ff0000'

BLACK = '#000000'

RED = '#ff4444'
YELLOW = '#ffff88'
PURPLE = '#ff88ff'
GREEN = '#88ff88'
LBLUE = '#88ffff'
BLUE = '#8888ff'



class History(object):
    def __init__(self):
        self.stack_low = []
        self.stack_top = []

    def push(self, state):
        #if equal to current state, do nothing
        try:
            if state == self.stack_low[-1]:
                return
        except IndexError:
            pass
        self.stack_low.append(state)
        del self.stack_top[:]

    def undo(self):
        try:
            state = self.stack_low.pop()
        except IndexError:
            return
        
        try:
            self.stack_top.insert(0, state)
        except IndexError:
            self.stack_top.append(state)

        try:
            return self.stack_low[-1]
        except IndexError:
            return

    def redo(self):
        try:
            state = self.stack_top.pop(0)
        except IndexError:
            return

        self.stack_low.append(state)

        return state

    def reset(self):
        del self.stack_low[:]
        del self.stack_top[:]


class ColorDialog(object):
    def __init__(self, board, cell, event):
        self.board = board
        self.cell = cell
        self.event = event

    def draw(self):
        cellsize = (self.cell.bbox[2] - self.cell.bbox[0])
        w, h = self.board.size

        x, y = self.event.x, self.event.y

        # build the box for the color dialog
        x0 = x
        x1 = x + cellsize*3
        y0 = y
        y1 = y + cellsize*2.5
        # if it overpasses the right border, change to left side
        if x1 > w:
            x0 = x - cellsize*3
            x1 = x
        # if it overpasses the bottom border, change to upside
        if y1 > h:
            y0 = y - cellsize*2.5
            y1 = y
            
        bbox = x0, y0, x1, y1
        
        self.board.create_rectangle(bbox, fill='white', tag='color_box')

        colors = [RED, YELLOW, GREEN, LBLUE, BLUE, PURPLE]
        coords = [(a, b) for a in (0, 1, 2) for b in (0, 1)]

        diff = cellsize*0.95
        
        # create the color boxes
        for color, (a, b) in zip(colors, coords):
            a0 = x0 + a*cellsize + diff
            a1 = x0 + (a+1)*cellsize - diff
            b0 = y0 + b*cellsize + diff
            b1 = y0 + (b+1)*cellsize - diff

            cbox = (a0, b0, a1, b1)
            rect = self.board.create_rectangle(cbox, fill=color,
                                               tag=('color_frame', color))
            self.board.tag_bind(rect, '<Button-1>', self.cb_chosen_color)

        # create the cancel label centered at bottom
        x = x0 + cellsize * 1.5
        y = y0 + cellsize * 2.2
        fontsize = int(cellsize/4)
        self.board.create_text((x, y), text='Cancel', fill='blue',
                               font=('Arial', fontsize, 'underline'),
                               tag=('color_frame', 'cancel_button'))

    def cb_click_left(self, event):
        self.board.delete('color_box')
        self.board.delete('color_frame')
        self.board.dialog = None

    def cb_chosen_color(self, event):
        x, y = event.x, event.y
        tag = self.board.find_closest(x, y)
        fill = self.board.itemcget(tag, 'fill')
        if fill:
            self.cell.color = fill
        else:
            print self.board.itemcget(tag, 'text')


class PopUpMenu(object):
    def __init__(self, board, event):
        self.board = board
        self.event = event

    def draw(self):
        w, h = self.board.size

        x, y = self.event.x, self.event.y

        x0 = x
        x1 = x+w/10
        y0 = y
        y1 = y+h/10

        # if it overpasses the right border, change to left side
        if x1 > w:
            x0 = x - w/10
            x1 = x
        # if it overpasses the bottom border, change to upside
        if y1 > h:
            y0 = y - h/10
            y1 = y      


class PencilMarks(object):
    def __init__(self):
        self.current = None

    def __repr__(self):
        cell = self.current
        marks = []
        for i, v in enumerate(cell.marks):
            if cell.board.itemcget(v, 'state') == NORMAL:
                marks.append(i+1)
        return 'marks(%s)'%marks

    def __get__(self, cell, owner):
        self.current = cell
        return self

    def __set__(self, cell, values):
        self.current = cell
        if cell.value:
            # cell has a value, can't set marks
            return

        marks = 0
        
        for v in range(1, 10):
            s = str(v)
            if s in map(str, values):
                marks |= 2**v
                cell.board.itemconfig(cell.marks[v-1], state=NORMAL)
            else:
                cell.board.itemconfig(cell.marks[v-1], state=HIDDEN)

        cell._marks = marks
        

    def set_color(self, v, color):
        cell = self.current
        i = int(v) -1
        cell.board.itemconfig(cell.marks[i], fill=color)

    def __int__(self):
        return self.current._marks

    def __contains__(self, item):
        try:
            len(item)
            for v in item:
                if not self[str(v)]:
                    return False
            return True
        except TypeError:
            return self[str(v)]
            
    def __getitem__(self, i):
        cell = self.current
        if cell._marks &(2 ** int(i)):
            return True
        return False

    def __setitem__(self, i, v):
        cell = self.current
        i = int(i)
        j = i-1
        if v:
            cell._marks |= 2**i
            cell.board.itemconfig(cell.marks[j], state=NORMAL)
        else:
            if cell._marks & 2**i:
                cell._marks ^= 2**i
                cell.board.itemconfig(cell.marks[j], state=HIDDEN)
                

    def __delete__(self, cell):
        cell._marks = 0
        for i in range(9):
            cell.board.itemconfig(cell.marks[i], state=HIDDEN)

    def toggle(self, i):
        
        if self[i]:
            self[i] = False
        else:
            self[i] = True
            
    def get_all(self):
        return [str(i) for i in range(1, 10) if self[i]]


class Cell(object):
    pencil = PencilMarks() # a descriptor to manage pencil marks
    def __init__(self, board, row, col):
        # canvas
        self.board = board
        
        # Tags
        # rectangle
        self._rect = None
        # text
        self._text = None
        # pencil marks
        self.marks = [None]*9

        # Values
        self._value = 0
        self._marks = 0
        
        # box coords, (x0, y0, x1, y1)
        self.row = row
        self.col = col
        self.bbox = None
        self.solution = None

        # selected?
        self._selected = False

        # original fill color
        self.fill = None
        
        self._highlight = False
        self._color = None

        self._readonly = False
        self.given = False

        # hint active on this cell?
        self.hint_active = False

    def __repr__(self):
        value = self.value if self.value else ''.join(self.pencil.get_all())
        return '(r%sc%s=%s)'%(self.row+1, self.col+1, value)

    def __str__(self):
        return 'r%sc%s'%(self.row+1, self.col+1)

    def __iter__(self):
        if self.value:
            return iter([])

        return iter(self.pencil.get_all())

    def __len__(self):
        return len(self.pencil.get_all())

    def __int__(self):
        # return a bit-wise representation of the pencil marks
        return int(self.pencil)

    def get_wrong(self):
        # return True if current value is wrong
        if not self.value:
            return False
        else:
            return self.value != self.solution
        
    wrong = property(get_wrong)

    def get_row(self):
        # return all cells sharing the same row
        row = [self.board.cells[self.row*9 + col] for col in range(9)]
        return row

    def get_col(self):
        # return all cells sharing the same col
        col = [self.board.cells[row*9 + self.col] for row in range(9)]
        return col

    def get_box(self):
        # return all cells sharing the same box
        box = []
        x = self.col / 3
        y = self.row / 3

        for row in range(y*3, y*3 + 3):
            for col in range(x*3, x*3 + 3):
                other = self.board.cells[row*9 + col]
                box.append(other)
        return box

    def candidates(self):
        others = []
        if self.value:
            return others
        others.extend([other.value for other in self.get_row() if other.value])
        others.extend([other.value for other in self.get_box() if other.value])
        others.extend([other.value for other in self.get_col() if other.value])

        others = set(others)
        marks = set(map(str, range(1, 10))) - others
        
        return list(marks)

    def intersect(self, other):
        if self.value:
            return []
        if other.value:
            return []
        my_marks = set(self.pencil.get_all())
        other_marks = set(other.pencil.get_all())
        return list(my_marks.intersection(other_marks))

    def draw(self, cellsize, origin):
        margin = cellsize / 2
        row = self.row
        col = self.col
        ox, oy = origin

        cs = cellsize
        df = cs*0.98

        bbox = x0, y0, x1, y1 = (ox + margin - df + (col + 1)*cs,
                                 oy + margin - df + (row + 1)*cs,
                                 ox + margin + df + col*cs,
                                 oy + margin + df + row*cs)
        
        # rectangle
        if self._rect is None:
            # find quarter color
            quarter = (row/3, col/3)
            if abs(quarter[1]-quarter[0]) in (2, 0):
                self.fill = LIGHT
            else:
                self.fill = DARK
            # initial draw
            self._rect = self.board.create_rectangle(*bbox,
                                                     fill=self.fill,
                                                     tags=('rect',
                                                           'rect_%s'%self))
        else:
            # redraw
            self.board.coords(self._rect, bbox)

        # text
        center = (bbox[0]+cs/2, bbox[1]+cs/2)
        fontsize = int(cs*0.8)

        if self._text is None:
            self._text = self.board.create_text(*center, text='',
                                               font=('Arial', fontsize))
        else:
            self.board.coords(self._text, center)
            self.board.itemconfig(self._text, font=('Arial', fontsize))

        # pencil marks
        pencilsize = cellsize / 3
        pencilfontsize = fontsize/3
        for i,(a, b) in enumerate([(a, b) for b in (0,1,2) for a in (0,1,2)]):
            x = x0 + pencilsize*a + pencilsize/2
            y = y0 + pencilsize*b + pencilsize/2
            if self.marks[i] is None:
                self.marks[i] = self.board.create_text(
                    x, y, text=str(i+1),
                    fill='black',
                    font=('Arial', pencilfontsize),
                    state=HIDDEN,
                    tags=('pencilmark',
                          'pencilmark_%s_%s_%s'%(row+1, col+1, i+1)
                          ),
                    )
            else:
                self.board.itemconfig(
                    self.marks[i], font=('Arial', pencilfontsize)
                    )
                self.board.coords(self.marks[i], (x, y))

        self.bbox = bbox
        self.center = center
        
    def encloses(self, pair):
        # check if a pair of x, y coordinates is within this box
        x, y = pair
        x0, y0, x1, y1 = self.bbox
        if x0 <= x <= x1 and y0 <= y <= y1:
            return True
        return False

    # value property
    def set_value(self, value):
        self._value = int(value) if value else 0
        self.board.itemconfig(self._text, text=str(value))
        self.update_color()

    def get_value(self):
        return str(self._value) if self._value else ''

    def del_value(self):
        self._value = 0
        self.board.itemconfig(self._text, text='')

    value = property(get_value, set_value, del_value)

    # readonly property
    def get_readonly(self):
        return self._readonly

    def set_readonly(self, readonly):
        self._readonly = readonly
        self.update_color()

    readonly = property(get_readonly, set_readonly)

    def toggle_readonly(self):
        self._readonly = not self._readonly
        self.update_color()

    def update_color(self):
        # color overrides all
        if self.color:
            fill = self.color
        elif self._selected:
            fill = SELECT
        elif self.highlight:
            fill = HIGHLIGHT
        else:
            fill = self.fill

        if self._selected:
            outline = RED
        else:
            outline = BLACK
            
        self.board.itemconfig(self._rect, fill=fill, outline=outline)
        
        # update text fill
        if self.wrong:
            textfill = WRONG
        elif self.given:
            textfill = GIVEN
        elif self.readonly:
            textfill = READONLY
        else:
            textfill = TEXT

        self.board.itemconfig(self._text, fill=textfill)

        # reset pencil marks colors
        for v in self:
            self.pencil.set_color(v, 'black')


    # highlight property
    def set_highlight(self, highlight):
        if bool(highlight) != self._highlight:
            self._highlight = bool(highlight)
            self.update_color()

    def get_highlight(self):
        return self._highlight

    highlight = property(get_highlight, set_highlight)

    # color property
    def set_color(self, color):
        self._color = color
        self.update_color()
        
    def get_color(self):
        return self._color

    color = property(get_color, set_color)

    def set(self):
        # set this cell as selected
        self._selected = True
        self.update_color()

    def reset(self):
        # set this cell as unselected
        fill = self.color or self.fill
        self._selected = False
        self.update_color()

    def tmp_color(self, color, outline=None):
        # set a temporary color
        self.board.itemconfig(self._rect, fill=color)
        if outline is not None:
            self.board.itemconfig(self._rect, outline=outline)
            
    def solve_hint(self):
        # if this cell has an active hint, do whatever action is
        # necessary to use it
        colors = [self.board.itemcget(mark, 'fill') for mark in self.marks]
        # if there's a single green mark, that's a single
        if self.hint_active == 1 and colors.count('green') == 1: 
            v = colors.index('green') + 1
            self.pencil.set_color(v, 'black')
            self.select()
            self.value = str(v)
            self.board.cb_changed_value()

        else:
            for i, color in enumerate(colors):
                # if there's any red marks, remove them
                if color == 'red':
                    self.pencil[i+1] = False
                    self.pencil.set_color(i+1, 'black')
                # if there's any green marks, reset color
                if color == 'green':
                    self.pencil.set_color(i+1, 'black')

            self.board.cb_changed_pencil_mark()
            self.update_color()

        self.hint_active = 0
            

    def select(self):
        # select this cell and unselect any other cells        
        for other in self.board.cells:
            if other is not self:
                other.reset()
        self.set()
        self.board.current = self
                
    def get_left(self):
        # get cell to the left
        row, col = self.row, self.col
        col -= 1
        if col < 0:
            return self
        else:
            return self.board.cells[row*9 + col]

    def get_right(self):
        # get cell to the right
        row, col = self.row, self.col
        col += 1
        if col > 8:
            return self
        else:
            return self.board.cells[row*9 + col]

    def get_up(self):
        # get cell up
        row, col = self.row, self.col
        row -= 1
        if row < 0:
            return self
        else:
            return self.board.cells[row*9 + col]
    
    def get_down(self):
        # get cell down
        row, col = self.row, self.col
        row += 1
        if row > 8:
            return self
        else:
            return self.board.cells[row*9 + col]

    def pop_color_dialog(self, event):
        dialog = ColorDialog(self.board, self, event)
        dialog.draw()
        return dialog
        
                
class Board(Tkinter.Canvas):
    def setup(self):
        self.gameid = None
        self.puzzle = None
        self.solution = None
        self.history = History()
        
        self.size = None
        self.cellsize = None
        self.cells = [None]*81
        self.lines = [[None]*4, [None]*4]

        self.links = []
        self.linklabels = {}
        self.linking = None

        # currently selected cell
        self.current = None
        # current waiting dialog
        self.dialog = None
        # highlight variable
        self.var_highlight = Tkinter.IntVar()
        self.var_highlight.set(1)
        self.var_automarks = Tkinter.IntVar()
        self.var_automarks.set(1)
        self.var_show_wrong = Tkinter.IntVar()
        self.var_show_wrong.set(1)

        self.marked = None

        self.setup_bindings()
        self.cb_draw_board()

    def setup_bindings(self):
        self.bind('<Configure>', self.cb_draw_board)
        self.bind('<Button-1>', self.cb_board_click_left)
        self.bind('<Button-3>', self.cb_board_click_right)
        self.bind('<Control-Button-3>', self.cb_board_click_control_right)
        self.bind('<Shift-Button-3>', self.cb_board_click_shift_right)

        self.bind('<Shift-Button-1>', self.cb_board_shift_click_left)
        self.bind('<Shift-ButtonRelease-1>', self.cb_board_shift_release_left)
        self.bind('<Shift-B1-Motion>', self.cb_board_shift_motion_left)
        self.bind('<Shift-Double-Button-1>', self.cb_board_shift_double_left)

        self.bind('<Shift-Button-4>', self.cb_board_change_link_state)
        self.bind('<Shift-Button-5>', self.cb_board_change_link_state)
        
        #self.bind('<B1-Motion>', self.cb_board_drag_left)
        self.bind('<B3-Motion>', self.cb_board_drag_right)
        #self.bind('<ButtonRelease-1>', self.cb_board_release_left)
        self.bind('<ButtonRelease-3>', self.cb_board_release_right)
        

    def cb_draw_board(self, event=None):
        if event is None:
            width = int(self['width'])
            height = int(self['height'])
        else:
            width = event.width
            height = event.height
        self.size = (width, height)
            

        # get the smaller
        if width < height:
            cellsize = width / 9
        else:
            cellsize = height / 9

        self.cellsize = cellsize

        origin = ((width/2) - (cellsize*5),
                  (height/2) - (cellsize*5))
        
        margin = cellsize/2
        ox, oy = origin

        # draw horizontal lines dividing boxes
        for i, n in enumerate((0, 3, 6, 9)):
            y = oy + margin + n*cellsize

            coords = (0+ox+margin, y, width-ox-margin, y)

            if self.lines[0][i] is None:
                self.lines[0][i] = self.create_line(*coords, width=3)
            else:
                self.coords(self.lines[0][i], *coords)
            
        # draw vertical lines dividing boxes
        for i, n in enumerate((0, 3, 6, 9)):
            x = ox + margin + n*cellsize
            coords = (x, 0+oy+margin, x, height-oy-margin)
            if self.lines[1][i] is None:
                self.lines[1][i] = self.create_line(*coords, width=3)
            else:
                self.coords(self.lines[1][i], *coords)
            
        # draw cells
        for i in xrange(81):
            cell = self.cells[i]
            if cell is None:
                row, col = divmod(i, 9)
                cell = Cell(self, row, col)
                self.cells[i] = cell
                
            cell.draw(cellsize, origin)

    def cb_print_board(self):
        board = ''
        for cell in self.cells:
            if cell.value:
                board += cell.value
            else:
                board += '0'
        print repr(board)

    def cb_board_click_left(self, event=None):
        if self.dialog is None:
            self.cb_board_select_cell(event)
        else:
            self.dialog.cb_click_left(event)
            
    def cb_board_click_right(self, event=None):
        self.cb_mark_circle(event)

    def cb_board_click_control_right(self, event=None):
        self.cb_mark_square(event)

    def cb_board_click_shift_right(self, event=None):
        self.cb_mark_diamond(event)


    def clear_mark(self, marktag):
        circle = self.find_withtag('circled_'+marktag)
        square = self.find_withtag('squared_'+marktag)
        diamond = self.find_withtag('diamond_'+marktag)
        if circle:
            self.delete(circle)
            return 1
        if square:
            self.delete(square)
            return 1
        if diamond:
            self.delete(diamond)
            return 1
        
    def cb_mark_circle(self, event=None):
        item = self.find_closest(event.x, event.y)
        tags = self.gettags(item)
        if 'pencilmark' not in tags:
            return

        marktag = tags[1]

        if self.clear_mark(marktag):
            return

        x, y = self.coords(item)

        x0 = x - self.cellsize/6
        x1 = x + self.cellsize/6
        y0 = y - self.cellsize/6
        y1 = y + self.cellsize/6

        circle = self.create_oval(x0, y0, x1, y1,
                                  fill='yellow', outline='black',
                                  tags=('circled_pencilmark',
                                        'circled_'+marktag,
                                        )
                                  )
        self.lift(item)

    def cb_mark_square(self, event=None):
        item = self.find_closest(event.x, event.y)
        tags = self.gettags(item)
        if 'pencilmark' not in tags:
            return

        marktag = tags[1]

        if self.clear_mark(marktag):
            return
        x, y = self.coords(item)

        x0 = x - self.cellsize/6
        x1 = x + self.cellsize/6
        y0 = y - self.cellsize/6
        y1 = y + self.cellsize/6
        
        square = self.create_rectangle(x0, y0, x1, y1,
                                       fill='red', outline='black',
                                       tags=('squared_pencilmark',
                                             'squared_'+marktag,
                                             )
                                       )
        self.lift(item)

    def cb_mark_diamond(self, event=None):
        item = self.find_closest(event.x, event.y)
        tags = self.gettags(item)
        if 'pencilmark' not in tags:
            return

        marktag = tags[1]

        if self.clear_mark(marktag):
            return
        x, y = self.coords(item)

        s = self.cellsize / 6
        
        x0 = x - s
        y0 = y

        x1 = x
        y1 = y - s

        x2 = x + s
        y2 = y

        x3 = x
        y3 = y + s

        diamond = self.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3,
                                        fill='green', outline='black',
                                        tags=('diamond_pencilmark',
                                              'diamond_'+marktag,
                                              )
                                        )
        self.lift(item)


    def cb_board_drag_right(self, event=None):
        x, y = event.x, event.y
        

    def cb_board_shift_click_left(self, event=None):
        self.cb_board_start_link(event)
    
    def cb_board_shift_motion_left(self, event=None):
        self.cb_board_motion_link(event)

    def cb_board_shift_release_left(self, event=None):
        self.cb_board_end_link(event)

    def cb_board_shift_double_left(self, event=None):
        self.cb_board_delete_link(event)

    def find_cell(self, x, y):
        # find cell which encloses x, y coords
        #for cell in self.cells:
        #    for mark in cell._marks:
        #        x0, y0, x1, y1 = mark.bbox
        #        if x0 <= x <= x1 and y0 <= y <= y1:
        #            return mark
        item = self.find_closest(x, y)
        tags = self.gettags(item)
        if 'pencilmark' not in tags:
            return
        x, y = self.coords(item)
        return x, y
        

    def cb_board_start_link(self, event=None):
        cell = self.find_cell(event.x, event.y)
        if cell is None:
            return

        sx, sy = cell#.center

        self.linking = self.create_line(sx, sy, sx, sy,
                                        fill='red', arrow='last',
                                        width=3,
                                        #dash=(3, 1),
                                        tags=('link'))

        
    def cb_board_motion_link(self, event=None):
        cell = self.find_cell(event.x, event.y)
        if cell is None:
            return
        if self.linking is None:
            return

        cx, cy = cell#cell.center
        sx, sy, foox, fooy = self.coords(self.linking)

        self.coords(self.linking, sx, sy, cx, cy)

        
    def cb_board_end_link(self, event=None):
        cell = self.find_cell(event.x, event.y)
        if self.linking is None:
            return
        if cell is None:
            self.delete(self.linking)
            return

        tags = self.gettags(self.linking)

        cx, cy = cell#.center
        sx, sy, foox, fooy = self.coords(self.linking)

        # if it's the same, destroy it
        if (cx, cy) == (sx, sy):
            self.delete(self.linking)
        else:
            # otherwise, add to the list and bind to the callbacks
            self.links.append(self.linking)
            self.addtag_withtag('current', 'link_end_%s_%s'%cell)

        self.linking = None

    def cb_board_delete_link(self, event=None):
        # with double click, delete link... coming to this cell first
        cell = self.find_cell(event.x, event.y)
        if cell is None:
            return

        cx, cy = cell#.center
        # first, try to find a link coming to this cell
        for link in self.links:
            # get the cords for it
            x0, y0, x1, y1 = self.coords(link)

            if (int(x1), int(y1)) == (int(cx), int(cy)):
                self.delete(link)
                self.links.remove(link)
                try:
                    label, frame = self.linklabels[link]
                    self.delete(label)
                    self.delete(frame)
                    del self.linklabels[link]
                except KeyError:
                    pass
                break

    def cb_board_change_link_state(self, event=None):
        # first, find a link coming to this cell
        cell = self.find_cell(event.x, event.y)
        if cell is None:
            return

        cx, cy = cell#.center
        # first, try to find a link coming to this cell
        for link in self.links:
            # get the cords for it
            x0, y0, x1, y1 = self.coords(link)

            if (int(x1), int(y1)) == (int(cx), int(cy)):
                break
        else:
            return

        try:
            label, frame = self.linklabels[link]
        except KeyError:
            x = x0 + (x1-x0)/2
            y = y0 + (y1-y0)/2
            fontsize = int(self.cellsize / 4)
            label = self.create_text(x, y, text='', fill='black',
                                     font=('Arial', fontsize, 'bold'),
                                     tags='linklabel')
            bbox = self.bbox(label)
            frame = self.create_rectangle(*bbox, fill='red',
                                          tags='linkframe')
            self.lift(label)
            
            self.linklabels[link] = (label, frame)

        text = self.itemcget(label, 'text')

        ts = '-='

        if event.num == 4:
            if not text:
                n = '1'
                t = '-'
            else:
                n = int(text[1])
                t = text[0]
                i = ts.index(t)
                
                if n < 9:
                    n += 1
                else:
                    n = 1
                    t = ts[int(not(i))]
                    
            self.itemconfig(label, text='%s%s%s'%(t, n, t))
            bbox = self.bbox(label)
            self.coords(frame, bbox)
        
        if event.num == 5:
            if not text:
                n = '9'
                t = '='
            else:
                n = int(text[1])
                t = text[0]
                i = ts.index(t)
                
                if n > 1:
                    n -= 1
                else:
                    n = 9
                    t = ts[int(not(i))]
                    
            self.itemconfig(label, text='%s%s%s'%(t, n, t))
            bbox = self.bbox(label)
            self.coords(frame, bbox)
        
    def cb_clear_lines(self, event=None):
        self.delete('line')
        self.delete('circled_pencilmark')
        self.delete('squared_pencilmark')
        self.delete('diamond_pencilmark')
        self.marked = None

    def cb_clear_links(self, event=None):
        self.delete('link')
        self.delete('linklabel')
        self.delete('linkframe')
        del self.links[:]

    def cb_board_release_right(self, event=None):
        pass

    def cb_board_select_cell(self, event=None):
        # select a cell with mouse click
        x, y = event.x, event.y
        for cell in self.cells:
            if cell.encloses((x, y)):
                cell.select()
                self.current = cell
                self.cb_changed_selection()
                


    def cb_board_choose_color(self, event=None):
        self.cb_board_select_cell(event)
        if self.current is not None:
            self.dialog = self.current.pop_color_dialog(event)

    def cb_board_pop_menu(self, event):
        self.dialog = PopUpMenu(self, event)

    def cb_board_up(self, event=None):
        if self.current is None:
            other = self.cells[0]
        else:
            other = self.current.get_up()
        if other is not self.current:
            other.select()
            self.current = other
            self.cb_changed_selection()

    def cb_board_down(self, event=None):
        if self.current is None:
            other = self.cells[0]
        else:
            other = self.current.get_down()
        if other is not self.current:
            other.select()
            self.current = other
            self.cb_changed_selection()

    def cb_board_left(self, event=None):
        if self.current is None:
            other = self.cells[0]
        else:
            other = self.current.get_left()
        if other is not self.current:
            other.select()
            self.current = other
            self.cb_changed_selection()
                
    def cb_board_right(self, event=None):
        if self.current is None:
            other = self.cells[0]
        else:
            other = self.current.get_right()
        if other is not self.current:
            other.select()
            self.current = other
            self.cb_changed_selection()


    def cb_board_number(self, event=None):
        cell = self.current

        if cell.given:
            return

        if cell.readonly:
            return

        if event is None:
            return
        
        n = event.char

        if cell.value == n:
            del cell.value
        else:
            cell.value = n
            del cell.pencil

        self.cb_changed_value()

        for cell in self.cells:
            if not cell.value:
                #print 'value', cell
                return
            if cell.wrong:
                #print 'wrong', cell
                return
            
        print 'Solved'

        self.parent.games[self.gameid]['solved'] = datetime.datetime.now()
        self.parent.save_games()

    def cb_board_pencil_mark(self, event=None):
        cell = self.current

        if cell.given:
            return

        if cell.readonly:
            return

        if cell.value:
            return

        if event is None:
            return
        
        n = event.char

        i = 'qweasdzxc'.index(n)
        cell.pencil.toggle(i+1)

        self.cb_changed_pencil_mark()
        
    def cb_board_readonly(self, event=None):
        cell = self.current
        if cell.given:
            return

        if not cell.value:
            return
        
        cell.toggle_readonly()


    def cb_changed_selection(self, event=None):
        v = self.current.value
        
        if self.var_highlight.get():
            for cell in self.cells:
                if v and v in cell.pencil:
                    cell.highlight = True
                else:
                    cell.highlight = False
                cell.hint_active = 0
        

    def cb_changed_value(self, event=None):
        v = self.current.value
        cell = self.current
        if self.var_automarks.get():
            for other in cell.get_row() + cell.get_col() + cell.get_box():
                other.pencil[v] = False
        del cell.pencil
        self.cb_changed_selection()

        self.save_state()
        
    def cb_changed_pencil_mark(self, event=None):
        self.save_state()

    def save_state(self):
        values = [cell.value for cell in self.cells]
        pencil = [cell.pencil.get_all() for cell in self.cells]
        self.history.push((values, pencil))
        
    def load_state(self, state):
        if state is None:
            return

        values, pencil = state
        for v, marks, cell in zip(values, pencil, self.cells):
            cell.value = v
            if v:
                del cell.pencil
            else:
                cell.pencil = marks
            

    def cb_change_color(self, event=None):
        cell = self.current
        if cell is None:
            return
        
        colors = {'F9':None,
                  'F5':YELLOW,
                  'F6':PURPLE,
                  'F7':GREEN,
                  'F8':LBLUE}

        fill = colors[event.keysym]
        cell.color = fill

    def cb_clear_all_pencil_marks(self, event=None):
        for cell in self.cells:
            del cell.pencil

    def cb_fill_all_pencil_marks(self, event=None):
        for cell in self.cells:
            cell.pencil = range(1, 10)

    def cb_fill_valid_pencil_marks(self, event=None):
        for cell in self.cells:
            cell.pencil = cell.candidates()
        self.save_state()


    def cb_toggle_highlight(self, event=None):
        v = self.var_highlight.get()
        self.var_highlight.set(not v)
        self.cb_changed_selection()

    def cb_reset_all_colors(self, event=None):
        for cell in self.cells:
            cell.color = None

    def load_puzzle(self, gameid, puzzle, solution):
        self.gameid = gameid
        self.puzzle = puzzle
        self.solution = solution

        self.cb_clear_all_pencil_marks()

        for i, v in enumerate(puzzle):
            cell = self.cells[i]
            cell.solution = str(solution[i]+1)

            if v is not None:
                cell.value = str(v+1)
                cell.given = True
                cell.readonly = True
                cell.update_color()

        self.save_state()

    def cb_undo(self, event=None):
        state = self.history.undo()
        self.load_state(state)

    def cb_redo(self, event=None):
        state = self.history.redo()
        self.load_state(state)

    def cb_clear_cell(self, event=None):
        if self.current is not None:
            self.current.value = ''
            del self.current.pencil
            self.save_state()

    def get_rows(self):
        for row in range(9):
            cells = []
            for col in range(9):
                other = self.cells[row*9 + col]
                cells.append(other)
            yield cells

    def get_cols(self):
        for col in range(9):
            cells = []
            for row in range(9):
                other = self.cells[row*9 + col]
                cells.append(other)
            yield cells

    def get_boxes(self):        
        for x in range(0, 9, 3):
            for y in range(0, 9, 3):
                cells = []
                for row in range(x, x+3):
                    for col in range(y, y+3):
                        other = self.cells[row*9 + col]
                        cells.append(other)
                yield cells

    def cb_hint(self, event=None):
        # check if there's any cell with an active hint and do it
        active = [cell for cell in self.cells if cell.hint_active]
        if active:
            for cell in active:
                cell.solve_hint()
            return 1

        #- Naked  Singles*
        #- Hidden Singles*
        #- Naked  Pairs*
        #- Naked  Triples*
        #- Locked Candidates (1)*
        #- Locked Candidates (2)*
        #- Naked  Quads*
        #- Hidden Pairs*
        #- Hidden Triples*
        #- Hidden Quads*
        #- X-Wing*
        #- Swordfish*
        #- Jellyfish*
        #- XY-Wing
        #- XYZ-Wing
        #- Colors
        #- Multi-Colors

        hints = self.parent.hintvars
                
        if hints['Naked Single'].get() and self.hint_naked_single():
            self.parent.status.set('Naked Single', timeout=2)
            return 1

        if hints['Hidden Single'].get() and self.hint_hidden_single():
            self.parent.status.set('Hidden Single', timeout=2)
            return 1

        if hints['Naked Pair'].get() and self.hint_naked_pair():
            self.parent.status.set('Naked Pair', timeout=2)
            return 1

        if hints['Pointing Pair'].get() and self.hint_pointing_pair(): 
            self.parent.status.set('Pointing Pair', timeout=2)
            return 1

        if hints['Box Line Reduction'].get() and self.hint_box_line_reduction():
            self.parent.status.set('Box Line Reduction', timeout=2)
            return 1

        if hints['Hidden Pair'].get() and self.hint_hidden_pair():
            self.parent.status.set('Hidden Pair', timeout=2)
            return 1

        if hints['Naked Triple'].get() and self.hint_naked_triple():
            self.parent.status.set('Naked Triple', timeout=2)
            return 1

        if hints['Hidden Triple'].get() and self.hint_hidden_triple():
            self.parent.status.set('Hidden Triple', timeout=2)
            return 1

        if hints['Naked Quad'].get() and self.hint_naked_quad():
            self.parent.status.set('Naked Quad', timeout=2)
            return 1

        if hints['Hidden Quad'].get() and self.hint_hidden_quad():
            self.parent.status.set('Hidden Quad', timeout=2)
            return 1

        if hints['X-Wing'].get() and self.hint_x_wing():
            self.parent.status.set('X-Wing', timeout=2)
            return 1

        if hints['Swordfish'].get() and self.hint_swordfish():
            self.parent.status.set('Swordfish', timeout=2)
            return 1

        if hints['Jellyfish'].get() and self.hint_jellyfish():
            self.parent.status.set('Swordfish', timeout=2)
            return 1

        #if self.hint_xy_wing():
        self.parent.status.set('No Hint', timeout=2)

    # solving hints

    # Naked Subset: If n cells in the same group contain exactly the
    # same n candidate values, these candidate values can be excluded
    # from other cells in the group.
    def hint_naked_single(self):
        for cell in self.cells:
            if not cell.value and len(cell) == 1:
                v = cell.pencil.get_all()[0]
                cell.pencil.set_color(v, 'green')
                cell.tmp_color('white', 'green')
                cell.hint_active = 1
                return 1
            
    def hint_naked_pair(self):
        return self.hint_naked_subset(2)
    
    def hint_naked_triple(self):
        return self.hint_naked_subset(3)

    def hint_naked_quad(self):
        return self.hint_naked_subset(4)

    def hint_naked_subset(self, n):
        groups = [self.get_rows(), self.get_cols(), self.get_boxes()]
        for group in itertools.chain(*groups):
        #for group in [list(self.get_rows())[7]]:
            strip_group = [cell for cell in group if not cell.value]
            strip_set = [set(cell.pencil.get_all()) for cell in strip_group]
            strip = zip(strip_group, strip_set)

            for comb in itertools.combinations(strip, n):
                cells, sets = zip(*comb)
                
                inter = reduce(set.union, sets)
                if len(inter) == n:
                    # we may have a naked pair in this group
                    break
            else:
                continue

            cleared = False
            
            for v in inter:
                for cell in set(group).difference(set(cells)):
                    if v in cell.pencil:
                        cell.pencil.set_color(v, 'red')
                        cell.tmp_color('white', 'red')
                        cell.hint_active = n
                        cleared = True

            if cleared:
                for v in inter:
                    for cell in cells:
                        if v in cell.pencil:
                            cell.pencil.set_color(v, 'green')
                            cell.tmp_color('white', 'green')
                            cell.hint_active = n

                return 1
            

    # Pointing Pair: When a specific candidate value inside a box is
    # restricted to one row or column, you can use the Pointing Pair
    # technique. This means that you can exclude the same candidate
    # value from other boxes in the same row or column.
    def hint_pointing_pair(self):
        # FIXME: this can be simplified a lot
        for box in self.get_boxes():
            cols = [box[x::3] for x in range(3)]

            values = []
            for col in cols:
                b = reduce(int.__or__, map(int, col))
                values.append(b)

            for j in range(1, 10):
                # if it appears in just a single column...
                count = [col for (col, v) in zip(cols, values) if (2**j) & v]
                if len(count) == 1:
                    # it may be a pointing pair... check the rest of
                    # the column
                    # part of the column inside the box
                    inbox = count[0]
                    # outside of the box
                    outbox = [c for c in inbox[0].get_col() if c not in inbox]

                    # check if it appears in any other cell
                    cells = [cell for cell in outbox if str(j) in cell]
                    if cells:
                        # they do, we have a pointing pair
                        # highlight the poiting cells
                        for cell in inbox:
                            if str(j) in cell:
                                cell.tmp_color('white', 'green')
                                cell.pencil.set_color(j, 'green')
                                cell.hint_active = 2
                        for cell in cells:
                            cell.tmp_color('white', 'red')
                            cell.pencil.set_color(j, 'red')
                            cell.hint_active = 2
                            
                        return 1


            rows = [box[x*3:(x+1)*3] for x in range(3)]
            values = []
            for row in rows:
                b = reduce(int.__or__, map(int, row))
                values.append(b)

            for j in range(1, 10):
                # if it appears in just a single row...
                count = [row for (row, v) in zip(rows, values) if (2**j) & v]
                if len(count) == 1:
                    # it may be a pointing pair... check the rest of
                    # the row
                    # part of the row inside the box
                    inbox = count[0]
                    # outside of the box
                    outbox = [c for c in inbox[0].get_row() if c not in inbox]

                    # check if it appears in any other cell
                    cells = [cell for cell in outbox if str(j) in cell]
                    if cells:
                        # they do, we have a pointing pair
                        # highlight the poiting cells
                        for cell in inbox:
                            if str(j) in cell:
                                cell.tmp_color('white', 'green')
                                cell.pencil.set_color(j, 'green')
                                cell.hint_active = 2
                        for cell in cells:
                            cell.tmp_color('white', 'red')
                            cell.pencil.set_color(j, 'red')
                            cell.hint_active = 2

                        return 1

    # Box Line Reduction: When a specific candidate value in a row or
    # column only occurs in one box, this value can be exluded from
    # other cells in the same box.
    def hint_box_line_reduction(self):
        for group in itertools.chain(self.get_rows(), self.get_cols()):
            # we need all 3 boxes that this group intersects
            boxes = [cell.get_box() for cell in group[::3]]
            inbox = [group[i:i+3] for i in range(0, 9, 3)]

            values = []
            for box in inbox:
                b = reduce(int.__or__, map(int, box))
                values.append(b)
                
            for j in range(1, 10):
                # if it apperar in just a single box...
                boxset = zip(boxes, inbox, values)
                count = [(box, ibox) for (box,ibox,v) in boxset if (2**j) & v]
                
                # if it appears in just a single box
                if len(count) == 1:
                    # it may be a box line reduction case... check the
                    # rest of the box
                    box, ibox = count[0]
                    outbox = [cell for cell in box if cell not in ibox]

                    # check if it appears in any other cell
                    cells = [cell for cell in outbox if str(j) in cell]

                    if cells:
                        # it does, we have a case, highlight the cells
                        for cell in ibox:
                            if str(j) in cell:
                                cell.tmp_color('white', 'green')
                                cell.pencil.set_color(j, 'green')
                                cell.hint_active = 2

                        for cell in cells:
                            cell.tmp_color('white', 'red')
                            cell.pencil.set_color(j, 'red')
                            cell.hint_active = 2

                        return 1

    # Hidden Pair: If two cells in a group contain an identical pair
    # of candidates and no other cells in that group contain those two
    # candidates, then other candidates in those two cells can be
    # excluded.
    def hint_hidden_single(self):
        return self.hint_hidden_subset(1)
    
    def hint_hidden_pair(self):
        return self.hint_hidden_subset(2)
    
    def hint_hidden_triple(self):
        return self.hint_hidden_subset(3)
    
    def hint_hidden_quad(self):
        return self.hint_hidden_subset(4)    
    
    def hint_hidden_subset(self, n):
        groups = [self.get_rows(), self.get_cols(), self.get_boxes()]
        for group in itertools.chain(*groups):

            # all candidates in the group
            all_values = []
            for cell in group:
                all_values.extend(cell.pencil.get_all())

            # candidates can appear at most n times
            values = [v for v in set(all_values) if all_values.count(v) <= n]

            # and we need at least n candidates
            if len(values) < n:
                continue

            # make cell sets
            sets = [(cell, set(cell.pencil.get_all())) for cell in group]

            # now, for each n items combination, if any n cells
            # combination intersect with the items, we have a hit
            for comb in itertools.combinations(values, n):
                comb = set(comb)
                cells = []
                for cell, subset in sets:
                    if comb.intersection(subset):
                        cells.append((cell, subset))

                if len(cells) == n:
                    # we have a subset here... let's check if the
                    # group has any other values besides the
                    # combination to make it a hidden subset
                    clear = False
                    for cell, subset in cells:
                        diff = subset.difference(comb)
                        if diff:
                            clear = True
                            # yes, we have it
                            cell.tmp_color('white', 'green')
                            cell.hint_active = n
                            for v in diff:
                                cell.pencil.set_color(v, 'red')
                            for v in comb:
                                cell.pencil.set_color(v, 'green')

                    if clear:
                        return 1

    # 
    def hint_xy_wing(self):
        return


    def hint_x_wing(self):
        return self.hint_fish(2)

    def hint_swordfish(self):
        return self.hint_fish(3)

    def hint_jellyfish(self):
        return self.hint_fish(4)

    # Look for N rows with 2 to N candidate cells for ONE given
    # digit. If these fall on exactly N common columns, then all N
    # rows can be cleared of that digit except in the defining cells.
    def hint_fish(self, n):
        # TODO: introduce boxes
        rows = list(self.get_rows())
        cols = list(self.get_cols())

        # So... for each digit...
        for digit in map(str, range(1, 10)):
            # get the rows with 2 to n candidate cells with the given
            # digit
            candidate_rows = []
            for row in rows:
                count = len([cell for cell in row if digit in cell])
                if 2 <= count <= n:
                    candidate_rows.append(row)

            # if not enough rows, ignore
            if len(candidate_rows) < n:
                continue

            # otherwise, group them in groups with n rows
            for group in itertools.combinations(candidate_rows, n):
                match = set()
                keep = []# cells to keep values
                for row in group:
                    for cell in row:
                        if digit in cell:
                            match.add(tuple(cell.get_col()))
                            keep.append(cell)

                # if the digit falls on n cols, then we probably have a fish
                if len(match) == n:
                    nokeep = [cell for col in match for cell in col
                              if cell not in keep and digit in cell]
                    if nokeep:
                        for cell in keep:
                            cell.pencil.set_color(digit, 'green')
                            cell.tmp_color('white', 'green')
                            cell.hint_active = n

                        for cell in nokeep:
                            cell.pencil.set_color(digit, 'red')
                            cell.tmp_color('white', 'red')
                            cell.hint_active = n
                            
                        return 1
            
        # So... for each digit...
        for digit in map(str, range(1, 10)):
            # get the rows with 2 to n candidate cells with the given
            # digit
            candidate_cols = []
            for col in cols:
                count = len([cell for cell in col if digit in cell])
                if 2 <= count <= n:
                    candidate_cols.append(col)

            # if not enough rows, ignore
            if len(candidate_cols) < n:
                continue

            # otherwise, group them in groups with n rows
            for group in itertools.combinations(candidate_cols, n):
                match = set()
                keep = []# cells to keep values
                for col in group:
                    for cell in col:
                        if digit in cell:
                            match.add(tuple(cell.get_row()))
                            keep.append(cell)

                # if the digit falls on n cols, then we probably have a fish
                if len(match) == n:
                    nokeep = [cell for row in match for cell in row
                              if cell not in keep and digit in cell]
                    if nokeep:
                        for cell in keep:
                            cell.pencil.set_color(digit, 'green')
                            cell.tmp_color('white', 'green')
                            cell.hint_active = n

                        for cell in nokeep:
                            cell.pencil.set_color(digit, 'red')
                            cell.tmp_color('white', 'red')
                            cell.hint_active = n
                            
                        return 1
            

class MainWindow(Tkinter.Tk):

    def setup(self):
        self.mainframe = Tkinter.Frame(self)
        self.optionsframe = Tkinter.Frame(self)
        self.toolsframe = Tkinter.Frame(self)
        
        self.board = Board(self.mainframe, width=500, height=500, bg='white')
        self.board.parent = self
        self.board.setup()
        self.board.pack(expand=1, fill=BOTH)

        self.status = TkExtra.StatusBar(self, anchor=W)
        self.status.pack(side=BOTTOM, expand=0, fill=X)

        self.toolsframe.pack(expand=0, side=LEFT, fill=Y)
        self.mainframe.pack(expand=1, side=LEFT, fill=BOTH)
        self.optionsframe.pack(expand=0, side=RIGHT, fill=Y)

        self.setup_bindings()

        self.build_menu()
        self.build_tools()
        self.build_solving()


    def setup_bindings(self):
        self.bind('<Up>', self.board.cb_board_up)
        self.bind('<Down>', self.board.cb_board_down)
        self.bind('<Left>', self.board.cb_board_left)
        self.bind('<Right>', self.board.cb_board_right)
        
        self.bind('1', self.board.cb_board_number)
        self.bind('2', self.board.cb_board_number)
        self.bind('3', self.board.cb_board_number)
        self.bind('4', self.board.cb_board_number)
        self.bind('5', self.board.cb_board_number)
        self.bind('6', self.board.cb_board_number)
        self.bind('7', self.board.cb_board_number)
        self.bind('8', self.board.cb_board_number)
        self.bind('9', self.board.cb_board_number)

        self.bind('q', self.board.cb_board_pencil_mark)
        self.bind('w', self.board.cb_board_pencil_mark)
        self.bind('e', self.board.cb_board_pencil_mark)
        self.bind('a', self.board.cb_board_pencil_mark)
        self.bind('s', self.board.cb_board_pencil_mark)
        self.bind('d', self.board.cb_board_pencil_mark)
        self.bind('z', self.board.cb_board_pencil_mark)
        self.bind('x', self.board.cb_board_pencil_mark)
        self.bind('c', self.board.cb_board_pencil_mark)

        self.bind('m', self.board.cb_board_readonly)
        self.bind('h', self.board.cb_hint)       
        self.bind('t', self.board.cb_toggle_highlight)       
        self.bind('r', self.board.cb_reset_all_colors)       
        self.bind('y', self.board.cb_clear_lines)
        self.bind('<Delete>', self.board.cb_clear_cell)

        self.bind('<F5>', self.board.cb_change_color)
        self.bind('<F6>', self.board.cb_change_color)
        self.bind('<F7>', self.board.cb_change_color)
        self.bind('<F8>', self.board.cb_change_color)
        self.bind('<F9>', self.board.cb_change_color)

        self.bind('<Prior>', self.board.cb_undo)
        self.bind('<Next>', self.board.cb_redo)

        
    def build_menu(self):
        opts = dict(relief=GROOVE, tearoff=0, bd=1)

        self['menu'] = menu = Tkinter.Menu(self, relief=GROOVE, bd=1)
        self.menu_root = menu

        self.menu_game = menu_game = Tkinter.Menu(menu, **opts)
        menu_game.add_command(label='New game', underline=0,
                              command=self.cb_newgame)
        menu_game.add_command(label='Clear marks', underline=0,
                               command=self.board.cb_clear_all_pencil_marks)
        menu_game.add_command(label='Fill all marks', underline=0,
                               command=self.board.cb_fill_all_pencil_marks)
        menu_game.add_command(label='Fill valid marks', underline=1,
                               command=self.board.cb_fill_valid_pencil_marks)
        menu_game.add_command(label='Reset colors', underline=0,
                              command=self.board.cb_reset_all_colors)
        menu_game.add_command(label='Clear Lines', underline=0,
                              command=self.board.cb_clear_lines)
        menu_game.add_command(label='Clear Links', underline=0,
                              command=self.board.cb_clear_links)
        menu_game.add_command(label='Hint', underline=0,
                               command=self.board.cb_hint)
        menu_game.add_command(label='Exit', underline=0,
                              command=self.cb_exit)

        menu.add_cascade(label='Game', underline=0, menu=menu_game)

        self.menu_help = menu_help = Tkinter.Menu(menu, **opts)

        menu_help.add_checkbutton(label='Highlight candidates',
                                  variable=self.board.var_highlight)
        menu_help.add_checkbutton(label='Auto pencil marks',
                                  variable=self.board.var_automarks)
        menu_help.add_command(label='Print Board',
                              command=self.board.cb_print_board)

        menu.add_cascade(label='Help', underline=0, menu=menu_help)

    def build_solving(self):
        self.hintvars = {}
        hints = [('Naked Single', 1, Tkinter.ACTIVE),
                 ('Hidden Single', 1, Tkinter.ACTIVE),
                 ('Naked Pair',0, Tkinter.ACTIVE),
                 ('Pointing Pair',0, Tkinter.ACTIVE),
                 ('Box Line Reduction',0, Tkinter.ACTIVE),
                 ('Hidden Pair',0, Tkinter.ACTIVE),
                 ('Naked Triple',0, Tkinter.ACTIVE),
                 ('Hidden Triple',0, Tkinter.ACTIVE),
                 ('Naked Quad',0, Tkinter.ACTIVE),
                 ('Hidden Quad',0, Tkinter.ACTIVE),
                 ('X-Wing',0, Tkinter.ACTIVE),
                 ('Swordfish',0, Tkinter.ACTIVE),
                 ('Jellyfish',0, Tkinter.ACTIVE),
                 ('Remote Pair', None, Tkinter.DISABLED),
                 ('XY-Wing', None, Tkinter.DISABLED),
                 ('XYZ-Wing', None, Tkinter.DISABLED),
                 ('Empty Rectangles', None, Tkinter.DISABLED),
                 ('Colors', None, Tkinter.DISABLED),
                 ('Nice Loop', None, Tkinter.DISABLED),
                 ('DIC', None, Tkinter.DISABLED),
                 ]

        for name, value, state in hints:
            var = Tkinter.IntVar()
            var.set(value)
            self.hintvars[name] = var
            button = Tkinter.Checkbutton(self.optionsframe, text=name,
                                         variable=var, state=state)
            button.pack(side=TOP, anchor=NW)

    def build_tools(self):
        opts = dict()#indicatoron=0)
        tools = ['Select', 'Color', 'Line', 'Link']

        self.toolvar = Tkinter.StringVar()
        self.toolvar.set('Select')

        for tool in tools:
            button = Tkinter.Radiobutton(self.toolsframe, text=tool,
                                         variable=self.toolvar, value=tool,
                                         command=self.cb_change_tool,
                                         width=10, anchor=W,
                                         **opts)
            button.pack(anchor=NW, side=TOP)


    def cb_change_tool(self, event=None):
        print self.toolvar.get()
    

    def cb_newgame(self, event=None):
        games = self.games.values()
        games.sort(key=lambda g: g['rate'])
        games.reverse()
        for game in games:
            if game['solved'] is None:
                break
        else:
            raise RuntimeError("No more games to play")

        solution = [int(v)-1 if v != '0' else None for v in game['solution']]
        puzzle = [int(v)-1 if v != '0' else None for v in game['puzzle']]
        rate = game['rate']
        gameid = game['id']
        hints = game['hints']
        solvable = game['solvable']

        print 'Puzzle id:   ', gameid
        print 'Puzzle rate: ', rate
        print 'Puzzle hints:', hints
        print 'Solvable    :', solvable

        self.board.load_puzzle(gameid, puzzle, solution)
        self.board.cb_fill_valid_pencil_marks()


    def cb_exit(self, event=None):
        pass

    def load_games(self):
        games = [eval(line) for line in open('games').readlines()]
        #games = [eval(line) for line in open('sample').readlines()]
        games = [(game['id'], game) for game in games]
        random.shuffle(games)
        self.games = dict(games)
        # sort games by rate
        solved = len([game for game in games if game[1]['solved'] is not None])
        print 'Solved games %s/%s'%(solved, len(games))

    def save_games(self):
        out = open('games', 'w')
        for game in self.games.values():
            out.write(repr(game)+'\n')



def main():
    root = MainWindow()
    root.setup()
    root.load_games()

    root.cb_newgame()
    
    try:
        root.mainloop()
    finally:
        root.save_games()


if __name__ == '__main__':
    main()
