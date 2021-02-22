import turtle
import tkinter
from tkinter import ttk

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
CreateNewWire = True
new_wire = None


class LogicGate:

    def __init__(self, gate_type):
        global gates
        self.t = turtle.Turtle()
        self.t.penup()
        self.t.speed(-1)
        self.t.setpos(250, 250)
        if gate_type == 1:
            self.state = False
        else:
            self.state = None
        self.parents = []
        self.children = []
        self.type = gate_type
        self.shape_change()
        gates.append(self)
        mouse_mode(mode)

    def ping(self):
        for i in self.children:
            i.update()

    def update(self, xdummy=None, ydummy=None):
        values = [i.state for i in self.parents]

        def xor(pointer=0, result=0):
            if pointer < len(values):
                return xor(pointer + 1, values[pointer] ^ result)
            else:
                return result

        if self.type == 1:
            self.state = not self.state
            self.shape_change()
            self.ping()

        if self.type == 2:
            if len(values) == 1:
                if values[0] is not None:
                    self.state = not values[0]
                else:
                    self.state = None
            else:
                self.state = None
            self.shape_change()
            self.ping()

        if self.type == 3:
            if len(values) > 1:
                self.state = any(values)
            else:
                self.state = None
            self.shape_change()
            self.ping()

        if self.type == 4:
            if len(values) > 1:
                self.state = all(values)
            else:
                self.state = None
            self.shape_change()
            self.ping()

        if self.type == 5:
            if len(self.parents) == 2:
                self.state = xor()
            else:
                self.state = None
            self.shape_change()
            self.ping()

        if self.type == 6:
            if len(self.parents) == 1:
                self.state = values[0]
            else:
                self.state = None
            self.shape_change()
            self.ping()

    def shape_change(self):
        if self.type == 1:
            if self.state:
                self.t.shape('Sprites/inp_box_on.gif')
            else:
                self.t.shape('Sprites/inp_box_off.gif')

        elif self.type == 2:
            if self.state is None:
                self.t.shape('Sprites/not_gate_none.gif')
            elif self.state:
                self.t.shape('Sprites/not_gate_on.gif')
            else:
                self.t.shape('Sprites/not_gate_off.gif')

        elif self.type == 3:
            if self.state is None:
                self.t.shape('Sprites/or_gate_none.gif')
            elif self.state:
                self.t.shape('Sprites/or_gate_on.gif')
            else:
                self.t.shape('Sprites/or_gate_off.gif')

        elif self.type == 4:
            if self.state is None:
                self.t.shape('Sprites/and_gate_none.gif')
            elif self.state:
                self.t.shape('Sprites/and_gate_on.gif')
            else:
                self.t.shape('Sprites/and_gate_off.gif')

        elif self.type == 5:
            if self.state is None:
                self.t.shape('Sprites/xor_gate_none.gif')
            elif self.state:
                self.t.shape('Sprites/xor_gate_on.gif')
            else:
                self.t.shape('Sprites/xor_gate_off.gif')

        elif self.type == 6:
            if self.state is None:
                self.t.shape('Sprites/out_box_none.gif')
            elif self.state:
                self.t.shape('Sprites/out_box_on.gif')
            else:
                self.t.shape('Sprites/out_box_off.gif')

    def delete(self, xdummy=None, ydummy=None):
        if mode == 2:
            self.t.hideturtle()
            for i in self.parents:
                i.delete()
            for i in self.children:
                i.delete()
            del self

    def dragging(self, x, y):
        if mode == 1 and self.parents == [] and self.children == []:
            self.t.ondrag(None)
            self.t.setheading(self.t.towards(x, y))
            self.t.goto(x, y)
            self.t.ondrag(self.dragging)

    def wiring(self, x, y):
        onmove(screen, None)
        #print("wiring")
        x1, y1 = new_wire.start
        # print('old coords overwritten')
        canvas.coords(new_wire.line, x1, y1, x, y)
        # print('line modified')
        onmove(screen, self.wiring)

    def pin_wire(self, x, y):
        global new_wire
        onmove(screen, None)
        # print('pin_wire')
        if new_wire is None and self.type != 6:
            #print('creating wire')
            new_wire = Wire()
            if self.t.ycor() > y:
                #print('make wire as parent')
                self.parents.append(new_wire)
                new_wire.child = self
            elif y > self.t.ycor():
                #print('make wire as child')
                self.children.append(new_wire)
                new_wire.parent = self
            # print('wire created')
            new_wire.start = x, y
            # print('first cords written to a wire')
            new_wire.line = canvas.create_line(x, y, x, y, width=5)
            # print('line created')
            onmove(screen, self.wiring)
        else:
            if self.t.ycor() > y and new_wire.child is None and self.type != 1:
                self.parents.append(new_wire)
                #print('make wire as a parent')
                new_wire.child = self
                new_wire.update()
                new_wire.ping()
                self.update()
                self.ping()
                onmove(screen, None)
            elif y > self.t.ycor() and new_wire.parent is None and self.type != 1:
                self.children.append(new_wire)
                #print('make wire as a child')
                new_wire.parent = self
                new_wire.update()
                new_wire.ping()
                self.update()
                self.ping()
                onmove(screen, None)
            else:
                new_wire.delete()
            new_wire = None


class Wire:

    def __init__(self):
        self.parent = None
        self.child = None
        self.state = None
        self.start = None
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
        if self.child is not None and self.child.type != 1:
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
        canvas.coords(self.line, 0, 0, 0, 0)
        canvas.itemconfig(self.line, fill='gray')
        try:
            if self.parent is not None:
                self.parent.children.remove(self)
            if self.child is not None:
                self.child.parents.remove(self)
        except ValueError:
            pass
        self.ping()
        del self


def onmove(self, fun, add=None):

    if fun is None:
        self.cv.unbind('<Motion>')
    else:
        def eventfun(event):
            fun(self.cv.canvasx(event.x) / self.xscale, -self.cv.canvasy(event.y) / self.yscale)
        self.cv.bind('<Motion>', eventfun, add)


def create_object():
    choice = menu.get()
    new_object = True

    if choice == 'Input box':
        LogicGate(1)

    elif choice == 'NOT gate':
        LogicGate(2)

    elif choice == 'OR gate':
        LogicGate(3)

    elif choice == 'AND gate':
        LogicGate(4)

    elif choice == 'XOR gate':
        LogicGate(5)

    elif choice == 'Indicator':
        LogicGate(6)

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
        i.t.onrelease(None)
    onmove(screen, None)

    if mode == 0:

        for i in gates:
            if i.type == 1:
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
            i.t.onclick(i.pin_wire)

        canvas.master.config(cursor='Pencil')


screen = turtle.Screen()
screen.title('Bitwise sandbox')
screen.setup(width=1.0, height=1.0, startx=None, starty=None)
screen.bgcolor('gray')
screen.setworldcoordinates(0, 845, 1536, 0)

canvas = screen.getcanvas()

btn_std_mode = tkinter.Button(canvas.master, text='0', cursor='arrow', command=lambda: mouse_mode(0))
btn_drag_mode = tkinter.Button(canvas.master, text='1', cursor='arrow', command=lambda: mouse_mode(1))
btn_del_mode = tkinter.Button(canvas.master, text='2', cursor='arrow', command=lambda: mouse_mode(2))
btn_wire_mode = tkinter.Button(canvas.master, text='3', cursor='arrow', command=lambda: mouse_mode(3))
btn_create = tkinter.Button(canvas.master, text="Create", cursor='arrow', command=create_object)
menu = ttk.Combobox(canvas.master, cursor='arrow', values=['Input box', 'NOT gate', 'OR gate', 'AND gate', 'XOR gate',
                                                           'Indicator'])

canvas.create_window(225, 10, window=btn_std_mode)
canvas.create_window(250, 10, window=btn_drag_mode)
canvas.create_window(275, 10, window=btn_del_mode)
canvas.create_window(300, 10, window=btn_wire_mode)
canvas.create_window(175, 10, window=btn_create)
canvas.create_window(75, 10, window=menu)

screen.mainloop()

"""
mode 0:
    onclick:
        gate - change state if inp_box, else nothing
    ondrag:
        nothing
mode 1:
    onclick:
        gate - if no wires connected, bind self ondrag to dragging, else nothing
    ondrag:
        gate - if binded exec dragging else nothing
mode 2:
    onclick:
        gate - delete self, parental and childish wires
    ondrag:
        nothing
mode 3:
    onclick:
        gate - bind self ondrag to wiring
    ondrag:
        gate - wiring
"""
