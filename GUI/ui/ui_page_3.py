import pyvisual as pv


def create_page_3_ui(window,ui):
    """
    Create and return UI elements for Page 3.
    :param container: The page widget for Page 3.
    :return: Dictionary of UI elements.
    """
    ui_page = {}
    ui_page["Button_0"] = pv.PvButton(container=window, x=365, y=13, width=292,
        height=75, text='PRUEBA SENSOR', font='assets/fonts/Lexend/Lexend.ttf', font_size=23,
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

    # Texto descriptivo
    ui_page["TextTitulo"] = pv.PvText(container=window, x=219, y=150, width=585,
        height=60, idle_color=(255, 255, 255, 0), text='DISTANCIA SENSOR (cm)', is_visible=True,
        text_alignment='center', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=29,
        font_color=(0, 0, 0, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=None, corner_radius=0,
        on_hover=None, on_click=None, on_release=None, tag=None)

    # Valor numérico del sensor
    ui_page["TextValorSensor"] = pv.PvText(container=window, x=402, y=240, width=219,
        height=120, idle_color=(255, 255, 255, 1), text='0', is_visible=True,
        text_alignment='center', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=71,
        font_color=(56, 136, 255, 1), bold=True, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=(0, 0, 0, 1), corner_radius=14,
        on_hover=None, on_click=None, on_release=None, tag=None)

    # Barra visual usando un rectángulo
    ui_page["BarraFondo"] = pv.PvRectangle(container=window, x=146, y=405, width=731,
        height=60, idle_color=(220, 220, 220, 1), border_color=(0, 0, 0, 1),
        border_thickness=2, corner_radius=29, is_visible=True, opacity=1,
        on_hover=None, on_click=None, on_release=None, tag=None)
    
    ui_page["BarraDistancia"] = pv.PvRectangle(container=window, x=146, y=405, width=14,
        height=60, idle_color=(56, 136, 255, 1), border_color=None,
        border_thickness=0, corner_radius=29, is_visible=True, opacity=1,
        on_hover=None, on_click=None, on_release=None, tag=None)

    return ui_page
