import reflex as rx
from app.states.inventory_state import InventoryState


def form_input(
    label: str, placeholder: str, key: str, type_: str = "text", default_value: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            type=type_,
            placeholder=placeholder,
            default_value=default_value,
            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 text-sm",
            on_change=lambda val: InventoryState.update_form_data(key, val),
        ),
        class_name="mb-4",
    )


def add_edit_modal() -> rx.Component:
    return rx.cond(
        InventoryState.is_add_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        rx.cond(
                            InventoryState.selected_item["id"],
                            "Edit Item",
                            "Add New Item",
                        ),
                        class_name="text-lg font-bold text-gray-900",
                    ),
                    rx.el.button(
                        rx.icon(
                            "x", class_name="w-5 h-5 text-gray-400 hover:text-gray-600"
                        ),
                        on_click=InventoryState.close_add_modal,
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        form_input(
                            "Item Name",
                            "e.g. Surgical Masks",
                            "name",
                            default_value=InventoryState.selected_item["name"],
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Category",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option(
                                        "Select Category", value="", disabled=True
                                    ),
                                    rx.foreach(
                                        InventoryState.categories,
                                        lambda cat: rx.el.option(
                                            cat["name"], value=cat["name"]
                                        ),
                                    ),
                                    value=InventoryState.selected_item["category"],
                                    on_change=lambda val: InventoryState.update_form_data(
                                        "category", val
                                    ),
                                    class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 text-sm appearance-none bg-white",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="w-4 h-4 text-gray-400 absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                            class_name="mb-4",
                        ),
                        class_name="grid grid-cols-2 gap-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Location",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option(
                                        "Select Location", value="", disabled=True
                                    ),
                                    rx.foreach(
                                        InventoryState.locations,
                                        lambda loc: rx.el.option(
                                            loc["name"], value=loc["name"]
                                        ),
                                    ),
                                    value=InventoryState.selected_item["location"],
                                    on_change=lambda val: InventoryState.update_form_data(
                                        "location", val
                                    ),
                                    class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 text-sm appearance-none bg-white",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="w-4 h-4 text-gray-400 absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                            class_name="mb-4",
                        ),
                        form_input(
                            "Expiration Date",
                            "YYYY-MM-DD",
                            "expiration_date",
                            type_="date",
                            default_value=InventoryState.selected_item[
                                "expiration_date"
                            ],
                        ),
                        class_name="grid grid-cols-2 gap-4",
                    ),
                    rx.el.div(
                        form_input(
                            "Quantity",
                            "0",
                            "quantity",
                            type_="number",
                            default_value=InventoryState.selected_item[
                                "quantity"
                            ].to_string(),
                        ),
                        form_input(
                            "Unit",
                            "e.g. pcs, boxes",
                            "unit",
                            default_value=InventoryState.selected_item["unit"],
                        ),
                        class_name="grid grid-cols-2 gap-4",
                    ),
                    rx.el.div(
                        form_input(
                            "Price ($)",
                            "0.00",
                            "price",
                            type_="number",
                            default_value=InventoryState.selected_item[
                                "price"
                            ].to_string(),
                        ),
                        form_input(
                            "Lot Number",
                            "Lot #",
                            "lot_number",
                            default_value=InventoryState.selected_item["lot_number"],
                        ),
                        class_name="grid grid-cols-2 gap-4",
                    ),
                    form_input(
                        "Serial Number",
                        "Serial # (Optional)",
                        "serial_number",
                        default_value=InventoryState.selected_item["serial_number"],
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Tags",
                            class_name="block text-sm font-medium text-gray-700 mb-2",
                        ),
                        rx.el.div(
                            rx.foreach(
                                InventoryState.tags,
                                lambda tag: rx.el.button(
                                    tag["name"],
                                    class_name=rx.cond(
                                        InventoryState.selected_item["tags"].contains(
                                            tag["name"]
                                        ),
                                        f"px-3 py-1 rounded-full text-xs font-medium border border-{tag['color']}-200 bg-{tag['color']}-100 text-{tag['color']}-700 transition-all",
                                        "px-3 py-1 rounded-full text-xs font-medium border border-gray-200 bg-gray-50 text-gray-600 hover:bg-gray-100 transition-all opacity-60",
                                    ),
                                    on_click=lambda: InventoryState.toggle_tag_selection(
                                        tag["name"]
                                    ),
                                ),
                            ),
                            class_name="flex flex-wrap gap-2",
                        ),
                        class_name="mt-4",
                    ),
                    class_name="space-y-1",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        class_name="px-4 py-2 text-gray-600 font-medium hover:bg-gray-100 rounded-lg transition-colors",
                        on_click=InventoryState.close_add_modal,
                    ),
                    rx.el.button(
                        "Save Item",
                        class_name="px-6 py-2 bg-emerald-600 text-white font-medium rounded-lg hover:bg-emerald-700 shadow-lg shadow-emerald-600/20 transition-all",
                        on_click=InventoryState.save_item,
                    ),
                    class_name="flex justify-end gap-3 mt-6 pt-4 border-t border-gray-100",
                ),
                class_name="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-2xl transform transition-all",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4",
        ),
    )


def detail_row(label: str, value: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(label, class_name="text-sm text-gray-500 w-1/3"),
        rx.el.span(value, class_name="text-sm font-medium text-gray-900 w-2/3"),
        class_name="flex items-start py-2 border-b border-gray-50 last:border-0",
    )


def item_detail_modal() -> rx.Component:
    item = InventoryState.selected_item
    return rx.cond(
        InventoryState.is_detail_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Item Details", class_name="text-lg font-bold text-gray-900"
                    ),
                    rx.el.button(
                        rx.icon(
                            "x", class_name="w-5 h-5 text-gray-400 hover:text-gray-600"
                        ),
                        on_click=InventoryState.close_detail_modal,
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.image(
                            src=item["image"],
                            class_name="w-full h-48 object-contain bg-gray-50 rounded-xl mb-4",
                        ),
                        rx.el.div(
                            rx.el.h2(
                                item["name"],
                                class_name="text-xl font-bold text-gray-900 mb-1",
                            ),
                            rx.el.div(
                                rx.cond(
                                    item["is_checked_out"],
                                    rx.el.span(
                                        "CHECKED OUT",
                                        class_name="text-xs font-bold px-2 py-0.5 rounded bg-orange-100 text-orange-600",
                                    ),
                                    rx.el.span(
                                        item["status"].upper(),
                                        class_name="text-xs font-bold px-2 py-0.5 rounded bg-gray-100 text-gray-600",
                                    ),
                                ),
                                class_name="mb-4",
                            ),
                            class_name="text-center",
                        ),
                        class_name="w-1/3",
                    ),
                    rx.el.div(
                        rx.cond(
                            item["is_checked_out"],
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "user", class_name="w-4 h-4 text-orange-600"
                                    ),
                                    rx.el.span(
                                        f"Checked out by {item['checked_out_by']}",
                                        class_name="text-sm font-medium text-orange-800",
                                    ),
                                    class_name="flex items-center gap-2 mb-1",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "calendar-clock",
                                        class_name="w-4 h-4 text-orange-600",
                                    ),
                                    rx.el.span(
                                        f"Expected return: {item['expected_return']}",
                                        class_name="text-sm text-orange-700",
                                    ),
                                    class_name="flex items-center gap-2",
                                ),
                                class_name="bg-orange-50 border border-orange-100 rounded-lg p-3 mb-4",
                            ),
                        ),
                        detail_row("Category", item["category"]),
                        detail_row("Location", item["location"]),
                        detail_row("Quantity", f"{item['quantity']} {item['unit']}"),
                        detail_row("Value", f"${item['price']:.2f}"),
                        detail_row("Lot Number", item["lot_number"]),
                        detail_row("Serial Number", item["serial_number"]),
                        detail_row("Expiration", item["expiration_date"]),
                        rx.el.div(
                            rx.el.span(
                                "Tags", class_name="text-sm text-gray-500 w-1/3"
                            ),
                            rx.el.div(
                                rx.foreach(
                                    item["tags"],
                                    lambda t: rx.el.span(
                                        t,
                                        class_name="inline-block px-2 py-0.5 rounded-full text-xs font-medium bg-gray-200 text-gray-700 mr-1",
                                    ),
                                ),
                                class_name="w-2/3 flex flex-wrap gap-1",
                            ),
                            class_name="flex items-start py-2 border-b border-gray-50 last:border-0",
                        ),
                        class_name="w-2/3 bg-gray-50 rounded-xl p-4",
                    ),
                    class_name="flex gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h4(
                            "History Log",
                            class_name="text-sm font-semibold text-gray-900 mb-3",
                        ),
                        rx.el.div(
                            rx.foreach(
                                InventoryState.history_log,
                                lambda log: rx.cond(
                                    log["item_name"] == item["name"],
                                    rx.el.div(
                                        rx.el.div(
                                            rx.el.span(
                                                log["action"],
                                                class_name="text-xs font-medium text-gray-900",
                                            ),
                                            rx.el.span(
                                                log["timestamp"],
                                                class_name="text-xs text-gray-500",
                                            ),
                                            class_name="flex justify-between mb-1",
                                        ),
                                        rx.el.p(
                                            log["detail"],
                                            class_name="text-xs text-gray-600",
                                        ),
                                        class_name="py-2 border-b border-gray-100 last:border-0",
                                    ),
                                ),
                            ),
                            class_name="max-h-40 overflow-y-auto pr-2",
                        ),
                        class_name="w-full bg-gray-50 rounded-xl p-4 mb-6",
                    ),
                    class_name="border-t border-gray-100 pt-6 mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("trash-2", class_name="w-4 h-4"),
                        "Delete",
                        class_name="flex items-center gap-2 px-4 py-2 text-red-600 font-medium hover:bg-red-50 rounded-lg transition-colors",
                        on_click=InventoryState.delete_item,
                    ),
                    rx.el.div(
                        rx.cond(
                            item["is_checked_out"],
                            rx.el.button(
                                rx.icon("log-in", class_name="w-4 h-4"),
                                "Check In",
                                class_name="flex items-center gap-2 px-4 py-2 bg-orange-100 text-orange-700 font-medium hover:bg-orange-200 rounded-lg transition-colors",
                                on_click=InventoryState.check_in_item,
                            ),
                            rx.el.button(
                                rx.icon("log-out", class_name="w-4 h-4"),
                                "Check Out",
                                class_name="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 font-medium hover:bg-gray-200 rounded-lg transition-colors",
                                on_click=InventoryState.open_checkout_modal,
                            ),
                        ),
                        rx.el.button(
                            rx.icon("arrow-left-right", class_name="w-4 h-4"),
                            "Move",
                            class_name="flex items-center gap-2 px-4 py-2 text-gray-700 font-medium hover:bg-gray-100 rounded-lg transition-colors",
                            on_click=InventoryState.open_move_modal,
                        ),
                        rx.el.button(
                            rx.icon("sliders-horizontal", class_name="w-4 h-4"),
                            "Adjust Stock",
                            class_name="flex items-center gap-2 px-4 py-2 text-gray-700 font-medium hover:bg-gray-100 rounded-lg transition-colors",
                            on_click=InventoryState.open_adjust_modal,
                        ),
                        rx.el.button(
                            rx.icon("pencil", class_name="w-4 h-4"),
                            "Edit",
                            class_name="flex items-center gap-2 px-6 py-2 bg-emerald-600 text-white font-medium rounded-lg hover:bg-emerald-700 shadow-lg shadow-emerald-600/20 transition-all",
                            on_click=lambda: InventoryState.edit_item(item),
                        ),
                        class_name="flex gap-2",
                    ),
                    class_name="flex justify-between items-center pt-4 border-t border-gray-100",
                ),
                class_name="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-3xl transform transition-all",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4",
        ),
    )


def move_stock_modal() -> rx.Component:
    return rx.cond(
        InventoryState.is_move_open,
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Move Stock", class_name="text-lg font-bold text-gray-900 mb-4"
                ),
                rx.el.p(
                    f"Moving: {InventoryState.selected_item['name']}",
                    class_name="text-sm text-gray-500 mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "To Location",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option(
                                "Select New Location", value="", disabled=True
                            ),
                            rx.foreach(
                                InventoryState.locations,
                                lambda loc: rx.el.option(
                                    loc["name"], value=loc["name"]
                                ),
                            ),
                            on_change=lambda val: InventoryState.update_form_data(
                                "to_location", val
                            ),
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 text-sm appearance-none bg-white",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="w-4 h-4 text-gray-400 absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none",
                        ),
                        class_name="relative",
                    ),
                    class_name="mb-4",
                ),
                form_input(
                    "Quantity",
                    "Amount to move",
                    "quantity",
                    type_="number",
                    default_value="1",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg",
                        on_click=InventoryState.close_move_modal,
                    ),
                    rx.el.button(
                        "Confirm Move",
                        class_name="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700",
                        on_click=InventoryState.confirm_move,
                    ),
                    class_name="flex justify-end gap-3 mt-4",
                ),
                class_name="bg-white rounded-xl shadow-2xl p-6 w-full max-w-md",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4",
        ),
    )


def checkout_modal() -> rx.Component:
    return rx.cond(
        InventoryState.is_checkout_open,
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Check Out Item", class_name="text-lg font-bold text-gray-900 mb-4"
                ),
                rx.el.p(
                    f"Checking out: {InventoryState.selected_item['name']}",
                    class_name="text-sm text-gray-500 mb-4",
                ),
                form_input("Checked Out By", "Person name or ID", "checked_out_by"),
                form_input(
                    "Expected Return Date",
                    "YYYY-MM-DD",
                    "expected_return",
                    type_="date",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg",
                        on_click=InventoryState.close_checkout_modal,
                    ),
                    rx.el.button(
                        "Confirm Checkout",
                        class_name="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700",
                        on_click=InventoryState.confirm_checkout,
                    ),
                    class_name="flex justify-end gap-3 mt-4",
                ),
                class_name="bg-white rounded-xl shadow-2xl p-6 w-full max-w-md",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4",
        ),
    )


def adjust_stock_modal() -> rx.Component:
    return rx.cond(
        InventoryState.is_adjust_open,
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Adjust Stock", class_name="text-lg font-bold text-gray-900 mb-4"
                ),
                rx.el.p(
                    f"Adjusting: {InventoryState.selected_item['name']}",
                    class_name="text-sm text-gray-500 mb-4",
                ),
                form_input(
                    "New Quantity",
                    "Enter total quantity",
                    "quantity",
                    type_="number",
                    default_value=InventoryState.selected_item["quantity"].to_string(),
                ),
                form_input("Note", "Reason for adjustment", "note"),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg",
                        on_click=InventoryState.close_adjust_modal,
                    ),
                    rx.el.button(
                        "Save Adjustment",
                        class_name="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700",
                        on_click=InventoryState.confirm_adjust,
                    ),
                    class_name="flex justify-end gap-3 mt-4",
                ),
                class_name="bg-white rounded-xl shadow-2xl p-6 w-full max-w-md",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4",
        ),
    )