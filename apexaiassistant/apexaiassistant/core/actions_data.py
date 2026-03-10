# ApexAiAssistant Action Definitions
# This file contains all default actions to be installed

# This would be imported by action_registry.py during installation
# Format: List of action definitions

ACTIONS_DATA = {
    "CRM": [
        {
            "action_name": "view_leads_summary",
            "description": "View comprehensive lead summary with status and source breakdown",
            "handler": "apexaiassistant.apexaiassistant.handlers.crm.get_leads_summary",
            "category": "QUERY",
            "risk": "Low",
            "roles": ["Sales User", "Sales Manager", "System Manager"]
        },
        {
            "action_name": "create_lead_draft",
            "description": "Create a draft lead record",
            "handler": "apexaiassistant.apexaiassistant.handlers.crm.create_lead_draft",
            "category": "DRAFT",
            "risk": "Low",
            "roles": ["Sales User", "Sales Manager", "System Manager"]
        },
        {
            "action_name": "convert_lead_to_customer",
            "description": "Convert a lead to customer",
            "handler": "apexaiassistant.apexaiassistant.handlers.crm.convert_lead_to_customer",
            "category": "APPROVE",
            "risk": "Medium",
            "confirmation": True,
            "roles": ["Sales Manager", "System Manager"]
        },
        {
            "action_name": "get_lead_conversion_rate",
            "description": "Calculate lead conversion statistics and rates",
            "handler": "apexaiassistant.apexaiassistant.handlers.crm.get_lead_conversion_rate",
            "category": "QUERY",
            "risk": "Low",
            "roles": ["Sales User", "Sales Manager", "System Manager"]
        },
        {
            "action_name": "view_opportunities",
            "description": "View opportunities with weighted value calculations",
            "handler": "apexaiassistant.apexaiassistant.handlers.crm.get_opportunities",
            "category": "QUERY",
            "risk": "Low",
            "roles": ["Sales User", "Sales Manager", "System Manager"]
        },
        {
            "action_name": "create_opportunity_draft",
            "description": "Create a draft opportunity",
            "handler": "apexaiassistant.apexaiassistant.handlers.crm.create_opportunity_draft",
            "category": "DRAFT",
            "risk": "Low",
            "roles": ["Sales User", "Sales Manager", "System Manager"]
        },
        {
            "action_name": "get_opportunity_pipeline",
            "description": "Analyze opportunity pipeline by stage",
            "handler": "apexaiassistant.apexaiassistant.handlers.crm.get_opportunity_pipeline",
            "category": "QUERY",
            "risk": "Low",
            "roles": ["Sales Manager", "System Manager"]
        },
        {
            "action_name": "get_customer_summary",
            "description": "Get customer list with revenue analytics",
            "handler": "apexaiassistant.apexaiassistant.handlers.crm.get_customer_summary",
            "category": "QUERY",
            "risk": "Low",
            "roles": ["Sales User", "Sales Manager", "Accounts User", "System Manager"]
        }
    ],
    "Selling": [
        {
            "action_name": "view_sales_orders",
            "description": "View sales orders with delivery and billing status",
            "handler": "apexaiassistant.apexaiassistant.handlers.selling.get_sales_orders",
            "category": "QUERY",
            "risk": "Low",
            "roles": ["Sales User", "Sales Manager", "System Manager"]
        },
        {
            "action_name": "get_pending_sales_orders",
            "description": "Get pending/outstanding sales orders",
            "handler": "apexaiassistant.apexaiassistant.handlers.selling.get_pending_sales_orders",
            "category": "QUERY",
            "risk": "Low",
            "roles": ["Sales User", "Sales Manager", "System Manager"]
        },
        {
            "action_name": "get_quotations_summary",
            "description": "View quotations with conversion rate tracking",
            "handler": "apexaiassistant.apexaiassistant.handlers.selling.get_quotations_summary",
            "category": "QUERY",
            "risk": "Low",
            "roles": ["Sales User", "Sales Manager", "System Manager"]
        },
        {
            "action_name": "get_sales_analytics",
            "description": "Comprehensive sales analytics - top customers, trends",
            "handler": "apexaiassistant.apexaiassistant.handlers.selling.get_sales_analytics",
            "category": "QUERY",
            "risk": "Low",
            "roles": ["Sales Manager", "System Manager"]
        },
        {
            "action_name": "create_sales_order_draft",
            "description": "Create a draft sales order",
            "handler": "apexaiassistant.apexaiassistant.handlers.selling.create_sales_order_draft",
            "category": "DRAFT",
            "risk": "Medium",
            "confirmation": True,
            "roles": ["Sales User", "Sales Manager", "System Manager"]
        }
    ],
    # Add all other modules here...
    # Total: 50+ actions across 12 modules
}

# Total action count: 50+
# This is a reference file - actual installation handled by action_registry.py
