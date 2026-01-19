import reflex as rx
from app.states.inventory_state import InventoryState, InventoryItem
from app.components.modals import (
    add_edit_modal,
    item_detail_modal,
    move_stock_modal,
    adjust_stock_modal,
    checkout_modal,
)
from app.components.tags_page import tags_page
from app.components.labels_page import labels_page
from app.components.settings_page import settings_page


def status_badge(item: InventoryItem) -> rx.Component:
    return rx.cond(
        item["is_checked_out"],
        rx.el.span(
            "Checked Out",
            class_name="px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-700 border border-orange-200",
        ),
        rx.match(
            item["status"],
            (
                "expired",
                rx.el.span(
                    "Expired",
                    class_name="px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-700 border border-red-200",
                ),
            ),
            (
                "warning",
                rx.el.span(
                    "Expiring Soon",
                    class_name="px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-700 border border-yellow-200",
                ),
            ),
            rx.el.span(
                "In Stock",
                class_name="px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-700 border border-emerald-200",
            ),
        ),
    )


def item_card_grid(item: InventoryItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=item["image"],
                class_name="w-full h-32 object-contain p-4 bg-gray-50/50",
            ),
            rx.el.div(status_badge(item), class_name="absolute top-3 right-3"),
            class_name="relative",
        ),
        rx.el.div(
            rx.el.h3(
                item["name"],
                class_name="font-semibold text-gray-900 mb-1 truncate",
                title=item["name"],
            ),
            rx.el.div(
                rx.el.p(
                    f"{item['category']} • {item['location']}",
                    class_name="text-xs text-gray-500 mb-3 truncate",
                ),
                rx.cond(
                    item["is_checked_out"],
                    rx.el.div(
                        rx.icon("user", class_name="w-3 h-3 mr-1 text-orange-600"),
                        rx.el.span(
                            f"Out: {item['checked_out_by']}",
                            class_name="text-xs font-medium text-orange-700 truncate",
                        ),
                        class_name="flex items-center bg-orange-100 px-2 py-1 rounded mb-3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Quantity",
                                class_name="text-xs text-gray-400 uppercase tracking-wide",
                            ),
                            rx.el.p(
                                f"{item['quantity']} {item['unit']}",
                                class_name="font-medium text-gray-900",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Value",
                                class_name="text-xs text-gray-400 uppercase tracking-wide text-right",
                            ),
                            rx.el.p(
                                f"${item['price']:.2f}",
                                class_name="font-medium text-gray-900 text-right",
                            ),
                        ),
                        class_name="flex justify-between items-end mb-3",
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span("Lot: ", class_name="text-gray-400"),
                        rx.el.span(
                            item["lot_number"],
                            class_name="text-gray-700 font-mono text-xs",
                        ),
                        class_name="text-xs",
                    ),
                    rx.el.div(
                        rx.el.span("Exp: ", class_name="text-gray-400"),
                        rx.el.span(
                            item["expiration_date"],
                            class_name="text-gray-700 font-mono text-xs",
                        ),
                        class_name="text-xs",
                    ),
                    class_name="flex justify-between pt-3 border-t border-gray-100",
                ),
            ),
            class_name="p-4",
        ),
        class_name=rx.cond(
            item["is_checked_out"],
            "group bg-orange-50/20 border border-orange-200 rounded-xl overflow-hidden hover:shadow-lg transition-all duration-300 cursor-pointer ring-1 ring-orange-200",
            "group bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-lg hover:border-emerald-200 transition-all duration-300 cursor-pointer",
        ),
        on_click=lambda: InventoryState.open_detail_modal(item),
    )


def item_row_list(item: InventoryItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=item["image"],
                class_name="w-10 h-10 rounded-lg bg-gray-50 object-contain p-0.5",
            ),
            rx.el.div(
                rx.el.h3(item["name"], class_name="font-medium text-gray-900 text-sm"),
                rx.el.p(
                    f"{item['lot_number']} • {item['serial_number']}",
                    class_name="text-xs text-gray-500 font-mono",
                ),
                class_name="flex flex-col min-w-0",
            ),
            class_name="flex items-center gap-4 w-1/3",
        ),
        rx.el.div(
            rx.el.span(item["category"], class_name="text-sm text-gray-600"),
            class_name="w-1/6",
        ),
        rx.el.div(
            rx.el.span(item["location"], class_name="text-sm text-gray-600"),
            class_name="w-1/6",
        ),
        rx.el.div(
            rx.el.span(
                f"{item['quantity']} {item['unit']}",
                class_name="text-sm font-medium text-gray-900",
            ),
            class_name="w-1/6 text-right pr-4",
        ),
        rx.el.div(
            rx.el.span(
                item["expiration_date"], class_name="text-sm font-mono text-gray-600"
            ),
            class_name="w-1/6",
        ),
        rx.el.div(status_badge(item), class_name="w-32 flex justify-end"),
        class_name=rx.cond(
            item["is_checked_out"],
            "flex items-center p-4 bg-orange-50/30 border border-orange-100 hover:bg-orange-50/50 rounded-lg transition-colors cursor-pointer",
            "flex items-center p-4 bg-white border border-gray-100 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer",
        ),
        on_click=lambda: InventoryState.open_detail_modal(item),
    )


def items_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    InventoryState.active_folder,
                    class_name="text-2xl font-bold text-gray-800",
                ),
                rx.el.p(
                    "Manage and track your medical inventory",
                    class_name="text-gray-500 mt-1",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.span(
                    f"{InventoryState.filtered_items.length()} items",
                    class_name="text-sm font-medium text-gray-500 bg-gray-100 px-3 py-1 rounded-full",
                )
            ),
            class_name="flex items-start justify-between mb-8",
        ),
        rx.cond(
            InventoryState.active_tag,
            rx.el.div(
                rx.el.span(
                    f"Filtering by tag: ", class_name="text-sm text-emerald-800"
                ),
                rx.el.span(
                    InventoryState.active_tag,
                    class_name="text-sm font-bold text-emerald-900 ml-1",
                ),
                rx.el.button(
                    rx.icon("x", class_name="w-4 h-4 text-emerald-700"),
                    on_click=InventoryState.clear_tag_filter,
                    class_name="ml-3 hover:bg-emerald-200 rounded-full p-0.5 transition-colors",
                ),
                class_name="bg-emerald-100 border border-emerald-200 px-4 py-2 rounded-lg mb-6 flex items-center inline-flex animate-fadeIn",
            ),
        ),
        rx.cond(
            InventoryState.view_mode == "grid",
            rx.el.div(
                rx.foreach(InventoryState.filtered_items, item_card_grid),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        "Item Details",
                        class_name="w-1/3 text-xs font-semibold text-gray-500 uppercase tracking-wider pl-14",
                    ),
                    rx.el.div(
                        "Category",
                        class_name="w-1/6 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.div(
                        "Location",
                        class_name="w-1/6 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.div(
                        "Quantity",
                        class_name="w-1/6 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right pr-4",
                    ),
                    rx.el.div(
                        "Expires",
                        class_name="w-1/6 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.div(
                        "Status",
                        class_name="w-32 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right",
                    ),
                    class_name="flex items-center px-4 py-3 bg-gray-50 rounded-lg mb-2",
                ),
                rx.el.div(
                    rx.foreach(InventoryState.filtered_items, item_row_list),
                    class_name="space-y-2",
                ),
                class_name="w-full",
            ),
        ),
        rx.cond(
            InventoryState.filtered_items.length() == 0,
            rx.el.div(
                rx.icon("package-open", class_name="w-16 h-16 text-gray-300 mb-4"),
                rx.el.h3(
                    "No items found", class_name="text-lg font-medium text-gray-900"
                ),
                rx.el.p(
                    "Try adjusting your search or filters", class_name="text-gray-500"
                ),
                class_name="flex flex-col items-center justify-center py-24 bg-white rounded-2xl border border-gray-100 border-dashed",
            ),
        ),
        class_name="max-w-7xl mx-auto",
    )


def content() -> rx.Component:
    return rx.el.main(
        rx.match(
            InventoryState.active_nav_item,
            ("Items", items_view()),
            ("Tags", tags_page()),
            ("Labels", labels_page()),
            ("Settings", settings_page()),
            items_view(),
        ),
        add_edit_modal(),
        item_detail_modal(),
        move_stock_modal(),
        adjust_stock_modal(),
        checkout_modal(),
        class_name="flex-1 p-8 overflow-y-auto bg-gray-50/50",
    )