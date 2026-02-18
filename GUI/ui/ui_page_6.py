import pyvisual as pv


def create_page_6_ui(window,ui):
    """
    Create and return UI elements for Page 6 (HUERTAS DE LEON 1).
    :param container: The page widget for Page 6.
    :return: Dictionary of UI elements.
    """
    ui_page = {}
    
    # Título de la página
    ui_page["Button_0"] = pv.PvButton(container=window, x=365, y=13, width=292,
        height=75, text='HUERTAS LEON 1', font='assets/fonts/Lexend/Lexend.ttf', font_size=23,
        font_color=(0, 0, 0, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(255, 255, 255, 1), hover_color=None,
        clicked_color=None, border_color=(0, 0, 0, 1), border_hover_color=None, border_thickness=1,
        corner_radius=0, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    # Icono de flecha para volver al menú de mapas
    ui_page["Icon_1"] = pv.PvIcon(container=window, x=40, y=13, width=73,
        height=75, idle_color=(75, 75, 75, 1), preserve_original_colors=False, icon_path='assets/icons/333e6fa6e1.svg',
        corner_radius=0, flip_v=False, flip_h=False, rotate=0,
        border_color=None, border_hover_color=None, border_thickness=0, border_style="solid",
        on_hover=None, on_click=None, on_release=None, is_visible=True,
        opacity=1, tag=None)

    # Botón grande para abrir el mapa interactivo
    ui_page["ButtonAbrirMapa"] = pv.PvButton(container=window, x=312, y=200, width=400,
        height=100, text='ABRIR MAPA INTERACTIVO', font='assets/fonts/Poppins/Poppins.ttf', font_size=26,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=True, italic=False,
        underline=False, strikethrough=False, idle_color=(76, 175, 80, 1), hover_color=(56, 142, 60, 1),
        clicked_color=None, border_color=(100, 100, 100, 1), border_hover_color=None, border_thickness=2,
        corner_radius=10, border_style="solid", box_shadow='2px 2px 6px 0px rgba(0,0,0,0.3)', box_shadow_hover='2px 2px 8px 0px rgba(0,0,0,0.4)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    # Información sobre el mapa
    ui_page["TextInfo1"] = pv.PvText(container=window, x=240, y=330, width=544,
        height=40, text='Vista satélite de Huertas de León 1', 
        font='assets/fonts/Poppins/Poppins.ttf', font_size=18,
        font_color=(80, 80, 80, 1), bold=False, italic=False, underline=False,
        strikethrough=False, h_align='center', v_align='center', is_visible=True,
        opacity=1, tag=None)

    ui_page["TextInfo2"] = pv.PvText(container=window, x=240, y=370, width=544,
        height=80, text='• Navegación con ratón\n• Zoom con rueda del ratón\n• Click para marcar puntos', 
        font='assets/fonts/Poppins/Poppins.ttf', font_size=14,
        font_color=(100, 100, 100, 1), bold=False, italic=False, underline=False,
        strikethrough=False, h_align='center', v_align='center', is_visible=True,
        opacity=1, tag=None)

    # Coordenadas del mapa
    ui_page["TextCoords"] = pv.PvText(container=window, x=240, y=460, width=544,
        height=30, text='Coordenadas: 38.6359, -2.9156', 
        font='assets/fonts/Poppins/Poppins.ttf', font_size=12,
        font_color=(120, 120, 120, 1), bold=False, italic=True, underline=False,
        strikethrough=False, h_align='center', v_align='center', is_visible=True,
        opacity=1, tag=None)

    return ui_page
