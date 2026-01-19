import reflex as rx
from app.states.inventory_state import InventoryState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2",
                    ),
                    rx.el.input(
                        placeholder="Search inventory, lots, serials...",
                        class_name="w-96 pl-10 pr-4 py-2.5 bg-gray-50 border-gray-200 border rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all text-sm text-gray-700",
                        on_change=InventoryState.set_search.debounce(300),
                    ),
                    class_name="relative",
                )
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.button(
                        rx.icon("layout-grid", class_name="w-4 h-4"),
                        class_name=rx.cond(
                            InventoryState.view_mode == "grid",
                            "p-2 rounded-lg bg-emerald-100 text-emerald-700 transition-colors",
                            "p-2 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors",
                        ),
                        on_click=lambda: InventoryState.set_view_mode("grid"),
                    ),
                    rx.el.button(
                        rx.icon("list", class_name="w-4 h-4"),
                        class_name=rx.cond(
                            InventoryState.view_mode == "list",
                            "p-2 rounded-lg bg-emerald-100 text-emerald-700 transition-colors",
                            "p-2 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors",
                        ),
                        on_click=lambda: InventoryState.set_view_mode("list"),
                    ),
                    class_name="flex items-center gap-1 bg-white border border-gray-200 rounded-xl p-1 shadow-sm",
                ),
                rx.el.div(
                    rx.icon(
                        "arrow-up-down",
                        class_name="w-4 h-4 text-gray-500 absolute left-3 top-1/2 transform -translate-y-1/2",
                    ),
                    rx.el.select(
                        rx.el.option("Newest First", value="newest"),
                        rx.el.option("Oldest First", value="oldest"),
                        rx.el.option("Name (A-Z)", value="az"),
                        rx.el.option("Quantity (High-Low)", value="qty_desc"),
                        rx.el.option("Expiration (Earliest)", value="expiration"),
                        on_change=InventoryState.set_sort,
                        class_name="pl-9 pr-8 py-2.5 bg-white border border-gray-200 rounded-xl text-sm font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 cursor-pointer shadow-sm hover:border-gray-300 transition-colors appearance-none",
                    ),
                    class_name="relative",
                ),
                rx.el.button(
                    rx.icon("plus", class_name="w-5 h-5"),
                    rx.el.span("Add Item"),
                    class_name="flex items-center gap-2 px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium rounded-xl shadow-lg shadow-emerald-600/20 transition-all active:scale-95",
                    on_click=InventoryState.open_add_modal,
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name="sticky top-0 z-10 bg-white/80 backdrop-blur-md border-b border-gray-100 px-8 py-4",
    )