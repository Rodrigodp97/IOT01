import pyvisual as pv


def create_page_1_ui(window,ui):
    """
    Create and return UI elements for Page 1.
    :param container: The page widget for Page 1.
    :return: Dictionary of UI elements.
    """
    ui_page = {}
    ui_page["Button_0"] = pv.PvButton(container=window, x=365, y=13, width=292,
        height=75, text='SECUENCIA', font='assets/fonts/Lexend/Lexend.ttf', font_size=23,
        font_color=(0, 0, 0, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(255, 255, 255, 1), hover_color=None,
        clicked_color=None, border_color=(0, 0, 0, 1), border_hover_color=None, border_thickness=1,
        corner_radius=0, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    ui_page["Button_1"] = pv.PvButton(container=window, x=554, y=505, width=292,
        height=75, text='MANUAL', font='assets/fonts/Lexend/Lexend.ttf', font_size=23,
        font_color=(195, 187, 224, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(255, 255, 255, 1), hover_color=None,
        clicked_color=None, border_color=(195, 187, 224, 1), border_hover_color=None, border_thickness=1,
        corner_radius=63, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    ui_page["Icon_2"] = pv.PvIcon(container=window, x=40, y=13, width=73,
        height=75, idle_color=(75, 75, 75, 1), preserve_original_colors=False, icon_path='assets/icons/333e6fa6e1.svg',
        corner_radius=0, flip_v=False, flip_h=False, rotate=0,
        border_color=None, border_hover_color=None, border_thickness=0, border_style="solid",
        on_hover=None, on_click=None, on_release=None, is_visible=True,
        opacity=1, tag=None)

    ui_page["Button_3"] = pv.PvButton(container=window, x=178, y=505, width=292,
        height=75, text='AUTOMATICO', font='assets/fonts/Lexend/Lexend.ttf', font_size=23,
        font_color=(195, 187, 224, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(255, 255, 255, 1), hover_color=None,
        clicked_color=None, border_color=(195, 187, 224, 1), border_hover_color=None, border_thickness=1,
        corner_radius=63, border_style="solid", box_shadow='1px 2px 4px 0px rgba(0,0,0,0.2)', box_shadow_hover='0px 2px 4px 5px rgba(0,0,0,0.2)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    ui_page["Webcam_4"] = pv.PvWebcam(container=window, x=40, y=108, width=944,
        height=377, scale=1, corner_radius=14, auto_start=True,
        flip_v=False, flip_h=False, rotate=0, border_color=(0, 0, 0, 1),
        border_hover_color=None, border_thickness=2, border_style="solid", is_visible=True,
        opacity=1, webcam_id=0, on_hover=None, on_click=None,
        on_release=None, tag=None)

    # Botón de PAUSA (solo visible en modo automático)
    ui_page["ButtonPausa"] = pv.PvButton(container=window, x=862, y=20, width=120,
        height=50, text='PAUSA', font='assets/fonts/Poppins/Poppins.ttf', font_size=18,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=True, italic=False,
        underline=False, strikethrough=False, idle_color=(255, 165, 0, 1), hover_color=(255, 140, 0, 1),
        clicked_color=None, border_color=(0, 0, 0, 1), border_hover_color=None, border_thickness=2,
        corner_radius=10, border_style="solid", box_shadow='2px 2px 4px 0px rgba(0,0,0,0.3)', box_shadow_hover='2px 2px 6px 0px rgba(0,0,0,0.4)',
        icon_path=None, icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1, paddings=(0, 0, 0, 0), is_visible=False,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)
    
    # LED circular indicador de estado del relé
    ui_page["LedRele"] = pv.PvRectangle(container=window, x=140, y=30, width=30,
        height=30, idle_color=(150, 150, 150, 1), hover_color=None, clicked_color=None,
        border_color=(100, 100, 100, 1), border_hover_color=None, border_thickness=2,
        corner_radius=15, border_style="solid", box_shadow='2px 2px 4px 0px rgba(0,0,0,0.3)',
        on_hover=None, on_click=None, on_release=None, is_visible=True,
        opacity=1, tag=None)
    
    # Texto indicador del estado del relé
    ui_page["TextEstadoRele"] = pv.PvText(container=window, x=180, y=30, width=120,
        height=30, text='DETENIDO', font='assets/fonts/Poppins/Poppins.ttf', font_size=16,
        font_color=(100, 100, 100, 1), bold=True, italic=False, underline=False,
        strikethrough=False, h_align='left', v_align='center', is_visible=True,
        opacity=1, tag=None)

    return ui_page
