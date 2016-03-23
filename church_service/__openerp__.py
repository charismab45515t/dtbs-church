{
    "name": "Church Service",
    "version": "0.1",
    "category": "church",
    "description": """Church Management System - Service""",
    "author": "DTBS",
    "website": "http://www.dtbsindo.web.id",
    "license": "AGPL-3",
    "depends": ["church_basic", "church_pastoral"],
    "data": [
        # view
        "view/service.xml",
        "view/member.xml",
        "view/service_non_active.xml",

        # sequence
        "data/ir_sequence_data.xml",

        # cron
        "data/service_cron.xml",

        # menu
        "view/menu.xml"
    ],
    "application": True,
    "installable": True,
}

