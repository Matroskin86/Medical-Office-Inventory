import reflex as rx
import logging
from typing import TypedDict
from datetime import datetime, timedelta


class FolderItem(TypedDict):
    id: str
    name: str
    count: int
    icon: str
    color: str


class Tag(TypedDict):
    id: str
    name: str
    color: str


class Location(TypedDict):
    id: str
    name: str
    address: str


class InventoryItem(TypedDict):
    id: str
    name: str
    category: str
    location: str
    quantity: int
    unit: str
    price: float
    lot_number: str
    serial_number: str
    expiration_date: str
    image: str
    status: str
    is_checked_out: bool
    checked_out_by: str
    checked_out_date: str
    expected_return: str
    tags: list[str]


class HistoryLog(TypedDict):
    id: str
    item_name: str
    action: str
    detail: str
    timestamp: str


class InventoryState(rx.State):
    active_nav_item: str = "Items"
    places_expanded: bool = True
    active_folder: str = "All Items"
    active_tag: str | None = None
    search_query: str = ""
    sort_option: str = "newest"
    view_mode: str = "grid"
    is_add_open: bool = False
    is_detail_open: bool = False
    is_move_open: bool = False
    is_adjust_open: bool = False
    is_checkout_open: bool = False
    new_tag_name: str = ""
    new_tag_color: str = "blue"
    new_location_name: str = ""
    new_category_name: str = ""
    selected_item: InventoryItem = {
        "id": "",
        "name": "",
        "category": "",
        "location": "",
        "quantity": 0,
        "unit": "",
        "price": 0.0,
        "lot_number": "",
        "serial_number": "",
        "expiration_date": "",
        "image": "",
        "status": "",
        "is_checked_out": False,
        "checked_out_by": "",
        "checked_out_date": "",
        "expected_return": "",
        "tags": [],
    }
    form_data: dict = {}
    history_log: list[HistoryLog] = []
    tags: list[Tag] = [
        {"id": "1", "name": "Urgent", "color": "red"},
        {"id": "2", "name": "Fragile", "color": "yellow"},
        {"id": "3", "name": "Refrigerated", "color": "blue"},
        {"id": "4", "name": "Sterile", "color": "emerald"},
    ]
    locations: list[Location] = [
        {"id": "1", "name": "North Richland Hills", "address": "Clinic A"},
        {"id": "2", "name": "Austin", "address": "Clinic B"},
        {"id": "3", "name": "Dallas Main", "address": "Hospital A"},
    ]
    categories: list[FolderItem] = [
        {
            "id": "bio",
            "name": "Bio Hazard Materials",
            "count": 12,
            "icon": "biohazard",
            "color": "text-red-500",
        },
        {
            "id": "supplies",
            "name": "Supplies",
            "count": 145,
            "icon": "package",
            "color": "text-blue-500",
        },
        {
            "id": "stomatology",
            "name": "Stomatology",
            "count": 30,
            "icon": "activity",
            "color": "text-emerald-500",
        },
        {
            "id": "pt",
            "name": "PT Equipment",
            "count": 25,
            "icon": "dumbbell",
            "color": "text-purple-500",
        },
        {
            "id": "meds",
            "name": "Medications",
            "count": 80,
            "icon": "pill",
            "color": "text-orange-500",
        },
        {
            "id": "computer",
            "name": "Computer Equipment",
            "count": 15,
            "icon": "monitor",
            "color": "text-gray-500",
        },
    ]
    all_items: list[InventoryItem] = [
        {
            "id": "1",
            "name": "Surgical Masks (N95)",
            "category": "Supplies",
            "location": "North Richland Hills",
            "quantity": 500,
            "unit": "pcs",
            "price": 1.25,
            "lot_number": "L-88392",
            "serial_number": "-",
            "expiration_date": "2025-12-01",
            "image": "/masks_product_white.png",
            "status": "ok",
            "is_checked_out": False,
            "checked_out_by": "",
            "checked_out_date": "",
            "expected_return": "",
            "tags": ["Sterile"],
        },
        {
            "id": "2",
            "name": "Epinephrine Injection",
            "category": "Medications",
            "location": "Austin",
            "quantity": 25,
            "unit": "vials",
            "price": 45.0,
            "lot_number": "EPI-2023-01",
            "serial_number": "SN-99283",
            "expiration_date": "2023-11-15",
            "image": "/product_vial_medical.png",
            "status": "warning",
            "is_checked_out": False,
            "checked_out_by": "",
            "checked_out_date": "",
            "expected_return": "",
            "tags": ["Urgent", "Refrigerated"],
        },
        {
            "id": "3",
            "name": "Dental Amalgam",
            "category": "Stomatology",
            "location": "North Richland Hills",
            "quantity": 12,
            "unit": "kits",
            "price": 120.0,
            "lot_number": "DA-002",
            "serial_number": "-",
            "expiration_date": "2026-05-20",
            "image": "/product_dental_amalgam.png",
            "status": "ok",
            "is_checked_out": False,
            "checked_out_by": "",
            "checked_out_date": "",
            "expected_return": "",
            "tags": [],
        },
        {
            "id": "4",
            "name": "Propofol",
            "category": "Medications",
            "location": "North Richland Hills",
            "quantity": 5,
            "unit": "vials",
            "price": 15.5,
            "lot_number": "PRO-992",
            "serial_number": "SN-11223",
            "expiration_date": "2023-08-01",
            "image": "/product_vial_white.png",
            "status": "expired",
            "is_checked_out": False,
            "checked_out_by": "",
            "checked_out_date": "",
            "expected_return": "",
            "tags": ["Refrigerated"],
        },
        {
            "id": "5",
            "name": "Resistance Bands Set",
            "category": "PT Equipment",
            "location": "Austin",
            "quantity": 15,
            "unit": "sets",
            "price": 25.0,
            "lot_number": "-",
            "serial_number": "-",
            "expiration_date": "2030-01-01",
            "image": "/bands_professional_product.png",
            "status": "ok",
            "is_checked_out": True,
            "checked_out_by": "Dr. Smith",
            "checked_out_date": "2023-10-25",
            "expected_return": "2023-10-30",
            "tags": [],
        },
        {
            "id": "6",
            "name": "Dell Optiplex 7080",
            "category": "Computer Equipment",
            "location": "Austin",
            "quantity": 3,
            "unit": "units",
            "price": 850.0,
            "lot_number": "-",
            "serial_number": "CN-0F9283",
            "expiration_date": "-",
            "image": "/product_computer_professional.png",
            "status": "ok",
            "is_checked_out": False,
            "checked_out_by": "",
            "checked_out_date": "",
            "expected_return": "",
            "tags": ["Fragile"],
        },
        {
            "id": "7",
            "name": "Biohazard Waste Bags",
            "category": "Bio Hazard Materials",
            "location": "North Richland Hills",
            "quantity": 200,
            "unit": "pcs",
            "price": 0.45,
            "lot_number": "BIO-22",
            "serial_number": "-",
            "expiration_date": "2028-01-01",
            "image": "/bags_red_biohazard.png",
            "status": "ok",
            "is_checked_out": False,
            "checked_out_by": "",
            "checked_out_date": "",
            "expected_return": "",
            "tags": ["Urgent"],
        },
        {
            "id": "8",
            "name": "Amoxicillin 500mg",
            "category": "Medications",
            "location": "Austin",
            "quantity": 300,
            "unit": "capsules",
            "price": 0.15,
            "lot_number": "AMX-552",
            "serial_number": "-",
            "expiration_date": "2023-12-10",
            "image": "/product_white_professional.png",
            "status": "warning",
            "is_checked_out": False,
            "checked_out_by": "",
            "checked_out_date": "",
            "expected_return": "",
            "tags": [],
        },
        {
            "id": "9",
            "name": "Sterile Gloves (L)",
            "category": "Supplies",
            "location": "North Richland Hills",
            "quantity": 1000,
            "unit": "pairs",
            "price": 0.2,
            "lot_number": "GLV-992",
            "serial_number": "-",
            "expiration_date": "2025-06-30",
            "image": "/gloves_white_medical.png",
            "status": "ok",
            "is_checked_out": False,
            "checked_out_by": "",
            "checked_out_date": "",
            "expected_return": "",
            "tags": ["Sterile"],
        },
        {
            "id": "10",
            "name": "Ultrasound Gel",
            "category": "Supplies",
            "location": "Austin",
            "quantity": 20,
            "unit": "bottles",
            "price": 5.5,
            "lot_number": "UG-221",
            "serial_number": "-",
            "expiration_date": "2024-02-15",
            "image": "/ultrasound_gel_bottle.png",
            "status": "ok",
            "is_checked_out": False,
            "checked_out_by": "",
            "checked_out_date": "",
            "expected_return": "",
            "tags": [],
        },
        {
            "id": "11",
            "name": "Defibrillator Pads",
            "category": "Supplies",
            "location": "Austin",
            "quantity": 4,
            "unit": "sets",
            "price": 45.0,
            "lot_number": "DEF-11",
            "serial_number": "-",
            "expiration_date": "2023-09-15",
            "image": "/pads_emergency_professional.png",
            "status": "expired",
            "is_checked_out": False,
            "checked_out_by": "",
            "checked_out_date": "",
            "expected_return": "",
            "tags": ["Urgent"],
        },
        {
            "id": "12",
            "name": "Dental Mirror",
            "category": "Stomatology",
            "location": "Austin",
            "quantity": 50,
            "unit": "pcs",
            "price": 3.5,
            "lot_number": "-",
            "serial_number": "-",
            "expiration_date": "-",
            "image": "/dental_mirror_professional.png",
            "status": "ok",
            "is_checked_out": False,
            "checked_out_by": "",
            "checked_out_date": "",
            "expected_return": "",
            "tags": ["Fragile"],
        },
    ]

    @rx.var
    def filtered_items(self) -> list[InventoryItem]:
        items = self.all_items
        if self.active_folder == "Expired":
            items = [i for i in items if i["status"] == "expired"]
        elif self.active_folder != "All Items":
            items = [
                i
                for i in items
                if i["category"] == self.active_folder
                or i["location"] == self.active_folder
            ]
        if self.active_tag:
            items = [i for i in items if self.active_tag in i["tags"]]
        if self.search_query:
            query = self.search_query.lower()
            items = [
                i
                for i in items
                if query in i["name"].lower()
                or query in i["lot_number"].lower()
                or query in i["serial_number"].lower()
            ]
        if self.sort_option == "newest":
            items = items[::-1]
        elif self.sort_option == "oldest":
            items = items
        elif self.sort_option == "az":
            items = sorted(items, key=lambda x: x["name"])
        elif self.sort_option == "qty_desc":
            items = sorted(items, key=lambda x: x["quantity"], reverse=True)
        elif self.sort_option == "expiration":
            items = sorted(
                items,
                key=lambda x: x["expiration_date"]
                if x["expiration_date"] != "-"
                else "9999-99-99",
            )
        return items

    @rx.var
    def tag_counts(self) -> dict[str, int]:
        counts = {}
        for tag in self.tags:
            count = sum((1 for item in self.all_items if tag["name"] in item["tags"]))
            counts[tag["name"]] = count
        return counts

    @rx.event
    def set_nav_item(self, item_name: str):
        self.active_nav_item = item_name

    @rx.event
    def toggle_places(self):
        self.places_expanded = not self.places_expanded

    @rx.event
    def set_folder(self, folder_name: str):
        self.active_folder = folder_name
        self.active_tag = None
        self.active_nav_item = "Items"

    @rx.event
    def select_tag_filter(self, tag_name: str):
        self.active_tag = tag_name
        self.active_nav_item = "Items"
        self.active_folder = "All Items"

    @rx.event
    def clear_tag_filter(self):
        self.active_tag = None

    @rx.event
    def set_search(self, query: str):
        self.search_query = query

    @rx.event
    def set_sort(self, sort_val: str):
        self.sort_option = sort_val

    @rx.event
    def set_view_mode(self, mode: str):
        self.view_mode = mode

    @rx.event
    def open_add_modal(self):
        self.selected_item = {
            "id": "",
            "name": "",
            "category": "",
            "location": "",
            "quantity": 0,
            "unit": "",
            "price": 0.0,
            "lot_number": "",
            "serial_number": "",
            "expiration_date": "",
            "image": "",
            "status": "",
            "tags": [],
        }
        self.form_data = {"tags": []}
        self.is_add_open = True

    @rx.event
    def edit_item(self, item: InventoryItem):
        self.selected_item = item
        self.form_data = item.copy()
        self.is_add_open = True
        self.is_detail_open = False

    @rx.event
    def close_add_modal(self):
        self.is_add_open = False
        self.form_data = {}

    @rx.event
    def update_form_data(self, key: str, value: str):
        if key in ["quantity", "price"]:
            try:
                self.form_data[key] = float(value) if key == "price" else int(value)
            except ValueError as e:
                logging.exception(f"Error converting {key} value '{value}': {e}")
        else:
            self.form_data[key] = value

    @rx.event
    def toggle_tag_selection(self, tag_name: str):
        current_tags = self.form_data.get("tags", self.selected_item.get("tags", []))
        if tag_name in current_tags:
            current_tags = [t for t in current_tags if t != tag_name]
        else:
            current_tags = current_tags + [tag_name]
        self.form_data["tags"] = current_tags
        self.selected_item["tags"] = current_tags

    @rx.event
    def save_item(self):
        if self.selected_item["id"]:
            for i, item in enumerate(self.all_items):
                if item["id"] == self.selected_item["id"]:
                    self.all_items[i] = {**item, **self.form_data}
                    break
            self.add_history_log(
                self.form_data.get("name", "Item"), "Updated", "Item details updated"
            )
        else:
            import uuid

            new_item = self.form_data.copy()
            new_item["id"] = str(uuid.uuid4())
            new_item["status"] = "ok"
            if "image" not in new_item:
                new_item["image"] = "/placeholder.svg"
            self.all_items.append(new_item)
            self.add_history_log(
                new_item.get("name", "New Item"), "Created", "Initial stock added"
            )
        self.is_add_open = False
        self.form_data = {}

    @rx.event
    def open_detail_modal(self, item: InventoryItem):
        self.selected_item = item
        self.is_detail_open = True

    @rx.event
    def close_detail_modal(self):
        self.is_detail_open = False

    @rx.event
    def open_move_modal(self):
        self.form_data = {"quantity": 1, "to_location": ""}
        self.is_move_open = True
        self.is_detail_open = False

    @rx.event
    def close_move_modal(self):
        self.is_move_open = False

    @rx.event
    def confirm_move(self):
        qty = int(self.form_data.get("quantity", 0))
        to_loc = self.form_data.get("to_location", "")
        if qty > 0 and to_loc and self.selected_item:
            if qty >= self.selected_item["quantity"]:
                for i, item in enumerate(self.all_items):
                    if item["id"] == self.selected_item["id"]:
                        self.all_items[i]["location"] = to_loc
                        self.selected_item["location"] = to_loc
                        break
            else:
                import uuid

                for i, item in enumerate(self.all_items):
                    if item["id"] == self.selected_item["id"]:
                        self.all_items[i]["quantity"] -= qty
                        self.selected_item["quantity"] -= qty
                        break
                new_item = self.selected_item.copy()
                new_item["id"] = str(uuid.uuid4())
                new_item["quantity"] = qty
                new_item["location"] = to_loc
                self.all_items.append(new_item)
            self.add_history_log(
                self.selected_item["name"], "Moved", f"Moved {qty} to {to_loc}"
            )
            self.is_move_open = False

    @rx.event
    def open_adjust_modal(self):
        self.form_data = {"quantity": self.selected_item["quantity"], "note": ""}
        self.is_adjust_open = True
        self.is_detail_open = False

    @rx.event
    def close_adjust_modal(self):
        self.is_adjust_open = False

    @rx.event
    def confirm_adjust(self):
        new_qty = int(self.form_data.get("quantity", 0))
        note = self.form_data.get("note", "Stock adjustment")
        if self.selected_item:
            old_qty = self.selected_item["quantity"]
            for i, item in enumerate(self.all_items):
                if item["id"] == self.selected_item["id"]:
                    self.all_items[i]["quantity"] = new_qty
                    self.selected_item["quantity"] = new_qty
                    break
            diff = new_qty - old_qty
            action = "Added" if diff > 0 else "Removed"
            self.add_history_log(
                self.selected_item["name"],
                action,
                f"{action} {abs(diff)} units. Note: {note}",
            )
            self.is_adjust_open = False

    @rx.event
    def open_checkout_modal(self):
        self.form_data = {"checked_out_by": "", "expected_return": ""}
        self.is_checkout_open = True
        self.is_detail_open = False

    @rx.event
    def close_checkout_modal(self):
        self.is_checkout_open = False

    @rx.event
    def confirm_checkout(self):
        checked_out_by = self.form_data.get("checked_out_by", "Unknown")
        expected_return = self.form_data.get("expected_return", "")
        if self.selected_item:
            for i, item in enumerate(self.all_items):
                if item["id"] == self.selected_item["id"]:
                    self.all_items[i]["is_checked_out"] = True
                    self.all_items[i]["checked_out_by"] = checked_out_by
                    self.all_items[i]["checked_out_date"] = datetime.now().strftime(
                        "%Y-%m-%d"
                    )
                    self.all_items[i]["expected_return"] = expected_return
                    self.selected_item["is_checked_out"] = True
                    self.selected_item["checked_out_by"] = checked_out_by
                    self.selected_item["checked_out_date"] = datetime.now().strftime(
                        "%Y-%m-%d"
                    )
                    self.selected_item["expected_return"] = expected_return
                    break
            self.add_history_log(
                self.selected_item["name"],
                "Checked Out",
                f"Checked out by {checked_out_by}. Return expected: {expected_return}",
            )
            self.is_checkout_open = False

    @rx.event
    def check_in_item(self):
        if self.selected_item:
            for i, item in enumerate(self.all_items):
                if item["id"] == self.selected_item["id"]:
                    self.all_items[i]["is_checked_out"] = False
                    self.all_items[i]["checked_out_by"] = ""
                    self.all_items[i]["checked_out_date"] = ""
                    self.all_items[i]["expected_return"] = ""
                    self.selected_item["is_checked_out"] = False
                    self.selected_item["checked_out_by"] = ""
                    self.selected_item["checked_out_date"] = ""
                    self.selected_item["expected_return"] = ""
                    break
            self.add_history_log(
                self.selected_item["name"], "Checked In", "Item returned to inventory"
            )
            self.is_detail_open = False

    @rx.event
    def delete_item(self):
        if self.selected_item:
            self.all_items = [
                i for i in self.all_items if i["id"] != self.selected_item["id"]
            ]
            self.add_history_log(
                self.selected_item["name"], "Deleted", "Item removed from inventory"
            )
            self.is_detail_open = False

    @rx.event
    def add_history_log(self, name: str, action: str, detail: str):
        import uuid

        self.history_log.insert(
            0,
            {
                "id": str(uuid.uuid4()),
                "item_name": name,
                "action": action,
                "detail": detail,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            },
        )

    @rx.event
    def add_tag(self):
        if self.new_tag_name:
            import uuid

            self.tags.append(
                {
                    "id": str(uuid.uuid4()),
                    "name": self.new_tag_name,
                    "color": self.new_tag_color,
                }
            )
            self.new_tag_name = ""

    @rx.event
    def delete_tag(self, tag_id: str):
        self.tags = [t for t in self.tags if t["id"] != tag_id]

    @rx.event
    def set_new_tag_name(self, name: str):
        self.new_tag_name = name

    @rx.event
    def set_new_tag_color(self, color: str):
        self.new_tag_color = color

    @rx.event
    def add_location(self):
        if self.new_location_name:
            import uuid

            self.locations.append(
                {
                    "id": str(uuid.uuid4()),
                    "name": self.new_location_name,
                    "address": "New Location",
                }
            )
            self.new_location_name = ""

    @rx.event
    def delete_location(self, loc_id: str):
        self.locations = [l for l in self.locations if l["id"] != loc_id]

    @rx.event
    def set_new_location_name(self, name: str):
        self.new_location_name = name

    @rx.event
    def add_category(self):
        if self.new_category_name:
            import uuid

            self.categories.append(
                {
                    "id": str(uuid.uuid4()),
                    "name": self.new_category_name,
                    "count": 0,
                    "icon": "folder",
                    "color": "text-gray-500",
                }
            )
            self.new_category_name = ""

    @rx.event
    def delete_category(self, cat_id: str):
        self.categories = [c for c in self.categories if c["id"] != cat_id]

    @rx.event
    def set_new_category_name(self, name: str):
        self.new_category_name = name