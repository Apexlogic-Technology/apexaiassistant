# ApexAiAssistant - Complete Actions Manifest

## Total Actions: 50+ Across 12 Modules

This document lists ALL actions available in ApexAiAssistant with detailed descriptions.

---

## 📊 CRM Module (7 Actions)

### 1. **view_leads_summary**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View comprehensive lead summary with status and source breakdown
- **Parameters**:
  - `from_date` (optional): Filter from date
  - `to_date` (optional): Filter to date
  - `status` (optional): Lead status filter
  - `source` (optional): Lead source filter
- **Returns**: List of leads with statistics
- **Roles**: Sales User, Sales Manager, System Manager

### 2. **create_lead_draft**
- **Category**: DRAFT
- **Risk**: Low
- **Description**: Create a draft lead record
- **Parameters**:
  - `lead_name` (required): Name of the lead
  - `email_id` (optional): Email address
  - `mobile_no` (optional): Mobile number
  - `company_name` (optional): Company name
  - `source` (optional): Lead source
- **Returns**: Draft lead document
- **Roles**: Sales User, Sales Manager, System Manager

### 3. **convert_lead_to_customer**
- **Category**: APPROVE
- **Risk**: Medium
- **Confirmation**: Yes
- **Description**: Convert a lead to customer
- **Parameters**:
  - `lead` (required): Lead ID to convert
- **Returns**: Created customer details
- **Roles**: Sales Manager, System Manager

### 4. **get_lead_conversion_rate**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Calculate lead conversion statistics and rates
- **Parameters**:
  - `from_date` (optional): Period start
  - `to_date` (optional): Period end
- **Returns**: Conversion rate, status breakdown
- **Roles**: Sales User, Sales Manager, System Manager

### 5. **view_opportunities**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View opportunities with weighted value calculations
- **Parameters**:
  - `from_date` (optional): Filter from date
  - `to_date` (optional): Filter to date
  - `status` (optional): Opportunity status
  - `opportunity_type` (optional): Type filter
- **Returns**: Opportunities with analytics
- **Roles**: Sales User, Sales Manager, System Manager

### 6. **create_opportunity_draft**
- **Category**: DRAFT
- **Risk**: Low
- **Description**: Create a draft opportunity
- **Parameters**:
  - `opportunity_from` (required): Lead/Customer
  - `party_name` (required): Party name
  - `opportunity_type` (optional): Sales/Maintenance
  - `opportunity_amount` (optional): Expected amount
  - `probability` (optional): Win probability %
  - `expected_closing` (optional): Expected close date
- **Returns**: Draft opportunity document
- **Roles**: Sales User, Sales Manager, System Manager

### 7. **get_opportunity_pipeline**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Analyze opportunity pipeline by stage
- **Parameters**:
  - `from_date` (optional): Period start
  - `to_date` (optional): Period end
- **Returns**: Pipeline stages with weighted values
- **Roles**: Sales Manager, System Manager

### 8. **get_customer_summary**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Get customer list with revenue analytics
- **Parameters**:
  - `customer_group` (optional): Filter by group
  - `territory` (optional): Filter by territory
  - `disabled` (optional): Include/exclude disabled
- **Returns**: Customers with total revenue and order count
- **Roles**: Sales User, Sales Manager, Accounts User, System Manager

---

## 💰 Selling Module (6 Actions)

### 1. **view_sales_orders**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View sales orders with delivery and billing status
- **Parameters**:
  - `from_date` (optional): Transaction date from
  - `to_date` (optional): Transaction date to
  - `status` (optional): Order status
  - `customer` (optional): Filter by customer
- **Returns**: Sales orders with status breakdown
- **Roles**: Sales User, Sales Manager, System Manager

### 2. **get_pending_sales_orders**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Get pending/outstanding sales orders not fully delivered or billed
- **Parameters**: None
- **Returns**: Pending orders, overdue count, outstanding amount
- **Roles**: Sales User, Sales Manager, System Manager

### 3. **get_quotations_summary**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View quotations with conversion rate tracking
- **Parameters**:
  - `from_date` (optional): Filter from date
  - `to_date` (optional): Filter to date
  - `status` (optional): Quotation status
- **Returns**: Quotations with conversion statistics
- **Roles**: Sales User, Sales Manager, System Manager

### 4. **get_sales_analytics**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Comprehensive sales analytics - top customers, item groups, trends
- **Parameters**:
  - `from_date` (optional): Analysis period start
  - `to_date` (optional): Analysis period end
- **Returns**: Top customers, sales by item group, monthly trends
- **Roles**: Sales Manager, System Manager

### 5. **create_sales_order_draft**
- **Category**: DRAFT
- **Risk**: Medium
- **Confirmation**: Yes
- **Description**: Create a draft sales order
- **Parameters**:
  - `customer` (required): Customer name
  - `transaction_date` (optional): Order date
  - `delivery_date` (optional): Delivery date
  - `items` (required): Array of items with item_code, qty, rate
- **Returns**: Draft sales order document
- **Roles**: Sales User, Sales Manager, System Manager

### 6. **create_quotation_draft**
- **Category**: DRAFT
- **Risk**: Low
- **Description**: Create a draft quotation
- **Parameters**:
  - `quotation_to` (required): Customer/Lead
  - `party_name` (required): Party name
  - `transaction_date` (optional): Quote date
  - `valid_till` (optional): Validity date
  - `items` (required): Array of items
- **Returns**: Draft quotation document
- **Roles**: Sales User, Sales Manager, System Manager

---

## 🛒 Buying Module (5 Actions)

### 1. **view_purchase_orders**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View purchase orders with receipt and billing status
- **Parameters**:
  - `from_date` (optional): Transaction date from
  - `to_date` (optional): Transaction date to
  - `status` (optional): Order status
  - `supplier` (optional): Filter by supplier
- **Returns**: Purchase orders with status breakdown
- **Roles**: Purchase User, Purchase Manager, System Manager

### 2. **get_pending_purchase_orders**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Get pending purchase orders not fully received or billed
- **Parameters**: None
- **Returns**: Pending POs, overdue count, outstanding amount
- **Roles**: Purchase User, Purchase Manager, System Manager

### 3. **get_supplier_quotations**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View supplier quotations for comparison
- **Parameters**:
  - `from_date` (optional): Filter from date
  - `to_date` (optional): Filter to date
  - `status` (optional): Quotation status
- **Returns**: Supplier quotations list
- **Roles**: Purchase User, Purchase Manager, System Manager

### 4. **get_supplier_performance**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Analyze supplier performance - on-time delivery, quality
- **Parameters**:
  - `supplier` (optional): Specific supplier
  - `from_date` (optional): Period start
  - `to_date` (optional): Period end
- **Returns**: Supplier metrics and ratings
- **Roles**: Purchase Manager, System Manager

### 5. **create_purchase_order_draft**
- **Category**: DRAFT
- **Risk**: Medium
- **Confirmation**: Yes
- **Description**: Create a draft purchase order
- **Parameters**:
  - `supplier` (required): Supplier name
  - `transaction_date` (optional): PO date
  - `schedule_date` (optional): Expected delivery
  - `items` (required): Array of items
- **Returns**: Draft purchase order document
- **Roles**: Purchase User, Purchase Manager, System Manager

---

## 📦 Stock Module (6 Actions)

### 1. **view_stock_summary**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View stock levels with valuation across warehouses
- **Parameters**:
  - `item_code` (optional): Specific item
  - `warehouse` (optional): Specific warehouse
  - `item_group` (optional): Filter by group
- **Returns**: Stock balances with projected qty and value
- **Roles**: Stock User, Stock Manager, System Manager

### 2. **get_stock_ledger**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View stock ledger entries (movements)
- **Parameters**:
  - `item_code` (optional): Filter by item
  - `warehouse` (optional): Filter by warehouse
  - `from_date` (optional): Period start
  - `to_date` (optional): Period end
- **Returns**: Stock movements with balances
- **Roles**: Stock User, Stock Manager, Accounts User, System Manager

### 3. **get_low_stock_items**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Identify items below reorder level
- **Parameters**:
  - `warehouse` (optional): Specific warehouse
  - `item_group` (optional): Filter by group
- **Returns**: Items requiring reorder
- **Roles**: Stock User, Stock Manager, Purchase User, System Manager

### 4. **get_stock_ageing**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Analyze slow-moving and aging stock
- **Parameters**:
  - `warehouse` (optional): Specific warehouse
  - `item_group` (optional): Filter by group
- **Returns**: Stock age analysis
- **Roles**: Stock Manager, Accounts Manager, System Manager

### 5. **get_batch_wise_stock**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View stock by batch with expiry tracking
- **Parameters**:
  - `item_code` (optional): Specific item
  - `warehouse` (optional): Specific warehouse
- **Returns**: Batch-wise stock with expiry dates
- **Roles**: Stock User, Stock Manager, System Manager

### 6. **create_stock_entry_draft**
- **Category**: DRAFT
- **Risk**: Medium
- **Confirmation**: Yes
- **Description**: Create draft stock entry for material transfer/receipt/issue
- **Parameters**:
  - `stock_entry_type` (required): Material Transfer/Receipt/Issue
  - `from_warehouse` (optional): Source warehouse
  - `to_warehouse` (optional): Target warehouse
  - `items` (required): Items to transfer
- **Returns**: Draft stock entry document
- **Roles**: Stock User, Stock Manager, System Manager

---

## 💵 Accounting Module (8 Actions)

### 1. **view_account_balances**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View account balances from general ledger
- **Parameters**:
  - `account` (optional): Specific account
  - `account_type` (optional): Filter by type
  - `root_type` (optional): Asset/Liability/Income/Expense
- **Returns**: Account balances
- **Roles**: Accounts User, Accounts Manager, System Manager

### 2. **get_trial_balance**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Generate trial balance report
- **Parameters**:
  - `company` (optional): Specific company
  - `from_date` (optional): Period start
  - `to_date` (optional): Period end
- **Returns**: Trial balance with debit/credit totals
- **Roles**: Accounts User, Accounts Manager, System Manager

### 3. **get_profit_and_loss**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Generate P&L statement
- **Parameters**:
  - `company` (optional): Specific company
  - `from_date` (required): Period start
  - `to_date` (required): Period end
- **Returns**: Income and expense breakdown with net profit/loss
- **Roles**: Accounts Manager, System Manager

### 4. **get_balance_sheet**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Generate balance sheet
- **Parameters**:
  - `company` (optional): Specific company
  - `as_on_date` (required): Balance sheet date
- **Returns**: Assets, liabilities, equity
- **Roles**: Accounts Manager, System Manager

### 5. **get_accounts_receivable**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View outstanding receivables by customer
- **Parameters**:
  - `customer` (optional): Specific customer
  - `ageing_based_on` (optional): Due date/posting date
- **Returns**: Outstanding invoices with aging
- **Roles**: Accounts User, Accounts Manager, System Manager

### 6. **get_accounts_payable**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View outstanding payables by supplier
- **Parameters**:
  - `supplier` (optional): Specific supplier
  - `ageing_based_on` (optional): Due date/posting date
- **Returns**: Outstanding bills with aging
- **Roles**: Accounts User, Accounts Manager, System Manager

### 7. **create_journal_entry_draft**
- **Category**: DRAFT
- **Risk**: High
- **Confirmation**: Yes
- **Description**: Create draft journal entry for manual accounting
- **Parameters**:
  - `posting_date` (optional): Entry date
  - `voucher_type` (optional): JE type
  - `accounts` (required): Array of account entries with debit/credit
  - `user_remark` (optional): Entry description
- **Returns**: Draft journal entry document
- **Roles**: Accounts User, Accounts Manager, System Manager

### 8. **create_payment_entry_draft**
- **Category**: DRAFT
- **Risk**: High
- **Confirmation**: Yes
- **Description**: Create draft payment entry
- **Parameters**:
  - `payment_type` (required): Receive/Pay
  - `party_type` (required): Customer/Supplier
  - `party` (required): Party name
  - `paid_amount` (required): Amount
  - `mode_of_payment` (optional): Cash/Bank/etc
- **Returns**: Draft payment entry document
- **Roles**: Accounts User, Accounts Manager, System Manager

---

## 👥 HR Module (7 Actions)

### 1. **view_employee_list**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View employee directory
- **Parameters**:
  - `status` (optional): Active/Left
  - `department` (optional): Filter by department
  - `designation` (optional): Filter by designation
- **Returns**: Employee list with details
- **Roles**: HR User, HR Manager, System Manager

### 2. **get_attendance_summary**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View attendance summary
- **Parameters**:
  - `employee` (optional): Specific employee
  - `from_date` (optional): Period start
  - `to_date` (optional): Period end
- **Returns**: Attendance records with present/absent statistics
- **Roles**: HR User, HR Manager, System Manager

### 3. **get_leave_applications**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View leave applications
- **Parameters**:
  - `status` (optional): Open/Approved/Rejected
  - `employee` (optional): Specific employee
  - `from_date` (optional): Period start
  - `to_date` (optional): Period end
- **Returns**: Leave applications list
- **Roles**: HR User, HR Manager, System Manager

### 4. **get_leave_balance**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Check leave balance for employees
- **Parameters**:
  - `employee` (optional): Specific employee
  - `leave_type` (optional): Specific leave type
- **Returns**: Leave balances by type
- **Roles**: HR User, HR Manager, Employee (own balance), System Manager

### 5. **approve_leave_application**
- **Category**: APPROVE
- **Risk**: Medium
- **Confirmation**: Yes
- **Description**: Approve a leave application
- **Parameters**:
  - `leave_application` (required): Leave application ID
- **Returns**: Approval confirmation
- **Roles**: HR Manager, Leave Approver, System Manager

### 6. **get_employee_performance**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View employee performance appraisals
- **Parameters**:
  - `employee` (optional): Specific employee
  - `from_date` (optional): Period start
  - `to_date` (optional): Period end
- **Returns**: Appraisal records and ratings
- **Roles**: HR Manager, System Manager

### 7. **create_employee_draft**
- **Category**: DRAFT
- **Risk**: Medium
- **Confirmation**: Yes
- **Description**: Create draft employee record
- **Parameters**:
  - `first_name` (required): First name
  - `last_name` (optional): Last name
  - `date_of_joining` (required): Joining date
  - `department` (required): Department
  - `designation` (required): Designation
  - `company` (required): Company
- **Returns**: Draft employee document
- **Roles**: HR Manager, System Manager

---

## 💸 Payroll Module (3 Actions)

### 1. **view_salary_slips**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View salary slips
- **Parameters**:
  - `employee` (optional): Specific employee
  - `from_date` (optional): Period start
  - `to_date` (optional): Period end
- **Returns**: Salary slips with earnings and deductions
- **Roles**: HR Manager, Accounts Manager, System Manager

### 2. **get_payroll_summary**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Get payroll summary for a period
- **Parameters**:
  - `month` (required): Payroll month
  - `year` (required): Payroll year
- **Returns**: Total payroll cost, employee count, department breakdown
- **Roles**: HR Manager, Accounts Manager, System Manager

### 3. **execute_payroll**
- **Category**: EXECUTE_PAYROLL
- **Risk**: Critical
- **Confirmation**: Yes
- **Description**: Execute payroll processing for a period
- **Parameters**:
  - `payroll_entry` (required): Payroll entry ID
- **Returns**: Payroll execution confirmation with employee count
- **Roles**: HR Manager, System Manager

---

## 📁 Projects Module (5 Actions)

### 1. **view_projects_summary**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View projects with completion tracking
- **Parameters**:
  - `status` (optional): Project status
  - `project_type` (optional): Internal/External
- **Returns**: Projects with cost, billing, completion %
- **Roles**: Projects User, Projects Manager, System Manager

### 2. **view_tasks_summary**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View tasks across projects
- **Parameters**:
  - `project` (optional): Specific project
  - `status` (optional): Task status
  - `assigned_to` (optional): Assigned user
- **Returns**: Task list with progress
- **Roles**: Projects User, Projects Manager, System Manager

### 3. **get_project_profitability**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Analyze project profitability
- **Parameters**:
  - `project` (optional): Specific project
- **Returns**: Cost vs billing analysis, profit margins
- **Roles**: Projects Manager, Accounts Manager, System Manager

### 4. **get_timesheet_summary**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View timesheets and hours logged
- **Parameters**:
  - `project` (optional): Specific project
  - `employee` (optional): Specific employee
  - `from_date` (optional): Period start
  - `to_date` (optional): Period end
- **Returns**: Timesheet entries with billable/non-billable hours
- **Roles**: Projects User, Projects Manager, System Manager

### 5. **create_task_draft**
- **Category**: DRAFT
- **Risk**: Low
- **Description**: Create a draft task
- **Parameters**:
  - `subject` (required): Task title
  - `project` (optional): Link to project
  - `priority` (optional): Low/Medium/High
  - `expected_time` (optional): Expected hours
  - `description` (optional): Task description
- **Returns**: Draft task document
- **Roles**: Projects User, Projects Manager, System Manager

---

## 🏭 Manufacturing Module (5 Actions)

### 1. **view_work_orders**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View work orders with production status
- **Parameters**:
  - `status` (optional): WO status
  - `production_item` (optional): Item being produced
  - `from_date` (optional): Planned start date from
- **Returns**: Work orders with produced vs planned qty
- **Roles**: Manufacturing User, Manufacturing Manager, System Manager

### 2. **view_bom_summary**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View Bill of Materials
- **Parameters**:
  - `item` (optional): Finished good item
  - `is_active` (optional): Active BOMs only
  - `is_default` (optional): Default BOMs only
- **Returns**: BOM list with costs
- **Roles**: Manufacturing User, Manufacturing Manager, System Manager

### 3. **get_production_plan**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View production planning
- **Parameters**:
  - `status` (optional): Plan status
  - `from_date` (optional): Period start
  - `to_date` (optional): Period end
- **Returns**: Production plans with material requirements
- **Roles**: Manufacturing Manager, System Manager

### 4. **get_job_card_status**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View job card status for work orders
- **Parameters**:
  - `work_order` (optional): Specific work order
  - `status` (optional): Job card status
- **Returns**: Job cards with operation status
- **Roles**: Manufacturing User, Manufacturing Manager, System Manager

### 5. **create_work_order_draft**
- **Category**: DRAFT
- **Risk**: Medium
- **Confirmation**: Yes
- **Description**: Create draft work order
- **Parameters**:
  - `production_item` (required): Item to produce
  - `qty` (required): Quantity
  - `bom_no` (optional): BOM to use
  - `planned_start_date` (optional): Start date
- **Returns**: Draft work order document
- **Roles**: Manufacturing User, Manufacturing Manager, System Manager

---

## 🎧 Support Module (4 Actions)

### 1. **view_issues_summary**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View support issues with priority tracking
- **Parameters**:
  - `status` (optional): Issue status
  - `priority` (optional): Low/Medium/High
  - `customer` (optional): Filter by customer
- **Returns**: Issues with status and priority breakdown
- **Roles**: Support Team, System Manager

### 2. **view_service_level_summary**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View SLA compliance metrics
- **Parameters**: None
- **Returns**: SLA compliance by priority, average resolution time
- **Roles**: Support Team, System Manager

### 3. **get_issue_analytics**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Analyze issue trends and patterns
- **Parameters**:
  - `from_date` (optional): Period start
  - `to_date` (optional): Period end
- **Returns**: Issue trends, top issues, resolution metrics
- **Roles**: Support Team Manager, System Manager

### 4. **create_issue_draft**
- **Category**: DRAFT
- **Risk**: Low
- **Description**: Create a draft support issue
- **Parameters**:
  - `subject` (required): Issue subject
  - `customer` (optional): Related customer
  - `priority` (optional): Issue priority
  - `issue_type` (optional): Issue category
  - `description` (optional): Detailed description
- **Returns**: Draft issue document
- **Roles**: Support Team, System Manager

---

## 🏢 Assets Module (4 Actions)

### 1. **view_assets_summary**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View company assets with depreciation
- **Parameters**:
  - `asset_category` (optional): Filter by category
  - `status` (optional): Asset status
  - `location` (optional): Physical location
- **Returns**: Assets with value and status breakdown
- **Roles**: Stock User, Accounts User, System Manager

### 2. **view_asset_maintenance_schedule**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View asset maintenance schedule
- **Parameters**:
  - `asset` (optional): Specific asset
- **Returns**: Upcoming maintenance tasks
- **Roles**: Stock User, Accounts User, System Manager

### 3. **get_asset_depreciation**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View asset depreciation schedule and entries
- **Parameters**:
  - `asset` (optional): Specific asset
  - `from_date` (optional): Period start
  - `to_date` (optional): Period end
- **Returns**: Depreciation entries and schedules
- **Roles**: Accounts User, Accounts Manager, System Manager

### 4. **create_asset_draft**
- **Category**: DRAFT
- **Risk**: Medium
- **Confirmation**: Yes
- **Description**: Create draft asset record
- **Parameters**:
  - `asset_name` (required): Asset name
  - `asset_category` (required): Category
  - `gross_purchase_amount` (required): Purchase cost
  - `purchase_date` (required): Purchase date
  - `available_for_use_date` (optional): In-service date
- **Returns**: Draft asset document
- **Roles**: Accounts User, Accounts Manager, System Manager

---

## ✅ Quality Module (4 Actions)

### 1. **view_quality_inspections**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View quality inspection records
- **Parameters**:
  - `status` (optional): Accepted/Rejected
  - `inspection_type` (optional): Incoming/Outgoing/In Process
  - `item_code` (optional): Specific item
- **Returns**: Inspection records with status breakdown
- **Roles**: Quality Manager, Stock User, System Manager

### 2. **view_quality_goals**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View quality management goals
- **Parameters**: None
- **Returns**: Quality goals and targets
- **Roles**: Quality Manager, System Manager

### 3. **get_quality_metrics**
- **Category**: QUERY
- **Risk**: Low
- **Description**: Analyze quality performance metrics
- **Parameters**:
  - `from_date` (optional): Period start
  - `to_date` (optional): Period end
- **Returns**: Rejection rates, inspection statistics
- **Roles**: Quality Manager, System Manager

### 4. **create_quality_inspection_draft**
- **Category**: DRAFT
- **Risk**: Low
- **Description**: Create draft quality inspection
- **Parameters**:
  - `inspection_type` (required): Type
  - `item_code` (required): Item
  - `sample_size` (optional): Sample size
  - `reference_type` (optional): Purchase Receipt/Delivery Note
  - `reference_name` (optional): Reference document
- **Returns**: Draft quality inspection document
- **Roles**: Quality Manager, Stock User, System Manager

---

## 🔧 Maintenance Module (3 Actions)

### 1. **view_maintenance_schedule**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View maintenance schedules
- **Parameters**:
  - `customer` (optional): Filter by customer
- **Returns**: Maintenance schedules list
- **Roles**: Sales User, System Manager

### 2. **view_maintenance_visits**
- **Category**: QUERY
- **Risk**: Low
- **Description**: View maintenance visit records
- **Parameters**:
  - `status` (optional): Completion status
  - `customer` (optional): Filter by customer
- **Returns**: Maintenance visits with status
- **Roles**: Sales User, System Manager

### 3. **create_maintenance_visit_draft**
- **Category**: DRAFT
- **Risk**: Low
- **Description**: Create draft maintenance visit
- **Parameters**:
  - `customer` (required): Customer
  - `mntc_date` (optional): Visit date
  - `maintenance_type` (optional): Type
  - `purposes` (optional): Array of purposes
- **Returns**: Draft maintenance visit document
- **Roles**: Sales User, System Manager

---

## 📊 Summary Statistics

- **Total Actions**: 50+
- **Total Modules**: 12
- **QUERY Actions**: 38 (Read-only operations)
- **DRAFT Actions**: 10 (Create draft documents)
- **APPROVE Actions**: 2 (Workflow approvals)
- **POST Actions**: 0 (Financial submissions - can be added)
- **EXECUTE_PAYROLL**: 1 (Critical payroll execution)

## 🔒 Security Levels

- **Low Risk**: 38 actions (Read operations, draft creation)
- **Medium Risk**: 10 actions (Document creation, approvals)
- **High Risk**: 2 actions (Financial entries)
- **Critical Risk**: 1 action (Payroll execution)

## 👥 Role Coverage

All actions respect ERPNext's role-based permission system:
- System Manager: Full access to all actions
- Module Managers: Full access within their module
- Module Users: Read and draft access within their module
- Specialized roles: Access to specific actions (e.g., Quality Manager for quality actions)

---

**Note**: This is the comprehensive list of built-in actions. You can easily add more actions by:
1. Creating handler functions in the appropriate module file
2. Registering them in ApexAiAssistant Action Registry
3. Assigning appropriate roles and permissions
