import pygame
from pygame.locals import *

from lib.BaseScene import BaseScene

from lib.Math.Vector import Vector2

from lib.HUD.Canvas import Canvas
from lib.HUD.Button import Button
from lib.HUD.Label import Label
from lib.HUD.RoundedRect import RoundedRect

from Calculator.parser import NumericStringParser       
# from Calculator.Background import Background                

DIGITS_COLORS = {
    'normal'    : (62, 65, 62),
    'hover'     : (62-5, 65-5, 62-5),
    'pressed'   : (62-10, 65-10, 62-10),
    'label'     : (225,255,255),
}
SPECIAL_OPS_COLORS = {
    'normal'    : (94, 96, 93),
    'hover'     : (94-5, 96-5, 93-5),
    'pressed'   : (94-10, 96-10, 93-10),
    'label'     : (225,255,255),
}
OPERATOR_COLORS = {
    'normal'    : (253, 168, 42),
    'hover'     : (253-10, 168-10, 42-10),
    'pressed'   : (253-20, 168-20, 42-20),
    'label'     : (225,255,255),
}
EQUAL_SIGN_COLORS = {
    'normal'    : (251, 141, 6),
    'hover'     : (251-10, 141-10, 0),
    'pressed'   : (251-20, 141-20, 0),
    'label'     : (225,255,255),
}
DEFAULT_COLORS = {
    'normal'    : (0, 225, 225),
    'hover'     : (62-5+50, 65-5+50, 62-5+50),
    'pressed'   : (62-10+50, 65-10+50, 62-10+50),
    'label'     : (225,255,255),
}
    # 'normal'    : (178,34,34),
OFF_COLORS = {
    'normal'    : (178+30,34+10,34+10),
    'hover'     : (178+5,34+5,34+5),
    'pressed'   : (178-20,34+0,34+0),
    'label'     : (225,255,255),
}



class Scene(BaseScene):
    def load(self):
        self.font = pygame.font.Font('Calculator/fonts/Oswald.ttf', 32)

        self.calc = Canvas(self.window, Canvas.TRANSPARENT).set_size_from_ratio(Vector2(0.35,0.9)).center()
        self.background = RoundedRect(self.calc, color=self.options.background.color, radius=self.options.background.radius)
        self.background.set_size_from_ratio(Vector2(1,1)).center().add_to_canvas(self.calc)
        
        self.button_values = [
            'C', '(', ')', 'sin', 'cos',
            'x²', '^', '√', 'log', 'ln',
            '7', '8', '9', 'DEL', 'OFF',
            '4', '5', '6', 'x', '/',
            '1', '2', '3', '+', '-',
            '0', '.', 'π', '='
        ]
        self.buttons = {}
        self.buttons_per_line = 5
        self.buttons_lines = 6

        button_size_as_width = (1-(self.buttons_per_line - 1)*self.options.button.margin - 2 * self.options.side_margin) / self.buttons_per_line
        button_size_as_height = button_size_as_width * self.calc.size.x / self.calc.size.y


        button_bloc_size = self.buttons_lines * button_size_as_height + (self.buttons_lines - 1) * self.options.button.margin
        result_height = 1 - button_bloc_size - 2 * self.options.side_margin - self.options.result_height_spacing

        self.result_rect = RoundedRect(self.calc, color=self.options.result.background, radius=self.options.result.radius).add_to_canvas(self.calc)
        self.result_rect.set_size_from_ratio(Vector2(1-2*self.options.side_margin, result_height)).center_horizontally_ratio(self.options.side_margin)

        rect_rad = 10
        button_margin_as_height =  self.options.button.margin * self.calc.size.x / self.calc.size.y


        for i, char in enumerate(self.button_values):
            row = i // self.buttons_per_line
            col = i % self.buttons_per_line

            button = Button(self.calc, rect_rad, DEFAULT_COLORS, char, self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + col * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + row * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
            if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                button.set_colors(DIGITS_COLORS)
            elif char in ['C', '(', ')', '.', 'π', '^', 'x²', '√', 'log', 'ln', 'cos', 'sin']:
                button.set_colors(SPECIAL_OPS_COLORS)
            elif char in ['+', '-', 'x', '/', 'DEL']:
                button.set_colors(OPERATOR_COLORS)
            elif char == 'OFF':
                button.set_colors(OFF_COLORS)
            elif char == '=':
                button.change_width_ratio(button_size_as_width * 2 + self.options.button.margin)
                button.set_colors(EQUAL_SIGN_COLORS)


            
            self.buttons[char] = button


        # Texte
        self.text_font = pygame.font.Font('Calculator/fonts/Oswald.ttf', 32)
        self.text_canvas = Canvas(self.calc, self.options.result.background).set_size_from_ratio(Vector2(1-2*self.options.side_margin-self.options.text.margin * 2,result_height)).center_point_horizontally_ratio(self.options.side_margin + result_height / 2).add_to_canvas(self.calc)
        
        self.text = Label(self.text_canvas, self.text_font, '0').set_color(self.options.text.color).load().set_size_from_ratio(Vector2(1,1)).fit_height()
        self.text.center().add_to_canvas(self.text_canvas)
        self.text.change_text('')
        self.text.word_wrapping = False

        # Parsing
        self.parser = NumericStringParser()
        self.result_print = False

        # ROW 1
        # Button(self.calc, rect_rad, DIGITS_COLORS, 'C', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 0 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 0 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        # Button(self.calc, rect_rad, DIGITS_COLORS, '+-', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 1 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 0 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        # Button(self.calc, rect_rad, DIGITS_COLORS, '%', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 2 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 0 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        # Button(self.calc, rect_rad, DIGITS_COLORS, '/', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 3 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 0 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
    
        # ROW 2
        # Button(self.calc, rect_rad, DIGITS_COLORS, '7', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 0 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 1 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        # Button(self.calc, rect_rad, DIGITS_COLORS, '8', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 1 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 1 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        # Button(self.calc, rect_rad, DIGITS_COLORS, '9', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 2 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 1 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        # Button(self.calc, rect_rad, DIGITS_COLORS, 'x', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 3 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 1 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)

        # ROW 3
        # Button(self.calc, rect_rad, DIGITS_COLORS, '4', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 0 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 2 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        # Button(self.calc, rect_rad, DIGITS_COLORS, '5', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 1 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 2 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        # Button(self.calc, rect_rad, DIGITS_COLORS, '6', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 2 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 2 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        # Button(self.calc, rect_rad, DIGITS_COLORS, '-', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 3 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 2 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        
        # ROW 4
        # Button(self.calc, rect_rad, DIGITS_COLORS, '1', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 0 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 3 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        # Button(self.calc, rect_rad, DIGITS_COLORS, '2', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 1 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 3 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        # Button(self.calc, rect_rad, DIGITS_COLORS, '3', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 2 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 3 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        # Button(self.calc, rect_rad, DIGITS_COLORS, '+', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 3 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 3 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        
        # ROW 5
        # Button(self.calc, rect_rad, DIGITS_COLORS, '0', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 0 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 4 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        # Button(self.calc, rect_rad, DIGITS_COLORS, '.', self.font).square_from_ratio(button_size_as_width).set_position_ratio(Vector2(self.options.side_margin + 1 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 4 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)
        # Button(self.calc, rect_rad, DIGITS_COLORS, '=', self.font).set_size_from_ratio(Vector2(button_size_as_width * 2 + self.options.button.margin, button_size_as_height)).set_position_ratio(Vector2(self.options.side_margin + 2 * (self.options.button.margin + button_size_as_width),self.options.side_margin + result_height + self.options.result_height_spacing + 4 * (button_margin_as_height + button_size_as_height))).add_to_canvas(self.calc)


        self.calc.load_all()
        # self.background = Background(self.app.options.window.width,self.app.options.window.height)



    def update(self, dt, events):
        for button_char, button in self.buttons.items():
            button.update(events)
            if button.just_released:
                if self.result_print and button_char != 'OFF':
                    if not self.text.text.startswith(' = ') or button_char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        self.text.text = ''
                    else:
                        text = self.text.text[3:]
                        self.text.text = text


                    self.result_print = False
                
                SPACED_OPERATORS = ['+', '-', 'x', '/', '^']
                MATH_FUNCTIONS_CHARS = ['cos', 'sin', 'log', 'ln', '√']
                MATH_FUNCTIONS = ['cos', 'sin', 'log', 'ln', 'Pi', 'sqrt']

                if button_char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '(', ')', 'π']:
                    self.text.text += button_char
                elif button_char in SPACED_OPERATORS:
                    self.text.text += (' ' + button_char + ' ')
                elif button_char in MATH_FUNCTIONS_CHARS:
                    self.text.text += (button_char + '(')
                elif button_char == 'x²':
                    self.text.text += (' ^ 2')
                elif button_char == 'C':
                    self.text.text = ''
                elif button_char == 'OFF':
                    self.continuer = False
                elif button_char == 'DEL' and len(self.text.text) > 0:
                    text = self.text.text.strip()[:-1].strip()
                    if text != '' and text[-1] in SPACED_OPERATORS:
                        text += ' '
                    self.text.text = text

                elif button_char == '=' and self.text.text.strip() != '':
                    expression = self.text.text

                    expression = expression.replace('x', '*')
                    expression = expression.replace(' ', '')
                    expression = expression.replace('π', 'Pi')
                    expression = expression.replace('√', 'sqrt')



                    new_exp = ''
                    for i in range(len(expression) - 1):
                        new_exp += expression[i]
                        if expression[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and expression[i+1] == '(':
                            new_exp += '*'
                    new_exp += expression[-1]
                    

                    for func in MATH_FUNCTIONS:
                        start_search = 0
                        while new_exp.find(func, start_search) != -1:
                            start_index = new_exp.find(func, start_search)
                            if start_index != 0 and new_exp[start_index-1] not in ['+', '-', '*', '/', '(']:
                                L = list(new_exp)
                                L.insert(start_index, '*')
                                new_exp = ''.join(L)

                            start_search += len(func)


                    # Add leading parentheses
                    num_paren = 0
                    for char in new_exp:
                        if char == '(':
                            num_paren += 1
                        elif char == ')':
                            num_paren -= 1
                    if num_paren > 0:
                        new_exp += ')' * num_paren
                    print(new_exp)
                    try:
                        result = str(self.parser.eval(new_exp))
                        if result[-2:] == '.0':
                            result = result[:-2]
                        self.text.text = f' = {result}'
                        pass
                    except Exception as e:
                        print(e)
                        if type(e) == OverflowError:
                            self.text.text = 'RESULT TOO BIG'
                        else:
                            self.text.text = 'ERROR'
                    self.result_print = True
            
                if self.text.font.size(self.text.text)[0] > self.text.size.x:
                    self.text.set_text_align(Label.TEXT_RIGHT)
                else:
                    self.text.set_text_align(Label.TEXT_LEFT)
                self.text.load()

        # self.background.update()


    def physics_update(self, dt):
        pass


    def draw(self, fenetre):
        # self.background.draw(fenetre)
        self.calc.draw()
        # print(self.background)
