import reflex as rx
from app.states.inventory_state import InventoryState


def list_item(text: str, on_delete: rx.event.EventType) -> rx.Component:
    return rx.el.div(
        rx.el.span(text, class_name="font-medium text-gray-700"),
        rx.el.button(
            rx.icon("trash-2", class_name="w-4 h-4 text-gray-400 hover:text-red-500"),
            on_click=on_delete,
        ),
        class_name="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors",
    )


def settings_section(
    title: str, description: str, content: rx.Component
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(title, class_name="text-lg font-semibold text-gray-900"),
            rx.el.p(description, class_name="text-sm text-gray-500"),
            class_name="mb-4",
        ),
        content,
        class_name="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6",
    )


def locations_editor() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.input(
                placeholder="New Location Name",
                on_change=InventoryState.set_new_location_name,
                class_name="flex-1 px-4 py-2 border border-gray-200 rounded-lg text-sm",
                default_value=InventoryState.new_location_name,
            ),
            rx.el.button(
                rx.icon("plus", class_name="w-4 h-4"),
                class_name="p-2.5 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700",
                on_click=InventoryState.add_location,
            ),
            class_name="flex gap-2 mb-4",
        ),
        rx.el.div(
            rx.foreach(
                InventoryState.locations,
                lambda loc: list_item(
                    loc["name"], lambda: InventoryState.delete_location(loc["id"])
                ),
            ),
            class_name="space-y-2 max-h-48 overflow-y-auto pr-2",
        ),
    )


def categories_editor() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.input(
                placeholder="New Category Name",
                on_change=InventoryState.set_new_category_name,
                class_name="flex-1 px-4 py-2 border border-gray-200 rounded-lg text-sm",
                default_value=InventoryState.new_category_name,
            ),
            rx.el.button(
                rx.icon("plus", class_name="w-4 h-4"),
                class_name="p-2.5 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700",
                on_click=InventoryState.add_category,
            ),
            class_name="flex gap-2 mb-4",
        ),
        rx.el.div(
            rx.foreach(
                InventoryState.categories,
                lambda cat: list_item(
                    cat["name"], lambda: InventoryState.delete_category(cat["id"])
                ),
            ),
            class_name="space-y-2 max-h-48 overflow-y-auto pr-2",
        ),
    )


def settings_page() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Settings", class_name="text-2xl font-bold text-gray-800 mb-2"),
        rx.el.p(
            "Configure your inventory application", class_name="text-gray-500 mb-8"
        ),
        rx.el.div(
            settings_section(
                "Locations Management",
                "Manage the clinics and storage locations available in the system.",
                locations_editor(),
            ),
            settings_section(
                "Categories Management",
                "Customize the item categories for organization.",
                categories_editor(),
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
        ),
        class_name="max-w-6xl mx-auto",
    )