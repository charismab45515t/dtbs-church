{
    "name": "Church Basic",
    "version": "0.1",
    "category": "church",
    "description": """Church Management System - Basic""",
    "author": "DTBS",
    "website": "http://www.dtbsindo.web.id",
    "license": "AGPL-3",
    "depends": ["base", "web_groupby_expand"],
    "data": [
        # view
        "view/tag.xml",
        "view/religion.xml",
        "view/member_template.xml",

        # view
        "view/church_basic.xml",
        "view/member_o2m.xml",
        "view/contact_type.xml",
        "view/last_education.xml",
        "view/type_service.xml",

        # menu
        "view/menu.xml",
    ],
    "application": True,
    "installable": True,
}

