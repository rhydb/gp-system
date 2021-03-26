# just so that Admin.py isnt clogged up by this
# should be re-added on release
new_user_form = [
    {
        "name": "Patient ID",
        "type": "entry"
    },
    {
        "name": "Name",
        "type": "entry",
        "required": True
    },
    {
        "name": "Date of Birth",
        "type": "entry",
        "required": True
    },
    {
        "name": "Gender",
        "required": True,
        "type": "dropdown",
        "menu_items": ["Male", "Female"]
    },
    {
        "name": "E-Mail",
        "type": "entry"
    },
    {
        "name": "Phone",
        "type": "entry"
    },
    {
        "name": "Post Code",
        "required": True,
        "type": "entry"
    },
    {
        "name": "Street",
        "required": True,
        "type": "entry"
    },
    {
        "name": "House",
        "required": True,
        "type": "entry",
    },
    {
        "name": "City",
        "required": True,
        "type": "entry"
    }
]
