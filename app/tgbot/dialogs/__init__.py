from .user.user_dialog import catalog_dialog
from .admin.admin_dialog import add_categories_dialog, add_product


dialogs_list = [
    catalog_dialog,
    add_categories_dialog,
    add_product,
]

__all__ = [
    'dialogs_list'
]