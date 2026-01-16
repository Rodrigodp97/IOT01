import pyvisual as pv


def create_page_2_ui(window,ui):
    """
    Create and return UI elements for Page 2.
    :param container: The page widget for Page 2.
    :return: Dictionary of UI elements.
    """
    ui_page = {}
    ui_page["Button_0"] = pv.PvButton(container=window, x=365, y=18, width=292,
        height=75, text='CONFIGURACIONES', font='assets/fonts/Lexend/Lexend.ttf', font_size=23,
        font_color=(0, 0, 0, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(255, 255, 255, 1), hover_color=None,
        clicked_color=None, border_color=(0, 0, 0, 1), border_hover_color=None, border_thickness=1,
        corner_radius=0, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    ui_page["Icon_1"] = pv.PvIcon(container=window, x=32, y=18, width=73,
        height=75, idle_color=(75, 75, 75, 1), preserve_original_colors=False, icon_path='assets/icons/333e6fa6e1.svg',
        corner_radius=0, flip_v=False, flip_h=False, rotate=0,
        border_color=None, border_hover_color=None, border_thickness=0, border_style="solid",
        on_hover=None, on_click=None, on_release=None, is_visible=True,
        opacity=1, tag=None)

    ui_page["Text_2"] = pv.PvText(container=window, x=175, y=190, width=200,
        height=94, idle_color=(144, 80, 178, 0), text='RETRASO DETECCION', is_visible=True,
        text_alignment='left', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=32,
        font_color=(0, 0, 0, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=None, corner_radius=0,
        on_hover=None, on_click=None, on_release=None, tag=None)

    # Texto para mostrar el valor del retraso
    ui_page["TextRetrasoValor"] = pv.PvText(container=window, x=409, y=217, width=87,
        height=60, idle_color=(255, 255, 255, 1), text='0', is_visible=True,
        text_alignment='center', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=41,
        font_color=(0, 0, 0, 1), bold=True, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=(0, 0, 0, 1), corner_radius=7,
        on_hover=None, on_click=None, on_release=None, tag=None)

    # Botón para incrementar
    ui_page["ButtonRetrasoUp"] = pv.PvButton(container=window, x=512, y=202, width=51,
        height=52, text='▲', font='assets/fonts/Poppins/Poppins.ttf', font_size=26,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(56, 136, 255, 1), hover_color=(76, 156, 255, 1),
        clicked_color=None, border_color=(0, 0, 0, 1), border_hover_color=None, border_thickness=1,
        corner_radius=7, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    # Botón para decrementar
    ui_page["ButtonRetrasoDown"] = pv.PvButton(container=window, x=512, y=262, width=51,
        height=52, text='▼', font='assets/fonts/Poppins/Poppins.ttf', font_size=26,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(56, 136, 255, 1), hover_color=(76, 156, 255, 1),
        clicked_color=None, border_color=(0, 0, 0, 1), border_hover_color=None, border_thickness=1,
        corner_radius=7, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    ui_page["Text_3"] = pv.PvText(container=window, x=658, y=195, width=169,
        height=85, idle_color=(144, 80, 178, 0), text='TIEMPO MEDIDAS', is_visible=True,
        text_alignment='left', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=32,
        font_color=(0, 0, 0, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=None, corner_radius=0,
        on_hover=None, on_click=None, on_release=None, tag=None)

    # Texto para mostrar el valor del tiempo
    ui_page["TextTiempoValor"] = pv.PvText(container=window, x=848, y=217, width=87,
        height=60, idle_color=(255, 255, 255, 1), text='0', is_visible=True,
        text_alignment='center', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=41,
        font_color=(0, 0, 0, 1), bold=True, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=(0, 0, 0, 1), corner_radius=7,
        on_hover=None, on_click=None, on_release=None, tag=None)

    # Botón para incrementar tiempo
    ui_page["ButtonTiempoUp"] = pv.PvButton(container=window, x=950, y=202, width=51,
        height=52, text='▲', font='assets/fonts/Poppins/Poppins.ttf', font_size=26,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(56, 136, 255, 1), hover_color=(76, 156, 255, 1),
        clicked_color=None, border_color=(0, 0, 0, 1), border_hover_color=None, border_thickness=1,
        corner_radius=7, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    # Botón para decrementar tiempo
    ui_page["ButtonTiempoDown"] = pv.PvButton(container=window, x=950, y=262, width=51,
        height=52, text='▼', font='assets/fonts/Poppins/Poppins.ttf', font_size=26,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(56, 136, 255, 1), hover_color=(76, 156, 255, 1),
        clicked_color=None, border_color=(0, 0, 0, 1), border_hover_color=None, border_thickness=1,
        corner_radius=7, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    ui_page["Text_4"] = pv.PvText(container=window, x=174, y=360, width=203,
        height=106, idle_color=(144, 80, 178, 0), text='DISTANCIA DETECCION', is_visible=True,
        text_alignment='left', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=32,
        font_color=(0, 0, 0, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=None, corner_radius=0,
        on_hover=None, on_click=None, on_release=None, tag=None)

    # Texto para mostrar el valor de la distancia
    ui_page["TextDistanciaValor"] = pv.PvText(container=window, x=409, y=387, width=87,
        height=60, idle_color=(255, 255, 255, 1), text='0', is_visible=True,
        text_alignment='center', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=41,
        font_color=(0, 0, 0, 1), bold=True, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=(0, 0, 0, 1), corner_radius=7,
        on_hover=None, on_click=None, on_release=None, tag=None)

    # Botón para incrementar distancia
    ui_page["ButtonDistanciaUp"] = pv.PvButton(container=window, x=512, y=372, width=51,
        height=52, text='▲', font='assets/fonts/Poppins/Poppins.ttf', font_size=26,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(56, 136, 255, 1), hover_color=(76, 156, 255, 1),
        clicked_color=None, border_color=(0, 0, 0, 1), border_hover_color=None, border_thickness=1,
        corner_radius=7, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    # Botón para decrementar distancia
    ui_page["ButtonDistanciaDown"] = pv.PvButton(container=window, x=512, y=432, width=51,
        height=52, text='▼', font='assets/fonts/Poppins/Poppins.ttf', font_size=26,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(56, 136, 255, 1), hover_color=(76, 156, 255, 1),
        clicked_color=None, border_color=(0, 0, 0, 1), border_hover_color=None, border_thickness=1,
        corner_radius=7, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    ui_page["Button_5"] = pv.PvButton(container=window, x=658, y=376, width=190,
        height=75, text='GUARDAR', font='assets/fonts/Inter/Inter.ttf', font_size=23,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(39, 168, 39, 1), hover_color=None,
        clicked_color=None, border_color=(100, 100, 100, 1), border_hover_color=None, border_thickness=0,
        corner_radius=7, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    return ui_page
