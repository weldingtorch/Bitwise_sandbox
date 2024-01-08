import turtle
import tkinter
from tkinter import ttk
from threading import Thread
from time import sleep


turtle.register_shape("Sprites/and_gate_off.gif")
turtle.register_shape("Sprites/and_gate_on.gif")
turtle.register_shape("Sprites/and_gate_none.gif")

turtle.register_shape("Sprites/not_gate_off.gif")
turtle.register_shape("Sprites/not_gate_on.gif")
turtle.register_shape("Sprites/not_gate_none.gif")

turtle.register_shape("Sprites/or_gate_off.gif")
turtle.register_shape("Sprites/or_gate_on.gif")
turtle.register_shape("Sprites/or_gate_none.gif")

turtle.register_shape("Sprites/xor_gate_off.gif")
turtle.register_shape("Sprites/xor_gate_on.gif")
turtle.register_shape("Sprites/xor_gate_none.gif")

turtle.register_shape("Sprites/inp_box_off.gif")
turtle.register_shape("Sprites/inp_box_on.gif")

turtle.register_shape("Sprites/out_box_off.gif")
turtle.register_shape("Sprites/out_box_on.gif")
turtle.register_shape("Sprites/out_box_none.gif")

mode = 0
gates = []
new_wire = None
queue = []


def execute_queue():
    global queue
    lines_executed = 0
    while True:
        if len(queue):
            queue.pop(0)()
            lines_executed += 1
            print(lines_executed)
        else:
            sleep(0.25)


class LogicGate:
    def __init__(self):
        global gates

        self.t = turtle.Turtle(visible=False)
        self.t.penup()
        self.t.speed(-1)
        self.t.setpos(250, 250)

        self.parents = []
        self.children = []
        self.state = None
        self.prev_values = []

        self.shape_change()
        self.t.showturtle()
        gates.append(self)

        mouse_mode(mode)

    def update(self, xdummy=None, ydummy=None):
        values = [par.state for par in self.parents]
        if self.prev_values != values:
            self.prev_values = values
            return values
        return None

    def ping(self):
        for i in self.children:
            queue.append(i.update)

    def shape_change(self):
        pass

    def delete(self, xdummy=None, ydummy=None):
        if mode == 2:
            self.t.hideturtle()
            for i in self.parents:
                i.delete()
            for i in self.children:
                i.delete()
            gates.remove(self)
            del self

    def dragging(self, x, y):
        if mode == 1 and self.parents == [] and self.children == []:
            self.t.ondrag(None)  # посмотреть что будет если убрать эту строку и ниже
            self.t.setheading(self.t.towards(x, y))
            self.t.goto(x, y)
            self.t.ondrag(self.dragging)

    def first_pin_wire(self, x, y):
        global new_wire
        # print('first_pin_wire')
        # print('creating wire')
        new_wire = Wire()
        if self.t.ycor() > y:
            # print('make wire as parent')
            self.parents.append(new_wire)
            new_wire.child = self
        elif y > self.t.ycor():
            # print('make wire as child')
            self.children.append(new_wire)
            new_wire.parent = self
        else:
            # print("wire deleted")
            new_wire.delete()
            return -1
        # print('wire created')
        new_wire.line = canvas.create_line(x, y, x, y, width=5)
        # print('line created')
        mouse_mode(4)

    def second_pin_wire(self, x, y):
        global new_wire
        # print("second pin")
        if self.t.ycor() > y and new_wire.child is None:
            self.parents.append(new_wire)
            #print('make wire as a parent')
            canvas.coords(new_wire.line, *canvas.coords(new_wire.line)[:2], x, y)
            new_wire.child = self
            new_wire.update()
        elif y > self.t.ycor() and new_wire.parent is None:
            self.children.append(new_wire)
            #print('make wire as a child')
            canvas.coords(new_wire.line, *canvas.coords(new_wire.line)[:2], x, y)
            new_wire.parent = self
            self.update()
        else:
            new_wire.delete()
        new_wire = None
        mouse_mode(3)
"""
    def wiring(self, x1, y1):
        self.t.ondrag(None)
        # print("wiring")
        x0, y0 = canvas.coords(new_wire.line)[:2]
        # print('got line's first point coords')
        canvas.coords(new_wire.line, x0, y0, x1, y1)
        # print('line modified')
        self.t.ondrag(self.wiring)
"""


class InputBox(LogicGate):
    def __init__(self):
        super().__init__()
        self.state = False

    def update(self, xdummy=None, ydummy=None):
        self.state = not self.state
        self.shape_change()
        self.ping()

    def shape_change(self):
        if self.state:
            self.t.shape('Sprites/inp_box_on.gif')
        else:
            self.t.shape('Sprites/inp_box_off.gif')

    def first_pin_wire(self, x, y):
        global new_wire
        # print('first_pin_wire')
        # print('creating wire')
        new_wire = Wire()
        if y > self.t.ycor():
            # print('make wire as child')
            self.children.append(new_wire)
            new_wire.parent = self
        else:
            # print("wire deleted")
            new_wire.delete()
            return -1
        # print('wire created')
        new_wire.line = canvas.create_line(x, y, x, y, width=5)
        # print('line created')
        mouse_mode(4)

    def second_pin_wire(self, x, y):
        global new_wire
        # print("second pin")
        if y > self.t.ycor() and new_wire.parent is None:
            self.children.append(new_wire)
            # print('make wire as a child')
            canvas.coords(new_wire.line, *canvas.coords(new_wire.line)[:2], x, y)
            new_wire.parent = self
            self.update()
        else:
            new_wire.delete()
        new_wire = None
        mouse_mode(3)


class NotGate(LogicGate):
    def update(self, xdummy=None, ydummy=None):
        values = super().update()

        if values is not None:
            if len(values) == 1 and values[0] is not None:
                self.state = not values[0]
            else:
                self.state = None
            self.shape_change()
            self.ping()

    def shape_change(self):
        if self.state is None:
            self.t.shape('Sprites/not_gate_none.gif')
        elif self.state:
            self.t.shape('Sprites/not_gate_on.gif')
        else:
            self.t.shape('Sprites/not_gate_off.gif')


class OrGate(LogicGate):
    def update(self, xdummy=None, ydummy=None):
        values = super().update()

        if values is not None:
            if len(values) > 1 and None not in values:
                self.state = any(values)
            else:
                self.state = None
            self.shape_change()
            self.ping()

    def shape_change(self):
        if self.state is None:
            self.t.shape('Sprites/or_gate_none.gif')
        elif self.state:
            self.t.shape('Sprites/or_gate_on.gif')
        else:
            self.t.shape('Sprites/or_gate_off.gif')


class AndGate(LogicGate):
    def update(self, xdummy=None, ydummy=None):
        values = super().update()

        if values is not None:
            if len(values) > 1 and None not in values:
                self.state = all(values)
            else:
                self.state = None
            self.shape_change()
            self.ping()

    def shape_change(self):
        if self.state is None:
            self.t.shape('Sprites/and_gate_none.gif')
        elif self.state:
            self.t.shape('Sprites/and_gate_on.gif')
        else:
            self.t.shape('Sprites/and_gate_off.gif')


class XorGate(LogicGate):
    def update(self, xdummy=None, ydummy=None):
        values = super().update()

        if values is not None:
            if len(values) >= 2 and None not in values:
                result = 0
                for value in values:
                    result ^ value
                
                self.state = result
            else:
                self.state = None
            self.shape_change()
            self.ping()

    def shape_change(self):
        if self.state is None:
            self.t.shape('Sprites/xor_gate_none.gif')
        elif self.state:
            self.t.shape('Sprites/xor_gate_on.gif')
        else:
            self.t.shape('Sprites/xor_gate_off.gif')


class OutputBox(LogicGate):
    def update(self, xdummy=None, ydummy=None):
        values = super().update()

        if values is not None:
            if len(values) == 1:
                self.state = values[0]
            else:
                self.state = None
            self.shape_change()
            self.ping()

    def shape_change(self):
        if self.state is None:
            self.t.shape('Sprites/out_box_none.gif')
        elif self.state:
            self.t.shape('Sprites/out_box_on.gif')
        else:
            self.t.shape('Sprites/out_box_off.gif')

    def first_pin_wire(self, x, y):
        global new_wire
        # print('first_pin_wire')

        # print('creating wire')
        new_wire = Wire()
        if self.t.ycor() > y:
            # print('make wire as parent')
            self.parents.append(new_wire)
            new_wire.child = self
        else:
            # print("wire deleted")
            new_wire.delete()
            return -1
        # print('wire created')
        new_wire.line = canvas.create_line(x, y, x, y, width=5)
        # print('line created')
        mouse_mode(4)

    def second_pin_wire(self, x, y):
        global new_wire
        # print("second pin")
        if self.t.ycor() > y and new_wire.child is None:
            self.parents.append(new_wire)
            # print('make wire as a parent')
            canvas.coords(new_wire.line, *canvas.coords(new_wire.line)[:2], x, y)
            new_wire.child = self
            new_wire.update()
        else:
            new_wire.delete()
        mouse_mode(3)
        new_wire = None


class Wire:
    def __init__(self):
        self.parent = None
        self.child = None
        self.state = None
        self.line = None
        self.update()

    def update(self):
        if self.parent is not None:
            self.state = self.parent.state
        else:
            self.state = None
        self.change_shape()
        self.ping()

    def ping(self):
        if self.child is not None:
            self.child.update()

    def change_shape(self):
        if self.state is None:
            color = '#9FA8B5'
        elif self.state:
            color = 'green'
        else:
            color = 'red'
        canvas.itemconfig(self.line, fill=color)

    def delete(self):
        try:
            canvas.coords(self.line, 0, 0, 0, 0)
            canvas.itemconfig(self.line, fill='gray')
        except :
            pass

        try:
            self.parent.children.remove(self)
        except (ValueError, AttributeError):
            pass

        try:
            self.child.parents.remove(self)
            self.child.update()
        except (ValueError, AttributeError):
            pass
        finally:
            del self


def create_object():
    choice = menu.get()
    new_object = True

    if choice == 'Input box':
        InputBox()

    elif choice == 'NOT gate':
        NotGate()

    elif choice == 'OR gate':
        OrGate()

    elif choice == 'AND gate':
        AndGate()

    elif choice == 'XOR gate ':
        XorGate()

    elif choice == 'Output box':
        OutputBox()

    else:
        new_object = False

    if new_object:
        mouse_mode(mode)


def mouse_mode(new_mode):
    global mode
    mode = new_mode
    for i in gates:
        i.t.onclick(None)
        i.t.ondrag(None)

    if mode == 0:
        for i in gates:
            if isinstance(i, InputBox):
                i.t.onclick(i.update)

        canvas.master.config(cursor='arrow')

    elif mode == 1:
        for i in gates:
            i.t.ondrag(i.dragging)

        canvas.master.config(cursor='fleur')

    elif mode == 2:
        for i in gates:
            i.t.onclick(i.delete)

        canvas.master.config(cursor='X_cursor')

    elif mode == 3:
        for i in gates:
            i.t.onclick(i.first_pin_wire)

        canvas.master.config(cursor='Pencil')

    elif mode == 4:
        for i in gates:
            i.t.onclick(i.second_pin_wire)

        canvas.master.config(cursor='Pencil')

    else:
        mouse_mode(1)


screen = turtle.Screen()
screen.title('Bitwise sandbox')
screen.setup(width=1.0, height=1.0, startx=None, starty=None)
screen.bgcolor('gray')
screen.setworldcoordinates(0, 845, 1536, 0)

canvas = screen.getcanvas()

btn_tgl_mode = tkinter.Button(canvas.master, text='Toggle', cursor='arrow', command=lambda: mouse_mode(0))
btn_mv_mode = tkinter.Button(canvas.master, text='Move', cursor='arrow', command=lambda: mouse_mode(1))
btn_del_mode = tkinter.Button(canvas.master, text='Delete', cursor='arrow', command=lambda: mouse_mode(2))
btn_wire_mode = tkinter.Button(canvas.master, text='Wire', cursor='arrow', command=lambda: mouse_mode(3))
btn_create = tkinter.Button(canvas.master, text="Create", cursor='arrow', command=create_object)
menu = ttk.Combobox(canvas.master, cursor='arrow', values=['Input box', 'NOT gate', 'OR gate', 'AND gate', 'XOR gate',
                                                           'Output box'])

canvas.create_window(25, 10, window=btn_tgl_mode)
canvas.create_window(75, 10, window=btn_mv_mode)
canvas.create_window(125, 10, window=btn_del_mode)
canvas.create_window(175, 10, window=btn_wire_mode)
canvas.create_window(375, 10, window=btn_create)
canvas.create_window(275, 10, window=menu)


queue_handle = Thread(target=execute_queue, daemon=True)
queue_handle.start()
screen.mainloop()
