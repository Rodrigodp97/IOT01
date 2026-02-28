import pyvisual as pv


def create_page_0_ui(window,ui):
    """
    Create and return UI elements for Page 0.
    :param container: The page widget for Page 0.
    :return: Dictionary of UI elements.
    """
    ui_page = {}
    # Fila superior - 2 botones centrados
    ui_page["Button_1"] = pv.PvButton(container=window, x=200, y=339, width=292,
        height=75, text='CONFIGURACION', font='assets/fonts/Poppins/Poppins.ttf', font_size=23,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(56, 136, 255, 1), hover_color=None,
        clicked_color=None, border_color=(100, 100, 100, 1), border_hover_color=None, border_thickness=0,
        corner_radius=0, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    ui_page["Button_0"] = pv.PvButton(container=window, x=532, y=339, width=292,
        height=75, text='INICIO SECUENCIA', font='assets/fonts/Poppins/Poppins.ttf', font_size=23,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(56, 136, 255, 1), hover_color=None,
        clicked_color=None, border_color=(100, 100, 100, 1), border_hover_color=None, border_thickness=0,
        corner_radius=0, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    # Fila inferior - 3 botones centrados
    ui_page["Button_4"] = pv.PvButton(container=window, x=62, y=454, width=292,
        height=75, text='RESULTADOS', font='assets/fonts/Poppins/Poppins.ttf', font_size=23,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(56, 136, 255, 1), hover_color=None,
        clicked_color=None, border_color=(100, 100, 100, 1), border_hover_color=None, border_thickness=0,
        corner_radius=0, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    ui_page["Button_2"] = pv.PvButton(container=window, x=366, y=454, width=292,
        height=75, text='PRUEBA SENSOR', font='assets/fonts/Poppins/Poppins.ttf', font_size=23,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(56, 136, 255, 1), hover_color=None,
        clicked_color=None, border_color=(100, 100, 100, 1), border_hover_color=None, border_thickness=0,
        corner_radius=0, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    ui_page["Button_5"] = pv.PvButton(container=window, x=670, y=454, width=292,
        height=75, text='MAPAS', font='assets/fonts/Poppins/Poppins.ttf', font_size=23,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(56, 136, 255, 1), hover_color=None,
        clicked_color=None, border_color=(100, 100, 100, 1), border_hover_color=None, border_thickness=0,
        corner_radius=0, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)
    
    # Texto de versión de firmware en esquina superior derecha
    ui_page["TextVersionFW"] = pv.PvText(container=window, x=750, y=20, width=250,
        height=30, text='Version FW: ---', font='assets/fonts/Poppins/Poppins.ttf', font_size=16,
        font_color=(100, 100, 100, 1), bold=False, italic=False, underline=False,
        strikethrough=False, h_align='right', v_align='top', is_visible=True,
        opacity=1, tag=None)

    # Indicador visual de conectividad para mapas (icono WiFi dinámico)
    ui_page["IconWifiEstado"] = pv.PvText(container=window, x=20, y=12, width=52,
        height=44, text='📶', font='assets/fonts/Poppins/Poppins.ttf', font_size=30,
        font_color=(180, 120, 0, 1), bold=True, italic=False, underline=False,
        strikethrough=False, h_align='left', v_align='center', is_visible=True,
        opacity=1, tag=None)

    ui_page["TextEstadoMapa"] = pv.PvText(container=window, x=70, y=20, width=230,
        height=30, text='COMPROBANDO...', font='assets/fonts/Poppins/Poppins.ttf', font_size=16,
        font_color=(180, 120, 0, 1), bold=True, italic=False, underline=False,
        strikethrough=False, h_align='left', v_align='top', is_visible=True,
        opacity=1, tag=None)

    ui_page["Image_6"] = pv.PvImage(container=window, x=364, y=18, image_path='assets/images/93916a4476.png',
        scale=0.634, corner_radius=0, flip_v=False, flip_h=False,
        rotate=0, border_color=None, border_hover_color=None, on_hover=None,
        on_click=None, on_release=None, border_thickness=0, border_style="solid",
        is_visible=True, opacity=1, tag=None)

    return ui_page
