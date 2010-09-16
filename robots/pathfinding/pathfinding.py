

from Tkinter import *
from TkExtra import *
import random
import math
import numpy


class Stack(list):
    push = list.append


class Queue(list):
    def key(self, item):
        return item.heuristic
    
    def push(self, item):
        self.append(item)
        self.sort(key=self.key)
        
    pop = lambda self: list.pop(self, 0)


class Cell(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.data = None

        self.wall = False

        self.visited = False
        self.previous = None
        self.heuristic = 0
        self.dist = 'inf'

        self._c = False

    def __repr__(self):
        return "<Cell (%s, %s), dist=%s>"%(self.x, self.y, self.dist)

    def mark(self):
        self.visited = True
        
    def reset_search(self):
        self.visited = False
        self.previous = None
        self.heuristic = 0
        self.dist = 'inf'

    def get_children(self):
        neighbors = [(x, y) for x in xrange(self.x-1, self.x+2)
                            for y in xrange(self.y-1, self.y+2)
                            if (x, y) != (self.x, self.y)
                            and
                            (0 <= x < self.w)
                            and
                            (0 <= y < self.h)]

        return neighbors
            
    def distance(self, dest):
        sx, sy = self.x, self.y
        dx, dy = dest.x, dest.y
        return math.hypot(sx-dx, sy-dy)

    def complexh(self, other, dest):
        sx, sy = self.x, self.y
        ox, oy = other.x, other.y
        dx, dy = dest.x, dest.y

        h = 0

        d1 = abs(dx - ox)
        d2 = abs(dx - sx)
        if d1 < d2:
            h -= 1
        if d1 > d2:
            h += 1

        d1 = abs(dy - oy)
        d2 = abs(dy - sy)
        if d1 < d2:
            h -= 1
        if d1 > d2:
            h += 1

        return h


class Graph(object):
    # use a matrix
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[Cell(x, y, width, height) for y in xrange(height)]
                     for x in xrange(width)]

        self.src = None
        self.dest = None

    def set_screen(self, n, s_call, d_call, w_call):
        w, h = self.width, self.height

        self.src = self.data[random.randint(0, w-1)][random.randint(0, h-1)]
        s_call(self.src.x, self.src.y)

        self.dest = self.data[random.randint(0, w-1)][random.randint(0, h-1)]
        d_call(self.dest.x, self.dest.y)

        # random walls
        return
        for i in xrange(n):
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            if (x, y) == (self.src.x, self.src.y) or (x, y) == (self.dest.x, self.dest.y):
                continue
            self.data[x][y].wall = True
            w_call(x, y)

    def reset_screen(self, call):
        for x in xrange(self.width):
            for y in xrange(self.height):
                self.data[x][y].wall = False
                self.data[x][y].data = None
                call(x, y)

        self.src = None
        self.dest = None
        
    def set(self, x, y, call):
        self.data[x][y].value = 1
        call(x, y)

    def clear(self, x, y, call):
        self.data[x][y].value = None
        call(x, y)

    def set_src(self, x, y, call, clear):
        if self.src is not None:
            clear(self.src.x, self.src.y)
        self.src = self.data[x][y]
        call(x, y)

    def set_dest(self, x, y, call, clear):
        if self.dest is not None:
            clear(self.dest.x, self.dest.y)
        self.dest = self.data[x][y]
        call(x, y)

    def set_wall(self, x, y, call):
        if not self.data[x][y].wall:
            self.data[x][y].wall = True
            call(x, y)

    def bfs_search(self, call=None):
        if self.src is None:
            yield None
        
        for column in self.data:
            for row in column:
                row.reset_search()

        path = []
        queue = Queue()
        queue.push(self.src)
        self.src.mark()
        while queue:
            cell = queue.pop()
            if cell is self.dest:
                break
            for x, y in cell.get_children():
                child = self.data[x][y]
                if not child.visited and not child.wall:
                    # A* uses both distance and complex heuristic for
                    # weighting
                    child.heuristic = cell.complexh(child, self.dest) + child.distance(self.dest)

                    child.previous = cell
                    child.mark()
                    queue.push(child)
                    
                    if call is not None:
                        call(cell.x, cell.y, child.x, child.y)
                    
        else:
            print "path not found"
            yield None

        cell = self.dest
        while cell is not None:
            path.append(cell)
            cell = cell.previous

        for c in reversed(path):
            yield [c.x, c.y]


    def _dijkstra_search(self, call=None):

        if self.src is None:
            yield None

        
        dists = numpy.array([[c.dist for c in col] for col in self.data])
        

        print dists


    def dijkstra_search(self, call=None):

        if self.src is None:
            yield None

        for column in self.data:
            for row in column:
                row.reset_search()
                
        # cache all items to ease choosing the best vertex
        Q = reduce(list.__add__, self.data)

        self.src.dist = 0


        def _pop_vertex(data):
            c = 0
            m = 'inf'
            for i, cell in enumerate(data):
                if cell.dist < m:
                    m = cell.dist
                    c = i
            return data.pop(c)

        def pop_vertex(data):
            return data.pop(data.index(min(data, key=lambda cell: cell.dist)))

        def pop_vertex(data):
            data.sort(key=lambda cell: cell.dist)
            return data.pop(0)
                    
        # while we have vertexes to choose from...
        run = True
        while Q and run:
            # find the best vertex... on first run it will be self.src
            # with dist=0
            current = pop_vertex(Q)
            current.mark()

            if current.dist == 'inf':
                break

            if current.previous != None:
                call(current.previous.x, current.previous.y,
                     current.x, current.y)
                
            
            
            children = [self.data[x][y] for x, y in current.get_children()]
            children = [child for child in children if not child.wall]
            for child in children:
                alt = current.distance(child)+current.dist
                if alt < child.dist:
                    child.previous = current
                    child.dist = alt
                if child is self.dest:
                    run = False
                    break


        path = []
        cell = self.dest
        while cell is not self.src and cell is not None:
            #print cell
            path.append(cell)
            cell = cell.previous

        path.append(self.src)
        
        for c in reversed(path):
            yield [c.x, c.y]

            
        
class Screen(Canvas):
    def __init__(self, parent, graph, cellsize=1, *args, **kwds):
        self.graph = graph
        self.cellsize = cellsize
        width = self.cellsize*graph.width +1
        height = self.cellsize*graph.height +1
        Canvas.__init__(self, parent, width=width, height=height,
                        *args, **kwds)

        self.tiles = [([None]*graph.height) for x in xrange(graph.width)]
        self.draw_tilemap()

        self.pathline = None
        self.tmplines = []

        self.bind("<Button-1>", self.event_set_wall)
        self.bind("<Button1-Motion>", self.event_set_wall)

        self.bind("<Control-Button-1>", self.event_set_src)
        self.bind("<Shift-Button-1>", self.event_set_dest)
        
        
    def draw_tilemap(self):
        for x in xrange(self.graph.width):
            x1 = x*self.cellsize+1
            x2 = x1+self.cellsize
            for y in xrange(self.graph.height):
                y1 = y*self.cellsize+1
                y2 = y1+self.cellsize
                tag = self.create_rectangle((x1, y1, x2, y2), stipple="gray50",
                                            outline="black")
                self.tiles[x][y] = tag

    def coord2cell(self, x, y):
        x = int(self.canvasx(x)//self.cellsize)
        y = int(self.canvasy(y)//self.cellsize)
        return x, y

    def event_set_wall(self, event=None):
        x, y = self.coord2cell(event.x, event.y)
        self.graph.set_wall(x, y, self.wall_set)

    def event_set_src(self, event=None):
        x, y = self.coord2cell(event.x, event.y)
        self.graph.set_src(x, y, self.src_set, self.clear)
        if self.pathline is not None:
            self.clear_path()

    def event_set_dest(self, event=None):
        x, y = self.coord2cell(event.x, event.y)
        self.graph.set_dest(x, y, self.dest_set, self.clear)
        if self.pathline is not None:
            self.clear_path()

    def clear_wall(self, event=None):
        pass

    def reset(self, event=None):
        self.clear_path()
        self.graph.reset_screen(self.clear)

    def redraw(self, event=None):
        self.reset()
        self.graph.set_screen(self.graph.width*self.graph.height//2, self.src_set, self.dest_set, self.wall_set)

    def wall_set(self, x, y):
        self.itemconfig(self.tiles[x][y], fill="black", stipple='')
    
    def src_set(self, x, y):
        self.itemconfig(self.tiles[x][y], fill="red", stipple="gray50")

    def dest_set(self, x, y):
        self.itemconfig(self.tiles[x][y], fill="green", stipple="gray50")

    def clear(self, x, y):
        self.itemconfig(self.tiles[x][y], fill='', stipple="gray50")

    def clear_path(self):
        self.delete(self.pathline)
        self.pathline = None
        while self.tmplines:
            self.delete(self.tmplines.pop())

    def draw_tmpline(self, *coords):
        coords = map(self.ctrans, coords)
        self.tmplines.append(self.create_line(coords, arrow=LAST, fill='red'))

    def path_set(self, *coords):
        pass

    def ctrans(self, v):
        return v*self.cellsize + self.cellsize//2
        
    def search(self, func):
        path = func(self.draw_tmpline)
        start = path.next()
        if start is None:
            return

        if self.pathline:
            self.clear_path()

        coords = map(self.ctrans, start)
                     
        self.pathline = self.create_line(coords[0], coords[1],
                                         coords[0], coords[1], arrow=LAST, fill='green', width=3)

        for cell in path:
            coords.extend(map(self.ctrans, cell))
            self.coords(self.pathline, *coords)


    def bfs_search(self):
        self.search(self.graph.bfs_search)

    def dijkstra_search(self):
        self.search(self.graph.dijkstra_search)
        


class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.build()


    def build(self):
        self.toolbar = ButtonBar(self)
        self.toolbar.pack(expand=1, fill=X)

        self.graph = Graph(60, 40)
        #self.graph = Graph(10, 10)
        self.screen = Screen(self, self.graph, bg="white", cellsize=20)
        self.screen.pack(expand=1, fill=BOTH)

        self.toolbar.add_button(0, text="Reset", command=self.screen.reset)
        self.toolbar.add_button(0, text="Redraw", command=self.screen.redraw)
        self.toolbar.add_button(1, text="A*", command=self.screen.bfs_search)
        self.toolbar.add_button(1, text="Dijkstra", command=self.screen.dijkstra_search)
        

if __name__ == '__main__':
    root = MainWindow()
    root.mainloop()

