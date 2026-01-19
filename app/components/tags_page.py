import reflex as rx
from app.states.inventory_state import InventoryState


def tag_card(tag: dict) -> rx.Component:
    count = InventoryState.tag_counts[tag["name"]]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("tag", class_name=f"w-5 h-5 text-{tag['color']}-500"),
                rx.el.span(tag["name"], class_name="font-medium text-gray-900"),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                rx.el.span(
                    f"{count} items",
                    class_name="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full group-hover:bg-gray-200 transition-colors",
                ),
                class_name="mt-2",
            ),
            class_name="flex flex-col items-start",
        ),
        rx.el.button(
            rx.icon("trash-2", class_name="w-4 h-4 text-gray-400 hover:text-red-500"),
            on_click=lambda: InventoryState.delete_tag(tag["id"]),
            class_name="p-2 hover:bg-red-50 rounded-lg transition-colors",
        ),
        class_name="group flex items-start justify-between p-4 bg-white border border-gray-100 rounded-xl hover:shadow-md hover:border-emerald-100 transition-all cursor-pointer",
        on_click=lambda: InventoryState.select_tag_filter(tag["name"]),
    )


def color_option(color: str) -> rx.Component:
    is_selected = InventoryState.new_tag_color == color
    return rx.el.button(
        class_name=rx.cond(
            is_selected,
            f"w-8 h-8 rounded-full bg-{color}-500 ring-2 ring-offset-2 ring-{color}-500 transition-all",
            f"w-8 h-8 rounded-full bg-{color}-500 opacity-50 hover:opacity-100 transition-all",
        ),
        on_click=lambda: InventoryState.set_new_tag_color(color),
    )


def tags_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Tags Management", class_name="text-2xl font-bold text-gray-800 mb-2"
            ),
            rx.el.p(
                "Create and manage tags for your inventory items",
                class_name="text-gray-500 mb-8",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3("Create New Tag", class_name="text-lg font-semibold mb-4"),
                rx.el.div(
                    rx.el.input(
                        placeholder="Enter tag name...",
                        on_change=InventoryState.set_new_tag_name,
                        class_name="w-full px-4 py-2 border border-gray-200 rounded-xl mb-4 focus:outline-none focus:ring-2 focus:ring-emerald-500/50",
                        default_value=InventoryState.new_tag_name,
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Select Color:",
                            class_name="text-sm text-gray-500 mb-2 block",
                        ),
                        rx.el.div(
                            color_option("red"),
                            color_option("orange"),
                            color_option("yellow"),
                            color_option("green"),
                            color_option("emerald"),
                            color_option("blue"),
                            color_option("purple"),
                            color_option("gray"),
                            class_name="flex gap-3 mb-6",
                        ),
                    ),
                    rx.el.button(
                        "Create Tag",
                        class_name="w-full py-2.5 bg-emerald-600 text-white font-medium rounded-xl hover:bg-emerald-700 transition-colors",
                        on_click=InventoryState.add_tag,
                    ),
                    class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
                ),
                class_name="w-full md:w-1/3",
            ),
            rx.el.div(
                rx.el.h3("Existing Tags", class_name="text-lg font-semibold mb-4"),
                rx.el.div(
                    rx.foreach(InventoryState.tags, tag_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                ),
                class_name="w-full md:w-2/3",
            ),
            class_name="flex flex-col md:flex-row gap-8",
        ),
        class_name="max-w-6xl mx-auto",
    )