import os
import threading
import random
import bot

import flet as ft
import grinding  # import your bot logic


def main(page: ft.Page):
    # Window setup
    icon_path = os.path.abspath("../win_assets/logo.ico")
    page.window.icon = icon_path
    page.title = "PokeNexus BOT"
    page.window.width = 800
    page.window.height = 800
    page.padding = 10
    page.window.center()
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.update()


    # ---------------- LEFT COLUMN (fixed buttons) ----------------
    left_column = ft.Column(
        controls=[
            ft.ElevatedButton("Global Start", on_click=lambda e: print("Global Start clicked")),
            ft.ElevatedButton("Global Stop", on_click=lambda e: print("Global Stop clicked")),
            ft.ElevatedButton("Global Reset", on_click=lambda e: print("Global Reset clicked")),
        ],
        spacing=10,
        width=150,
    )

    # ---------------- RIGHT COLUMN (dynamic content) ----------------
    right_column = ft.Column(spacing=10, expand=2)

    # Input fields for each tab
    mining_inputs = [ft.TextField(label="Mining Input 1"), ft.TextField(label="Mining Input 2")]
    fishing_inputs = [ft.TextField(label="Fishing Spot")]
    grinding_inputs = [ft.TextField(label="Initial Money"), ft.TextField(label="Grind Session (hours)")]

    # ---------------- Content for each tab ----------------
    def mining_content():
        return ft.Column(
            [
                ft.ElevatedButton("Start Mining", on_click=lambda e: print("Mining Start")),
                ft.ElevatedButton("Stop Mining", on_click=lambda e: print("Mining Stop")),
                *mining_inputs,
            ],
            spacing=10,
        )

    def fishing_content():
        return ft.Column(
            [
                ft.ElevatedButton("Cast Rod", on_click=lambda e: print("Fishing Cast")),
                ft.ElevatedButton("Reel In", on_click=lambda e: print("Fishing Reel")),
                *fishing_inputs,
            ],
            spacing=10,
        )

    # ---------------- Grinding Tab ----------------
    pokemon_list = []  # holds backend data for each added Pokémon

    def grinding_content():
        # local state
        pokemon_display = ft.Column(spacing=5)
        pokemon_display_container = ft.Container(
            content=ft.ListView(
                controls=[pokemon_display],
                expand=True,
                spacing=5,
            ),
            bgcolor=ft.Colors.GREY_200,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=8,
            padding=10,
            width=400,
            height=250,
        )

        # Input controls
        pokemon_name = ft.TextField(label="Pokemon Name", width=200)
        move_dropdown = ft.Dropdown(
            label="Move",
            options=[ft.dropdown.Option(str(i)) for i in range(1, 5)],
            width=100,
        )
        catch_button = ft.ElevatedButton(
            "Catch: OFF", bgcolor=ft.Colors.GREY_300, color=ft.Colors.BLACK
        )

        # Toggle catch button
        def toggle_catch(e):
            if catch_button.text == "Catch: OFF":
                catch_button.text = "Catch: ON"
                catch_button.bgcolor = ft.Colors.GREEN
                catch_button.color = ft.Colors.WHITE
            else:
                catch_button.text = "Catch: OFF"
                catch_button.bgcolor = ft.Colors.GREY_300
                catch_button.color = ft.Colors.BLACK
            page.update()

        catch_button.on_click = toggle_catch

        # Refresh Pokémon display
        def refresh_display():
            pokemon_display.controls.clear()
            for i, p in enumerate(pokemon_list):
                pokemon_display.controls.append(
                    ft.Row(
                        [
                            ft.Text(
                                f"{p['name']}",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                font_family="Arial",
                                color=ft.Colors.BLACK,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                tooltip="Remove",
                                on_click=lambda e, index=i: remove_pokemon(index),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                )
            page.update()

        # Remove Pokémon
        def remove_pokemon(index):
            del pokemon_list[index]
            refresh_display()

        # Add Pokémon
        def add_pokemon(e):
            name = pokemon_name.value.strip()
            move = move_dropdown.value
            catch = (catch_button.text == "Catch: ON")

            if not name or not move:
                page.snack_bar = ft.SnackBar(ft.Text("Please enter Pokemon name and select a move"))
                page.snack_bar.open = True
                page.update()
                return

            pokemon_entry = {"name": name, "move": move, "catch": catch}
            pokemon_list.append(pokemon_entry)

            # Reset inputs
            pokemon_name.value = ""
            move_dropdown.value = None
            catch_button.text = "Catch: OFF"
            catch_button.bgcolor = ft.Colors.GREY_300
            catch_button.color = ft.Colors.BLACK
            refresh_display()

        return ft.Column(
            [
                ft.ElevatedButton("Start Grinding", on_click=start_handler),
                ft.ElevatedButton("Stop Grinding", on_click=stop_handler),
                *grinding_inputs,
                ft.Row(
                    [pokemon_name, move_dropdown, catch_button, ft.ElevatedButton("Add Pokemon", on_click=add_pokemon)],
                    spacing=10,
                ),
                pokemon_display_container,
            ],
            spacing=10,
        )

    # ---------------- Handlers ----------------
    def start_handler(e):
        initial_money = grinding_inputs[0].value
        timer = {
            "session_duration": 18000 if grinding_inputs[1].value == "" else int(grinding_inputs[1].value) * 3600,
            "break_time": random.randint(3, 5) * 60,
            "run_time": random.randint(25, 55) * 60,
        }
        grinding.append_pokemon(pokemon_list)
        grinding.reload_images()
        grinding.start_grinding()

        # Run timer_cycle in its own thread
        threading.Thread(
            target=grinding.timer_cycle,
            args=(timer["session_duration"], timer["run_time"], timer["break_time"]),
            daemon=True,
        ).start()



    def stop_handler(e):
        grinding.stop_grinding()

    # ---------------- Tabs ----------------
    def update_tab_content():
        index = tabs.selected_index
        if index == 0:
            right_column.controls = [mining_content()]
        elif index == 1:
            right_column.controls = [fishing_content()]
        elif index == 2:
            right_column.controls = [grinding_content()]
        page.update()

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[ft.Tab(text="Mining"), ft.Tab(text="Fishing"), ft.Tab(text="Grinding")],
        height=40,
        on_change=lambda e: update_tab_content(),
    )

    # Separators
    tabs_separator = ft.Container(height=1, width=None, bgcolor=ft.Colors.GREY_300)
    separator = ft.Container(width=1, height=None, bgcolor=ft.Colors.GREY_300)

    # Main layout
    main_row = ft.Row(controls=[left_column, separator, right_column], spacing=20, expand=True)
    page.add(tabs, tabs_separator, main_row)

    # Initialize first tab content
    update_tab_content()

# Start the bot
bot.start_bot()
# Run the app
ft.app(target=main, assets_dir="win_assets")
