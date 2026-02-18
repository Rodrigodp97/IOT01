import pyvisual as pv


def create_page_4_ui(window,ui):
    """
    Create and return UI elements for Page 4.
    :param container: The page widget for Page 4.
    :return: Dictionary of UI elements.
    """
    ui_page = {}
    ui_page["Button_0"] = pv.PvButton(container=window, x=365, y=13, width=292,
        height=75, text='RESULTADOS SECUENCIA', font='assets/fonts/Lexend/Lexend.ttf', font_size=23,
        font_color=(0, 0, 0, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(255, 255, 255, 1), hover_color=None,
        clicked_color=None, border_color=(0, 0, 0, 1), border_hover_color=None, border_thickness=1,
        corner_radius=0, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    ui_page["Icon_1"] = pv.PvIcon(container=window, x=40, y=13, width=73,
        height=75, idle_color=(75, 75, 75, 1), preserve_original_colors=False, icon_path='assets/icons/333e6fa6e1.svg',
        corner_radius=0, flip_v=False, flip_h=False, rotate=0,
        border_color=None, border_hover_color=None, border_thickness=0, border_style="solid",
        on_hover=None, on_click=None, on_release=None, is_visible=True,
        opacity=1, tag=None)

    # Título LITROS FUMIGADOS
    ui_page["Text_3"] = pv.PvText(container=window, x=70, y=150, width=400,
        height=60, idle_color=(255, 255, 255, 0), text='LITROS FUMIGADOS', is_visible=True,
        text_alignment='center', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=29,
        font_color=(0, 0, 0, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=None, corner_radius=0,
        on_hover=None, on_click=None, on_release=None, tag=None)

    # Valor de litros fumigados
    ui_page["TextLitrosValor"] = pv.PvText(container=window, x=120, y=240, width=300,
        height=120, idle_color=(255, 255, 255, 1), text='0.0', is_visible=True,
        text_alignment='center', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=71,
        font_color=(56, 136, 255, 1), bold=True, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=(0, 0, 0, 1), corner_radius=14,
        on_hover=None, on_click=None, on_release=None, tag=None)

    # Depósito de líquido - Fondo (contorno)
    ui_page["DepositoFondo"] = pv.PvRectangle(container=window, x=170, y=390, width=200,
        height=180, idle_color=(220, 220, 220, 1), border_color=(0, 0, 0, 1),
        border_thickness=3, corner_radius=10, is_visible=True, opacity=1,
        on_hover=None, on_click=None, on_release=None, tag=None)
    
    # Depósito de líquido - Nivel (se ajustará dinámicamente)
    ui_page["DepositoNivel"] = pv.PvRectangle(container=window, x=175, y=395, width=190,
        height=170, idle_color=(56, 136, 255, 1), border_color=None,
        border_thickness=0, corner_radius=7, is_visible=True, opacity=0.8,
        on_hover=None, on_click=None, on_release=None, tag=None)
    
    # Texto de capacidad del depósito
    ui_page["TextCapacidad"] = pv.PvText(container=window, x=170, y=365, width=200,
        height=25, idle_color=(255, 255, 255, 0), text='600 L', is_visible=True,
        text_alignment='center', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=16,
        font_color=(100, 100, 100, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=None, corner_radius=0,
        on_hover=None, on_click=None, on_release=None, tag=None)

    # Título ARBOLES CONTADOS
    ui_page["Text_4"] = pv.PvText(container=window, x=554, y=150, width=400,
        height=60, idle_color=(255, 255, 255, 0), text='ARBOLES FUMIGADOS', is_visible=True,
        text_alignment='center', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=29,
        font_color=(0, 0, 0, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=None, corner_radius=0,
        on_hover=None, on_click=None, on_release=None, tag=None)

    # Valor de árboles contados
    ui_page["TextArbolesValor"] = pv.PvText(container=window, x=604, y=240, width=300,
        height=120, idle_color=(255, 255, 255, 1), text='0', is_visible=True,
        text_alignment='center', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=71,
        font_color=(56, 136, 255, 1), bold=True, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=(0, 0, 0, 1), corner_radius=14,
        on_hover=None, on_click=None, on_release=None, tag=None)

    return ui_page