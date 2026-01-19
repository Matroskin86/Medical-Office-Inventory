import reflex as rx
from app.states.inventory_state import InventoryState, InventoryItem


def label_card(item: InventoryItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    item["name"],
                    class_name="font-bold text-gray-900 text-sm leading-tight h-10 overflow-hidden",
                ),
                rx.el.p(
                    f"ID: {item['id'][:8]}",
                    class_name="text-[10px] text-gray-500 font-mono mt-1",
                ),
                class_name="flex-1 pr-2",
            ),
            rx.el.div(
                rx.image(
                    src=f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={item['id']}",
                    class_name="w-14 h-14 mix-blend-multiply",
                ),
                class_name="bg-white",
            ),
            class_name="flex justify-between items-start mb-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "LOT",
                        class_name="text-[9px] text-gray-400 font-bold uppercase tracking-wider",
                    ),
                    rx.el.span(
                        item["lot_number"], class_name="text-xs font-mono font-semibold"
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.div(
                    rx.el.span(
                        "EXP",
                        class_name="text-[9px] text-gray-400 font-bold uppercase tracking-wider",
                    ),
                    rx.el.span(
                        item["expiration_date"],
                        class_name="text-xs font-mono font-semibold",
                    ),
                    class_name="flex flex-col text-right",
                ),
                class_name="flex justify-between mb-2",
            ),
            rx.el.div(
                rx.el.span(
                    item["category"], class_name="text-[10px] text-gray-500 truncate"
                ),
                rx.el.span(
                    item["location"],
                    class_name="text-[10px] text-gray-500 truncate text-right",
                ),
                class_name="flex justify-between border-t border-gray-100 pt-2",
            ),
            class_name="flex flex-col",
        ),
        class_name="bg-white border border-gray-300 rounded-lg p-3 w-[3.5in] h-[2in] break-inside-avoid shadow-sm print:shadow-none print:border-black relative overflow-hidden",
    )


def labels_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Label Generator",
                    class_name="text-2xl font-bold text-gray-800 mb-2",
                ),
                rx.el.p(
                    "Preview and print asset labels with QR codes",
                    class_name="text-gray-500 mb-8",
                ),
            ),
            rx.el.button(
                rx.icon("printer", class_name="w-5 h-5"),
                "Print Labels",
                class_name="flex items-center gap-2 px-6 py-2.5 bg-gray-900 text-white font-medium rounded-xl hover:bg-gray-800 transition-colors shadow-lg",
                on_click=rx.call_script("window.print()"),
            ),
            class_name="flex items-start justify-between mb-8 print:hidden",
        ),
        rx.el.div(
            rx.foreach(InventoryState.filtered_items, label_card),
            class_name="flex flex-wrap gap-6 justify-center print:block print:space-y-4",
        ),
        class_name="max-w-7xl mx-auto print:max-w-none",
    )