import reflex as rx
from app.states.inventory_state import InventoryState


def nav_item(icon: str, text: str) -> rx.Component:
    is_active = InventoryState.active_nav_item == text
    return rx.el.button(
        rx.icon(icon, class_name="w-5 h-5"),
        rx.el.span(text, class_name="font-medium"),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 w-full px-4 py-3 text-emerald-50 bg-white/10 rounded-xl transition-colors",
            "flex items-center gap-3 w-full px-4 py-3 text-emerald-100 hover:bg-white/5 hover:text-white rounded-xl transition-colors",
        ),
        on_click=lambda: InventoryState.set_nav_item(text),
    )


def folder_item(text: str, is_sub: bool = False) -> rx.Component:
    is_selected = InventoryState.active_folder == text
    padding = rx.cond(is_sub, "pl-12", "pl-4")
    return rx.el.button(
        rx.el.div(
            rx.icon(
                "folder",
                class_name=rx.cond(
                    is_selected,
                    "w-4 h-4 text-emerald-200 fill-current",
                    "w-4 h-4 text-emerald-300",
                ),
            ),
            rx.el.span(text, class_name="truncate"),
            class_name=f"flex items-center gap-3 {padding}",
        ),
        class_name=rx.cond(
            is_selected,
            "w-full py-2 text-sm text-white font-medium bg-white/10 rounded-lg text-left transition-colors",
            "w-full py-2 text-sm text-emerald-100 hover:text-white hover:bg-white/5 rounded-lg text-left transition-colors",
        ),
        on_click=lambda: InventoryState.set_folder(text),
    )


def all_items_nav_item() -> rx.Component:
    is_selected = InventoryState.active_folder == "All Items"
    return rx.el.button(
        rx.el.div(
            rx.icon(
                "layers",
                class_name=rx.cond(
                    is_selected,
                    "w-4 h-4 text-emerald-200 fill-current",
                    "w-4 h-4 text-emerald-300",
                ),
            ),
            rx.el.span("All Items", class_name="truncate"),
            class_name="flex items-center gap-3 pl-4",
        ),
        class_name=rx.cond(
            is_selected,
            "w-full py-2 text-sm text-white font-medium bg-white/10 rounded-lg text-left transition-colors mb-2 ring-1 ring-white/10 shadow-sm",
            "w-full py-2 text-sm text-emerald-100 hover:text-white hover:bg-white/5 rounded-lg text-left transition-colors mb-2",
        ),
        on_click=lambda: InventoryState.set_folder("All Items"),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("activity", class_name="w-8 h-8 text-white"),
                rx.el.h1(
                    "MedInventory",
                    class_name="text-2xl font-bold text-white tracking-tight",
                ),
                class_name="flex items-center gap-3 px-4 py-6 mb-2",
            ),
            rx.el.nav(
                rx.el.div(
                    nav_item("package", "Items"),
                    nav_item("tags", "Tags"),
                    nav_item("qr-code", "Labels"),
                    nav_item("settings", "Settings"),
                    class_name="space-y-1 px-3",
                ),
                rx.el.div(class_name="h-px bg-emerald-500/30 my-6 mx-4"),
                rx.el.div(
                    rx.el.p(
                        "CATEGORIES",
                        class_name="px-4 text-xs font-semibold text-emerald-300 mb-3 tracking-wider",
                    ),
                    rx.el.div(
                        all_items_nav_item(),
                        rx.foreach(
                            InventoryState.categories,
                            lambda cat: folder_item(cat["name"]),
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.el.div(
                                    rx.icon(
                                        "map-pin", class_name="w-4 h-4 text-emerald-300"
                                    ),
                                    rx.el.span("Places", class_name="flex-1 text-left"),
                                    rx.icon(
                                        "chevron-down",
                                        class_name=rx.cond(
                                            InventoryState.places_expanded,
                                            "w-4 h-4 transform rotate-180 transition-transform",
                                            "w-4 h-4 transition-transform",
                                        ),
                                    ),
                                    class_name="flex items-center gap-3 pl-4",
                                ),
                                class_name="w-full py-2 text-sm text-emerald-100 hover:text-white hover:bg-white/5 rounded-lg transition-colors",
                                on_click=InventoryState.toggle_places,
                            ),
                            rx.cond(
                                InventoryState.places_expanded,
                                rx.el.div(
                                    rx.foreach(
                                        InventoryState.locations,
                                        lambda loc: folder_item(
                                            loc["name"], is_sub=True
                                        ),
                                    ),
                                    class_name="mt-1 space-y-1 animate-fadeIn",
                                ),
                            ),
                        ),
                        folder_item("Expired"),
                        class_name="space-y-1 px-3",
                    ),
                    class_name="flex-1 overflow-y-auto",
                ),
                class_name="flex flex-col h-full",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="w-72 h-screen bg-emerald-900 flex-shrink-0 border-r border-emerald-800 shadow-xl z-20",
    )