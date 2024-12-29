import arcade, math, json, tkinter

class DrawingApp(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(title="simulatore della carta in cina",width=880,height=587)
        self.save = []
        self.shapes = []
        self.current_color = arcade.color.BLACK
        self.carta = arcade.load_texture("Assets/carta.jpg")
        self.penna = arcade.load_texture("Assets/penna.png")
        self.tavolo = arcade.load_texture("Assets/tavolo.jpg")
        self.ink = arcade.load_texture("Assets/ink.png")
        self.mano_destra = arcade.load_texture("Assets/mano_destra.png")
        self.mano_sinistra = arcade.load_texture("Assets/mano_sinistra.png")
        self.casa = arcade.load_texture("Assets/casa.jpg")
        self.home = arcade.load_texture("Assets/home.png")
        self.cmano = [self.mano_destra,155,55]
        self.cmano2 = [self.mano_sinistra,205,-55]
        self.drawing = False
        self.set_mouse_visible(False)
        self.pensize = 10
        self.window = self.menu
        self.colors = [
            (arcade.color.BLACK  ,  arcade.key.KEY_1),
            (arcade.color.RED    ,  arcade.key.KEY_2),
            (arcade.color.GREEN  ,  arcade.key.KEY_3),
            (arcade.color.BLUE   ,  arcade.key.KEY_4),
            (arcade.color.YELLOW ,  arcade.key.KEY_5),
            (arcade.color.PURPLE ,  arcade.key.KEY_6),
            (arcade.color.CYAN   ,  arcade.key.KEY_7),
            (arcade.color.ORANGE ,  arcade.key.KEY_8),
            (arcade.color.PINK   ,  arcade.key.KEY_9),
            (arcade.color.BROWN  ,  arcade.key.KEY_0),]
        self.selected = [145, 555]

    def on_draw(self):
        self.window()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.window == self.game:
            self.drawing = True

    def on_mouse_release(self, x, y, button, modifiers):
        if self.window == self.game:
            self.drawing = False
            if 16 < x < 104 and 356 < y < 464 and self.pensize < 15:
                self.pensize += 3
            for i in range(0,10):
                if 145 + 65.7*i - 20 < x < 145 + 65.7*i + 20 and 555-20 < y < 555+20:
                    self.selected[0] = 145 + 65.7 * i
                    self.current_color = self.colors[i][0]
            if 17 < x < 123 and 227 < y < 333:
                self.cmano,self.cmano2 = self.cmano2,self.cmano
            if 787 < x < 853 and 387 < y < 453:
                self.window = self.menu
        elif self.window == self.menu:
            if 265 < self._mouse_x < 615 and 263 < self._mouse_y < 363:
                self.window = self.game
            if 265 < self._mouse_x < 615 and 123 < self._mouse_y < 223:
                self.window = self.chisiamo
        elif self.window == self.chisiamo:
            if 787 < x < 853 and 387 < y < 453:
                self.window = self.menu
    def on_key_press(self, key, modifiers):
        if self.window == self.game:
            for i in range(10):
                if key == self.colors[i][1]:
                    self.selected[0] = 145 + 65.7 * i
                    self.current_color = self.colors[i][0]
            if key == arcade.key.R:
                self.shapes = []
            if key == arcade.key.I and self.pensize < 15:
                self.pensize += 3
            if key == arcade.key.S:
                self.saving()
            #if key == arcade.key.O:
            #    self.opening()
            if key == arcade.key.M:
                self.cmano2,self.cmano = self.cmano,self.cmano2
        elif self.window == self.menu:
            print(self.home.width/15,self.home.height/15)
            if key == arcade.key.A:
                self.window = self.game
    def menu(self):
        colorrect1 = arcade.color.WHITE
        colorrect2 = arcade.color.WHITE
        if 265 < self._mouse_x < 615 and 263 < self._mouse_y < 363:
            colorrect1 = arcade.color.GREEN
        if 265 < self._mouse_x < 615 and 123 < self._mouse_y < 223:
            colorrect2 = arcade.color.GREEN
        arcade.start_render()
        arcade.draw_texture_rectangle(450, 300, self.casa.width, self.casa.height, self.casa)
        arcade.draw_text("powered by VIKONAD", 15, 15, arcade.color.WHITE, 15,bold=True,font_name=("courier", "arial"))
        arcade.draw_rectangle_outline(880/2,587/2+20,350,100,colorrect1,10)
        arcade.draw_rectangle_outline(880/2,587/2-120,350,100,colorrect2,10)
        arcade.draw_text("Inizia", 880/2-65,587/2+5, colorrect1, 40,bold=True,font_name=("courier", "arial"))
        arcade.draw_text("Chi siamo", 880/2-130,587/2-140, colorrect2, 40,bold=True,font_name=("courier", "arial"))
        arcade.draw_texture_rectangle(self._mouse_x+self.cmano[2], self._mouse_y+self.penna.height/2-10, self.penna.width, self.penna.height, self.penna, self.cmano[1])

    def game(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(450, 300, self.tavolo.width, self.tavolo.height, self.tavolo)
        arcade.draw_texture_rectangle(880/2, 0, self.carta.width, self.carta.height*2, self.carta,90)
        arcade.draw_texture_rectangle(60, 420, self.ink.width/5, self.ink.height/5, self.ink)
        arcade.draw_texture_rectangle(820, 420, self.home.width/5, self.home.height/5, self.home)
        arcade.draw_texture_rectangle(70,280,self.mano_destra.width/15,self.mano_destra.height/15,self.cmano[0])
        arcade.draw_text("powered by VIKONAD", 15, 15, arcade.color.BLACK, 15,bold=True,font_name=("courier", "arial"))

        if self.drawing and self.pensize > 0 and 125 < self._mouse_x < 754 and self._mouse_y < 500:
            self.pensize -= 0.06
            self.shapes.append(arcade.create_ellipse_filled(self._mouse_x, self._mouse_y, math.ceil(self.pensize), math.ceil(self.pensize), self.current_color))
            self.save.append([self._mouse_x,self._mouse_y,math.ceil(self.pensize),self.current_color])

        arcade.draw_rectangle_filled(self.selected[0],self.selected[1],50,50,arcade.color.WHITE)

        for i in range(0,10):
            arcade.draw_rectangle_filled(145 + 65.7 * i, 555, 40, 40, self.colors[i][0])

        for shape in self.shapes:
            shape.draw()

        arcade.draw_text(f"Inchiostro: {math.ceil(self.pensize*10)}%", 125,510, arcade.color.WHITE, 10,bold=True,font_name=("courier", "arial"))

        arcade.draw_texture_rectangle(self._mouse_x+self.cmano[2], self._mouse_y+self.penna.height/2-10, self.penna.width, self.penna.height, self.penna, self.cmano[1])
        arcade.create_ellipse_filled(self._mouse_x, self._mouse_y, self.pensize, self.pensize, self.current_color).draw()

        if self.pensize > 0:
            self.pensize -= 0.0003
        
    def chisiamo(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(450, 300, self.tavolo.width, self.tavolo.height, self.tavolo)
        arcade.draw_texture_rectangle(820, 420, self.home.width/5, self.home.height/5, self.home)
        arcade.draw_texture_rectangle(880/2, 0, self.carta.width, self.carta.height*2, self.carta,90)
        arcade.draw_text("3N", 135,470, arcade.color.BLACK, 20,bold=True,font_name=("courier", "arial"))
        arcade.draw_text("30/01/24", 635,470, arcade.color.BLACK, 20,bold=True,font_name=("courier", "arial"))
        arcade.draw_text("Valentin Baltag Rares", 165,350, arcade.color.BLACK, 40,bold=True,font_name=("courier", "arial"))
        arcade.draw_text("Alessandro Mezetti", 165,250, arcade.color.BLACK, 40,bold=True,font_name=("courier", "arial"))
        arcade.draw_text("Arash Momeni", 165,150, arcade.color.BLACK, 40,bold=True,font_name=("courier", "arial"))
        arcade.draw_text("powered by VIKONAD", 15, 15, arcade.color.BLACK, 15,bold=True,font_name=("courier", "arial"))

        arcade.draw_texture_rectangle(self._mouse_x+self.cmano[2], self._mouse_y+self.penna.height/2-10, self.penna.width, self.penna.height, self.penna, self.cmano[1])
    
    def saving(self):
        def on_submit():
            input_text = entry.get()
            with open(f"Disegni Salvati/{input_text}.json", "w") as file:
                json.dump(self.save,file,indent=4)

        root = tkinter.Tk()
        root.title("salva il tuo disegno")
        root.geometry("250x80")
        label = tkinter.Label(root, text="metti un nome per il tuo disegno:")
        label.pack()
        entry = tkinter.Entry(root)
        entry.pack()
        submit_button = tkinter.Button(root, text="Salva", command=on_submit)
        submit_button.pack()
        root.mainloop()

def main():
    window = DrawingApp(800, 600, "DrawingApp")
    arcade.run()

if __name__ == "__main__":
    main()
