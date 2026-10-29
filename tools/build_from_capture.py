# Reference only: turned the raw demo-site capture (not included in this repo) into src/screens.json.
# Day-to-day edits go in src/screens.json; rebuild with ../build.py.
import json, re, html
from parse import parse_guide, parse_form

M = json.load(open('data/masters.json'))
R = {r['h']: r for r in json.load(open('data/routes.json'))}
E = json.load(open('data/extra.json'))
S, X = E['S'], E['X']

MENU = "☰ Menu"
MORE = "⋮ More > Settings"

screens = []


def add(id, group, title, icon, path, guide_text=None, form=None, img=None, route=None,
        extra=None, summary=None, can=None, rules=None, tips=None, watch=None, next=None, concepts=None, tabs=None):
    g = parse_guide(guide_text or '')
    s = {
        'id': id, 'group': group, 'title': title, 'icon': icon, 'path': path, 'route': route or '',
        'summary': summary or g.get('summary', ''), 'next': next or g.get('next', ''),
        'can': can or g.get('can', []), 'concepts': concepts or g.get('concepts', []),
        'rules': rules or g.get('rules', []), 'tips': tips or g.get('tips', []), 'watch': watch or g.get('watch', []),
        'fields': parse_form(form) if form else [], 'img': img or '', 'tabs': tabs or [], 'extra': extra or [],
    }
    screens.append(s)


# ---------------- Getting started ----------------
G0 = 'Getting started'
add('login', G0, 'Logging in', 'login', 'Company URL > Login page', img='login',
    summary='Sign in with your Employee Id and Password. Use Forgot Password? to reset a password, and New User? Click here to register where self-registration is enabled.',
    can=['Enter Employee Id and Password, then click LOGIN',
         'Tick Remember Me on a personal device only',
         'Reset a forgotten password with Forgot Password?',
         'Self-register as a new user, where the company allows it'],
    rules=['Employee Id and Password are both mandatory', 'Your landing page and menus depend on the role assigned to your login'])
add('welcome', G0, 'Welcome page and Quick Links', 'home', f'{MENU} > Dashboard', R['#/dashboard']['guide'], img='welcome')
add('layout', G0, 'Screen layout and navigation', 'dashboard_customize', 'Every screen', img='sidemenu',
    summary='The side menu (☰) holds every module. The top bar has search, Web Login, the approvals bell, the More (⋮) menu and your profile. Most screens have a ? icon that opens a Guide panel with rules and tips.',
    can=['Side menu: My Profile, Dashboard, Approvals, My Applications, HR, Tax, Help Desk, Log Time, Employee Assets, Uploads, Company Policy, Performance and Growth, Reports, Gifts & Rewards, 247 HRM Support',
         'Search (magnifier): find employees, pages or quick links (Ctrl K on desktop)',
         'Web Login icon (running man): punch in / punch out from the browser',
         'Bell: pending approvals with a count for each approval type',
         'More (⋮): Old Application, Go Social and Settings (Ticketing, Roles, IP Security, Company Settings, MFA, Approval Configuration, Notification, Masters)',
         'Guide panel (?): what the screen does, the next step, key concepts, validation rules and common mistakes',
         'Chat assistant (bottom right): HR Mate bot for leave requests, leave balance, payslips, holidays and attendance'],
    tips=['Every master list supports Search, Reset, column filters, Show/Hide Columns, paging, Edit and Delete (with a confirmation prompt)',
          'Fields marked * are mandatory; system-generated IDs are read-only',
          'If a menu or Quick Link is missing for a user, check the role permissions in Settings > Roles'])
add('bell', G0, 'Pending approvals (bell)', 'notifications', 'Top bar > Bell icon', img='approvals-bell',
    summary='The bell shows the total pending approvals and a count for each type, so approvers can jump straight to what is waiting.',
    can=['See counts for Tax saving details, Leaves/Incidents and C-off, New Joinees, Employee Updates, HR approval, Resignation status change, Local Claims, Leave Encashment and Final Settlement',
         'Click a type to open its approval list'])

# ---------------- Setup sequence (consultant) ----------------
G1 = 'Implementation setup'
add('setup', G1, 'Recommended setup sequence', 'checklist', 'Implementation checklist',
    summary='Configure in this order: each step feeds dropdowns and calculations in the next. Skipping ahead is the most common cause of missing dropdown values and wrong first payrolls.',
    can=['1. Company Settings, Roles, IP Security, MFA — who can log in and what each role sees',
         '2. Organization masters: Location → Department → Section → Designation → Grade → Employment Type → Cost Center → Bank Master → Finance Company → Custom Fields',
         '3. Statutory: PF Master, ESI Master, Professional Tax (one row per state) and Income Tax Setup for the financial year',
         '4. Attendance: Pay Period → Shift Definition → Shift Patterns → Late Early → Over Time Rules → Incident → Leave Type → Dynamic WeekOff; then Holiday Management per state/location',
         '5. Salary: Allowances → Deductions → Loans → Advances → Notice Period; Local Claim and Company Welfare masters if used',
         '6. Workflow: Approval Configuration, Manage Ticketing Details, Notification settings',
         '7. Employee data: Employee Master or Uploads (Existing Employees, Leave Opening Balance, Bank/Loans, TDS)',
         '8. Monthly cycle: attendance and leave uploads → Payroll (Trial → Final, lock) → Payslips publish → statutory reports (PF ECR, ESI, PT) and Bank Transfer'],
    rules=['Departments must exist before Sections (a Section cannot be saved without its parent Department)',
           'Set the Location Employee Prefix and Auto INC before creating employees, so employee IDs generate automatically',
           'Shift list on the employee form depends on Location; Section list depends on Department',
           'Pay Period must be selected before any payroll summary loads',
           'Payslips must be published before employees can see them in self-service'],
    tips=['Run a Trial Payroll and reconcile it against the client’s last manual payroll before the first Final run',
          'Confirm PF/ESI/PT applicability location by location before go-live; it is the most common source of statutory defects',
          'Keep master names short and standardised; they appear in every report'])

# ---------------- Settings ----------------
G2 = 'Settings'
sett = [('Company Settings', 'business', 's-company', 'company'), ('Roles', 'settings_accessibility', 's-roles', 'roles'),
        ('IP Security', 'security', 's-ip', 'ipsec'), ('MFA Settings', 'shield_lock', 's-mfa', 'mfa'),
        ('Approval Configuration', 'approval', 's-approvalcfg', 'approvalcfg'), ('Notification', 'notifications_active', 's-notif', 'notif'),
        ('Manage Ticketing Details', 'admin_panel_settings', 's-ticket', 'ticketing')]
for name, icon, img, sid in sett:
    v = S[name]
    kw = {}
    if name == 'Approval Configuration':
        kw = dict(summary='Sets the approval SLA for Leaves, Incidents and C-off requests: whether approvals are bound to the pay period, how many days an employee has to raise a request, and how many days approvers have to act.',
                  can=['Choose whether the PayPeriod cut-off applies (Yes/No)', 'Set SLA Request Days (how long after the date an employee can raise a request)',
                       'Set SLA Days (how long approvers have to act)', 'Click Submit to save'],
                  rules=['PayPeriod, SLA Request Days and SLA Days are mandatory'])
    tabs = {'Roles': ['Roles', 'Assign Roles', 'Role Transfer', 'Default Permissions'],
            'IP Security': ['IP Restriction Feature', 'IP Restrictions'],
            'Company Settings': ['Attendance', 'TimeSheets', 'Prospective Employee', 'General Settings', 'Swipe / embedded settings'],
            'Notification': ['Attendance', 'TimeSheets', 'Help Desk', 'Income Tax'],
            'Manage Ticketing Details': ['1. Category Master', '2. Authority Assign', '3. Authority Grid']}.get(name, [])
    add(sid, G2, name, icon, f'{MORE} > {name}', v.get('guide'), img=img, route=v.get('hash'), tabs=tabs, **kw)

# ---------------- Masters ----------------
cat_name = {'organization': 'Organization', 'attendance': 'Attendance', 'salary': 'Salary', 'statutory': 'Statutory',
            'incomeTaxSetup': 'Income Tax Setup', 'others': 'Others'}
cats = ['organization'] * 10 + ['attendance'] * 8 + ['salary'] * 5 + ['statutory'] * 3 + ['incomeTaxSetup'] + ['others'] * 7
micons = ['badge', 'military_tech', 'location_city', 'account_tree', 'workspaces', 'work_outline', 'account_balance', 'dynamic_form', 'pie_chart', 'corporate_fare',
          'calendar_month', 'beach_access', 'report_problem', 'alarm_on', 'more_time', 'view_week', 'credit_card', 'rule',
          'attach_money', 'money_off', 'account_balance_wallet', 'paid', 'hourglass_bottom',
          'savings', 'health_and_safety', 'receipt_long', 'request_quote',
          'currency_exchange', 'engineering', 'assignment_turned_in', 'list_alt', 'event_repeat', 'request_page', 'volunteer_activism']
add('masters-home', 'Masters', 'Masters overview', 'apps', f'{MORE} > Masters', img='masters-home',
    summary='Masters hold the reference data used across the application: 34 masters in six groups (Organization, Attendance, Salary, Statutory, Income Tax Setup, Others). Use the left list or the module search to jump between them.',
    can=['Organization (10): Employment Type, Grade, Location, Department, Section, Designation, Bank Master, Custom Fields, Cost Center, Finance Company Master',
         'Attendance (8): Payperiod Master, Leave Type, Incident Master, Late Early Master, Shift Definition, Shift Patterns, Unassigned Card, Over Time Rules',
         'Salary (5): Allowances, Deductions, Loans, Advances, Notice Period',
         'Statutory (3): PF Master, ESI Master, Professional Tax',
         'Income Tax Setup (1): tax periods, mapping, tax rules and info text',
         'Others (7): Currency, Work Order, Contract, Key List Item, Dynamic WeekOff, Local Claim Master, Company Welfare Master'],
    rules=['Required fields must be completed before saving', 'Record IDs are system-generated and read-only', 'Delete asks for confirmation; a master already used by employees should be edited, not deleted'])
for r in M:
    i = r['i']
    cat = cat_name[cats[i]]
    name = r['name']
    img = f'm{i}' if i != 32 else ''
    add(f'master-{i}', f'Masters — {cat}', name if 'Master' in name or name in ('Income Tax Setup',) else name,
        micons[i], f'{MORE} > Masters > {cat} > {name}', r.get('guide'), form=r.get('form'), img=img, route=r.get('hash'),
        extra=[['List columns', re.sub(r'^.*?refresh', '', (r.get('cols') or '')).replace(', action', '').strip()]] if r.get('cols') else [])

# ---------------- HR ----------------
G4 = 'HR operations'
hr = [('#/EmployeeMaster', 'Employee Master (directory)', 'groups', 'HR > Employee Master', 'r-empmaster'),
      ('addEmp', 'Add / edit an employee', 'person_add', 'HR > Employee Master > + Add Employee', ''),
      ('#/prospective-employee', 'Prospective Employee', 'person_add', 'HR > Prospective Employee', 'r-prospective'),
      ('#/payroll', 'Payroll', 'calculate', 'HR > Payroll', 'r-payroll'),
      ('#/payslip', 'Payslips (publishing)', 'receipt', 'HR > Payslips', 'r-payslip'),
      ('#/lettergeneration', 'Letter Generation', 'drafts', 'HR > Letter Generation', 'r-letters'),
      ('#/holiday-management', 'Holiday Management', 'beach_access', 'HR > Holiday Management', 'r-holiday'),
      ('#/HRLoansAdvances/advances', 'Advances Management', 'payments', 'HR > Advances Management', 'r-hradv'),
      ('#/HRLoansAdvances/loans', 'Loans Management', 'account_balance', 'HR > Loans Management', 'r-hrloan'),
      ('#/employeeId-card', 'Employee ID Card', 'badge', 'HR > Employee ID Card', 'r-idcard'),
      ('#/Leave-EncashmentHr', 'Leave Encashment by HR', 'paid', 'HR > Leave Encashment by HR', 'r-leaveenchr'),
      ('#/Arrears-Calculation', 'Arrears Calculation', 'functions', 'HR > Arrears Calculation', 'r-arrears'),
      ('#/final-settlement', 'Final Settlement (F&F)', 'done_all', 'HR > Final Settlement', 'r-fnf'),
      ('#/bonus-calculation', 'Bonus Calculation', 'emoji_events', 'HR > Bonus Calculation', 'r-bonus'),
      ('#/exgratia-calculation', 'Exgratia Calculation', 'redeem', 'HR > Exgratia Calculation', 'r-exgratia'),
      ('#/stopSalary', 'Stop Salary', 'block', 'HR > Stop Salary', 'r-stopsal'),
      ('#/delete-document', 'Delete Document', 'delete_forever', 'HR > Delete Document', 'r-deldoc'),
      ('#/incometaxsubheaders/emi', 'Income Tax EMI', 'schedule', 'Tax > EMI', 'r-emi'),
      ('#/uploads', 'Uploads (bulk data)', 'cloud_upload', 'Uploads', 'r-uploads'),
      ('#/applications/helpdesk', 'Help Desk', 'live_help', 'Help Desk', 'r-helpdesk'),
      ('#/applications/project-management', 'Log Time (timesheets)', 'settings_input_composite', 'Log Time', 'r-logtime'),
      ('#/employeeassets', 'Employee Assets', 'computer', 'Employee Assets', 'r-assets'),
      ('#/companypolicy', 'Company Policy', 'bookmarks', 'Company Policy', 'r-policy')]
for key, title, icon, path, img in hr:
    src = X['addEmp'] if key == 'addEmp' else R[key]
    kw = {}
    tabs = [t.split('\n')[-1] for t in src.get('tabs', [])] if isinstance(src.get('tabs'), list) else []
    if key == '#/employeeId-card':
        kw = dict(summary='Lists every employee with ID, employment type, location, department, designation, grade and status, and lets HR view or download each employee’s ID card.',
                  can=['Search for an employee', 'Click the eye icon to preview the ID card', 'Click the download icon to download it', 'Export the list with the export icon'])
    extra = []
    if key == 'addEmp':
        extra = [['Sections of the form', 'Basic Detail (Employee ID, Title*, First Name*, Middle/Last Name, Gender, Date of Birth, Official Email Id*, Aadhaar No + file) • Employment Details (Company Name*, Date of Join*, Employment Type*, Grade*, Reporting To*, Enrollment ID, Department*, Designation*, Location*, Shift*, Section*) • Attendance & Weekly Off (Late*, Swipe Attendance*, Regularize Date*, Attendance*, Pay Period*, Work Order Number, Weekly Off*, Select Week*) • Statutory Applicability (PF + PF Number, ESI + ESI Number, PT, PAN Number + file, UAN Number, NPS, EPS, NPS Percentage, Portal Accessibility) • Salary Structure (Select Salary Structure*, Salary*, Month, Year) • Bank Details (Payment Mode: Cash / Cheque / Bank)'],
                 ['Dependencies', 'Shift list depends on the selected Location; Section list depends on the selected Department.']]
    if key == '#/uploads':
        extra = [['Upload types', 'Joinee Allowance Upload • Existing Employees Upload • Allowance Upload • Deductions Upload • Monthly Attendance • Incident Upload • Daily Attendance • Shift Allotment Upload • LOP Arrears Upload • Leaves Upload • Leave Opening Balance Upload • Backdated Leave Upload • Employee Documents • Loans Advance Upload • TDS Upload'],
                 ['How every upload works', '1. Pick the upload type and mode → 2. Download Template → 3. Fill it without changing columns (.xlsx only) → 4. Choose File to upload → 5. Review the tabs, fix errors → 6. Send valid rows for approval']]
    if key == '#/payroll':
        extra = [['Component cards', 'Gross • Payroll Processed • Yet to Payroll Process • Leaves • LOP • Attendance (Regularisation, On Tour) • Joinees • Resignees • Salary Changes / Zero Salaries • Allowances • Deductions • L & A • L & A Deductions • Overtime • Statutory • TDS • Budget • Stop Salaries'],
                 ['Monthly run', '1. Choose Month and Pay Period → 2. Filter employees → 3. Check Yet to Payroll Process and pending approvals → 4. Process attendance and LOP → 5. Trial Payroll and reconcile → 6. Final / Attendance & Payroll Process: calculate, lock, send for approval → 7. Publish payslips']]
    if key == '#/final-settlement':
        tabs = ['Pending Details', 'F&F Status History', 'Approved Details', 'Final Settlement Report']
    add('hr-' + re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-'), G4, title, icon, f'{MENU} > {path}', src.get('guide'), img=img,
        route=src.get('final') or src.get('hash'), tabs=tabs, extra=extra, **kw)

# ---------------- My Applications ----------------
G5 = 'My Applications (self-service)'
ess = [('#/SocialDashboard/profile', 'My Profile', 'person', 'My Profile', 'r-profile'),
       ('#/Approvals', 'Approvals', 'task_alt', 'Approvals', 'r-approvals'),
       ('#/applications/weblogin', 'Web Login (attendance punches)', 'login', 'My Applications > Web Login', 'r-weblogin'),
       ('#/leaves', 'Leave & Attendance', 'event_available', 'My Applications > Leave & Attendance', 'r-leaves'),
       ('#/applications/compensatoryRequest', 'Compensatory Off', 'work_history', 'My Applications > Compensatory Off', 'r-coff'),
       ('#/applications/incometax', 'Income Tax Saving (declaration)', 'savings', 'My Applications > Income Tax Saving', 'r-itax'),
       ('#/applications/employeepayslip', 'Employee Payslip', 'receipt_long', 'My Applications > Employee Payslip', 'r-emppayslip'),
       ('#/EmployeeResignation', 'Resignation', 'logout', 'My Applications > Resignation', 'r-resign'),
       ('#/EmployeeAdvances', 'Advances', 'account_balance_wallet', 'My Applications > Advances', 'r-empadv'),
       ('#/EmployeeLoans', 'Loans', 'request_quote', 'My Applications > Loans', 'r-emploan'),
       ('#/leave-encashment', 'Leave Encashment', 'paid', 'My Applications > Leave Encashment', 'r-leaveenc'),
       ('#/local-claim/employee-request', 'Local Claim', 'description', 'My Applications > Local Claim', 'r-localclaim')]
for key, title, icon, path, img in ess:
    src = R[key]
    kw = {}
    tabs = [t.split('\n')[-1] for t in src.get('tabs', [])]
    if key == '#/Approvals':
        kw = dict(summary='One place for approvers to see every pending request type with its count and open the list to approve or reject.',
                  can=['Tax saving details', 'Leaves, Incidents and C-off', 'New Joinees', 'Employee Updates', 'HR approval', 'Resignation status change', 'Local Claims', 'Leave Encashment Approvals', 'Final Settlement'],
                  tips=['Click View Approvals on a card to open that queue', 'The same counts appear under the bell icon in the top bar'])
    if key == '#/leaves':
        tabs = ['Attendance Calendar', 'Shift Summary', 'Leave Balances', 'C-Off History', 'Incident History', 'Leave Approvals', 'Incident Approvals', 'C-Off Approvals']
    add('ess-' + re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-'), G5, title, icon, f'{MENU} > {path}', src.get('guide'), img=img,
        route=src.get('final'), tabs=tabs, **kw)
add('ess-travel', G5, 'Travel Requisition', 'flight_takeoff', f'{MENU} > My Applications > Travel Requisition',
    summary='Opens the travel requisition screens of the older 247HRM application in a new page, where employees raise travel requests and track approvals.',
    can=['Raise a travel requisition', 'Track its approval status'], tips=['This screen lives in the Old Application, so its look differs from the rest of the product'])

# ---------------- Dashboards & reports ----------------
G6 = 'Dashboards & Reports'
for k, ic, img in [('CXO Dashboard', 'leaderboard', 'd-cxo'), ('HR Dashboard', 'supervisor_account', 'd-hr'),
                   ('Manager Dashboard', 'manage_accounts', 'd-mgr'), ('Attendance', 'schedule', 'd-att')]:
    v = X[k]
    add('dash-' + k.split()[0].lower(), G6, k if k != 'Attendance' else 'Attendance Dashboard', ic,
        f'Welcome page > Quick Links > {k}', v.get('guide'), img=img, route=v.get('hash'))
rep = R['#/report']['main']
cats_rep = {}
for m in re.finditer(r'(MIS|Payroll|Income Tax|Statutory|Analytics|Attendance) (\d+) reports\s+· [^\n]*?expand_more(.*?)(?=(?:insights|payments|receipt_long|gavel|analytics|how_to_reg)(?:MIS|Payroll|Income Tax|Statutory|Analytics|Attendance) \d+ reports|starFavourites)', rep, re.S):
    names = [n.strip() for n in re.split(r'(?:\s*edit)?\s*\n\s*star\s*\n?', m.group(3)) if n.strip()]
    names = [n.replace(' edit', '').strip() for n in names]
    names = [n for n in names if n and n not in ('asd', 'AMAN', 'ABC', 'Name', 'star')]
    cats_rep[m.group(1)] = sorted(set(names), key=names.index)
add('reports', G6, 'Reports', 'menu_book', f'{MENU} > Reports', R['#/report']['guide'], img='r-reports', route='#/report',
    extra=[[f'{c} reports ({len(v)})', ' • '.join(v)] for c, v in cats_rep.items()])
add('gifts', G6, 'Gifts & Rewards', 'card_giftcard', f'{MENU} > Gifts & Rewards',
    summary='Information page for 247HRM’s rewards add-on: corporate gifting, reward points allocation and white-labelled reward programmes.',
    can=['Corporate Gifting: gift cards and branded merchandise', 'Points Allocation: buy reward points and distribute them to employees', 'Reward Programs: white-labelled loyalty programmes'])
add('pms', G6, 'Performance and Growth', 'hub', f'{MENU} > Performance and Growth',
    summary='Opens the separate Performance & Growth application (single sign-on from 247HRM). It was not walked through for this manual.',
    can=['Goal Achiever', 'People Assessment', '360 Degree Review', 'Workforce Wellbeing', 'Workforce Engagement', 'Custom Survey', 'Strategic Networking', 'Learning & Development', 'Talent Analysis', 'Announcements', 'Action Plan', 'Smart Auth', 'Performance Management System'])


# ---------------- module + role tagging ----------------
MODULES = [
 ['core','Core HR','Employee master, organisation masters, documents, exits','employee data|employee master|core|core hr|hrms|employee management|application setup|employee|onboarding|exit'],
 ['payroll','Payroll','Salary, statutory (PF/ESI/PT), loans & advances, payslips','payroll|salary|statutory|pf|esi|loans|advances|loan'],
 ['itax','Income Tax','Tax setup, declarations, TDS/EMI','income tax|incometax|tds|tax|it declaration'],
 ['attendance','Attendance & Biometric','Shifts, punches, OT, late/early, incidents','attendance|biometric|time attendance|shift|punch|swipe'],
 ['leave','Leave','Leave types, comp-off, holidays, encashment','leave|leaves|holiday|comp off|compensatory'],
 ['letters','Letters','Letter templates and generation','letter|letters|letter generation'],
 ['helpdesk','Help Desk (Grievance)','Tickets, categories, routing','grievance|help desk|helpdesk|ticket|ticketing'],
 ['travel','Travel & Expenses','Local claims and travel requisitions','travel|expense|expenses|claim|claims|reimbursement|local claim'],
 ['asset','Asset Management','Asset groups, stores, allocation','asset|assets'],
 ['timesheet','Timesheet','Log time against projects','timesheet|time sheet|log time|project|projects'],
 ['ats','Recruitment / Pre-onboarding','Prospective employees and bulk invites','ats|recruitment|prospective|pre onboarding|pre-onboarding|hiring'],
 ['pms','Performance & Growth','PMS, 360, LMS, engagement','pms|performance|360|lms|learning|appraisal|goal|engagement'],
 ['rewards','Gifts & Rewards','Rewards and gifting add-on','gifts|rewards|social points|gifting'],
]
MOD_OF = {
 'login':'base','welcome':'base','layout':'base','bell':'base','setup':'base','company':'base','roles':'base','ipsec':'base','mfa':'base',
 'approvalcfg':'leave','notif':'base','ticketing':'helpdesk','masters-home':'base',
 'master-0':'core','master-1':'core','master-2':'core','master-3':'core','master-4':'core','master-5':'core','master-6':'payroll','master-7':'core',
 'master-8':'core','master-9':'payroll','master-10':'attendance','master-11':'leave','master-12':'attendance','master-13':'attendance','master-14':'attendance',
 'master-15':'attendance','master-16':'attendance','master-17':'attendance','master-18':'payroll','master-19':'payroll','master-20':'payroll','master-21':'payroll',
 'master-22':'core','master-23':'payroll','master-24':'payroll','master-25':'payroll','master-26':'itax','master-27':'base','master-28':'core','master-29':'core',
 'master-30':'base','master-31':'attendance','master-32':'travel','master-33':'payroll',
 'hr-employee-master-directory':'core','hr-add-edit-an-employee':'core','hr-prospective-employee':'ats','hr-payroll':'payroll','hr-payslips-publishing':'payroll',
 'hr-letter-generation':'letters','hr-holiday-management':'leave','hr-advances-management':'payroll','hr-loans-management':'payroll','hr-employee-id-card':'core',
 'hr-leave-encashment-by-hr':'leave','hr-arrears-calculation':'payroll','hr-final-settlement-f-f':'payroll','hr-bonus-calculation':'payroll','hr-exgratia-calculation':'payroll',
 'hr-stop-salary':'payroll','hr-delete-document':'core','hr-income-tax-emi':'itax','hr-uploads-bulk-data':'base','hr-help-desk':'helpdesk','hr-log-time-timesheets':'timesheet',
 'hr-employee-assets':'asset','hr-company-policy':'core',
 'ess-my-profile':'core','ess-approvals':'base','ess-web-login-attendance-punches':'attendance','ess-leave-attendance':'leave','ess-compensatory-off':'leave',
 'ess-income-tax-saving-declaration':'itax','ess-employee-payslip':'payroll','ess-resignation':'core','ess-advances':'payroll','ess-loans':'payroll',
 'ess-leave-encashment':'leave','ess-local-claim':'travel','ess-travel':'travel',
 'dash-cxo':'base','dash-hr':'attendance','dash-manager':'base','dash-attendance':'attendance','reports':'base','gifts':'rewards','pms':'pms'}
EMP = {'login','welcome','layout','ess-my-profile','ess-web-login-attendance-punches','ess-leave-attendance','ess-compensatory-off','ess-income-tax-saving-declaration',
       'ess-employee-payslip','ess-resignation','ess-advances','ess-loans','ess-leave-encashment','ess-local-claim','ess-travel','dash-attendance',
       'hr-help-desk','hr-log-time-timesheets','hr-company-policy','pms','gifts'}
MGR = EMP | {'bell','ess-approvals','dash-manager'}
for sc in screens:
    sc['mod'] = MOD_OF[sc['id']]
    r = ['hr']
    if sc['id'] in MGR: r.append('manager')
    if sc['id'] in EMP: r.append('employee')
    sc['roles'] = r
REPMOD = {'MIS':'core','Payroll':'payroll','Income Tax':'itax','Statutory':'payroll','Analytics':'core','Attendance':'attendance'}
for sc in screens:
    if sc['id'] == 'reports':
        sc['extra'] = [[t, v, REPMOD[t.split(' reports')[0]]] for t, v in sc['extra']]
missing = [k for k in MOD_OF if k not in {x['id'] for x in screens}]
assert not missing, missing

json.dump(screens, open('site/data.json', 'w'), ensure_ascii=False)
print(len(screens), 'screens')
for s in screens:
    if not (s['summary']):
        print('NO SUMMARY', s['id'])
print({k: len(v) for k, v in cats_rep.items()})

tpl = open('template.html').read()
meta = {'date': '30 Oct 2026', 'reports': sum(len(v) for v in cats_rep.values()), 'modules': MODULES, 'client': '', 'export': False}
out = tpl.replace('__DATA__', json.dumps(screens, ensure_ascii=False).replace('</', '<\\/')).replace('__META__', json.dumps(meta, ensure_ascii=False))
open('site/index.html', 'w').write(out)
print('index.html', len(out))
