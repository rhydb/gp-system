# just so that Admin.py isnt clogged up by this
# should be re-added on release
new_user_form = [
    {
        "name": "patient_id",
        "display_name": "Patient ID",
        "type": "entry"
    },
    {
        "name": "name",
        "display_name": "Name",
        "type": "entry",
        "required": True
    },
    {
        "name": "date_of_birth",
        "display_name": "Date of Birth",
        "type": "entry",
        "required": True
    },
    {
        "name": "gender",
        "display_name": "Gender",
        "required": True,
        "type": "dropdown",
        "menu_items": ["Male", "Female"]
    },
    {
        "name": "email",
        "display_name": "E-Mail",
        "type": "entry"
    },
    {
        "name": "phone",
        "display_name": "Phone",
        "type": "entry"
    },
    {
        "name": "post_code",
        "display_name": "Post Code",
        "required": True,
        "type": "entry"
    },
    {
        "name": "street",
        "display_name": "Street",
        "required": True,
        "type": "entry"
    },
    {
        "name": "house",
        "display_name": "House",
        "required": True,
        "type": "entry",
    },
    {
        "name": "city",
        "display_name": "City",
        "required": True,
        "type": "entry"
    }
]
