from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Page margins ──────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin   = Inches(1.25)
    section.right_margin  = Inches(1.25)

# ── Base font ─────────────────────────────────────────────────
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)

# ── Helpers ───────────────────────────────────────────────────
def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def heading1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after  = Pt(6)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = 'Times New Roman'
    return p

def heading2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(4)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'
    return p

def body(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    return p

def bullet(label, rest=''):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(4)
    if label:
        r1 = p.add_run(label)
        r1.bold = True
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
    if rest:
        r2 = p.add_run(rest)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(12)

def plain_bullet(text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)

# ══════════════════════════════════════════════════════════════
# TITLE PAGE
# ══════════════════════════════════════════════════════════════
doc.add_paragraph('\n\n\n')
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('Project Proposal')
r.bold = True; r.font.size = Pt(24); r.font.name = 'Times New Roman'

doc.add_paragraph()
s = doc.add_paragraph()
s.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = s.add_run(
    'Mitigating "Lag-to-Churn": An AI-Driven Edge Defence Framework\n'
    'Against Layer 4 DDoS Attacks in the Gaming Industry'
)
r2.bold = True; r2.font.size = Pt(15); r2.font.name = 'Times New Roman'

doc.add_paragraph('\n\n')
a = doc.add_paragraph()
a.alignment = WD_ALIGN_PARAGRAPH.CENTER
r3 = a.add_run('Uday Vachasiddha\nRoll No: 213065')
r3.font.size = Pt(13); r3.font.name = 'Times New Roman'

doc.add_paragraph()
i = doc.add_paragraph()
i.alignment = WD_ALIGN_PARAGRAPH.CENTER
r4 = i.add_run('Birla Institute of Technology and Science (BITS) Pilani')
r4.font.size = Pt(13); r4.font.name = 'Times New Roman'

doc.add_page_break()

# ══════════════════════════════════════════════════════════════
# 2.1  OVERVIEW OF THE COMPUTING ARTEFACT
# ══════════════════════════════════════════════════════════════
heading1('2.1  Overview of the Computing Artefact')

body(
    'The computing artefact to be designed is an intelligent network security simulation '
    'system — specifically, an AI-driven edge defence pipeline for mitigating Layer 4 '
    'volumetric Distributed Denial of Service (DDoS) attacks targeting real-time multiplayer '
    'gaming servers. The artefact combines a machine-learning classification engine with an '
    'asynchronous real-time streaming backend and a live administrative dashboard, together '
    'forming a complete vertical slice of a production-grade edge security architecture.'
)

body(
    'The importance of this artefact is rooted in a well-documented industry problem. '
    '"Games as a Service" (GaaS) platforms — where revenue is generated through continuous '
    'online player engagement — are acutely vulnerable to DDoS disruption. Unlike web '
    'applications, multiplayer games rely on the User Datagram Protocol (UDP) for its '
    'low-overhead, connectionless packet delivery, which makes them fast but also '
    'fundamentally exposed to volumetric flooding (Zargar, Joshi and Tipper, 2013). A '
    'sustained UDP flood saturates server resources, causing packet loss, disconnections, and '
    'complete service outages. Players who experience this churn away from the platform, '
    'directly damaging developer revenue — a phenomenon this project terms "Lag-to-Churn".'
)

body(
    'Traditional DDoS mitigation relies on centralised scrubbing centres, which reroute '
    'traffic to a remote cleaning facility before returning it to the server. While adequate '
    'for websites tolerating delays of several seconds, this approach adds 50–200ms of '
    'round-trip latency to game sessions, rendering real-time play impossible (Mirkovic and '
    'Reiher, 2004). Furthermore, conventional rule-based firewalls that block traffic above '
    'a fixed rate threshold inevitably produce false positives during organic traffic surges '
    '— such as game launches or tournament events — incorrectly dropping legitimate players '
    'at the worst possible commercial moment.'
)

body(
    'This project addresses these twin failures by developing a simulation of an '
    'intelligent, edge-deployed classification system. Rather than counting raw packet '
    'volumes, the system analyses behavioural metadata — packet size, inter-arrival time, '
    'size variance, and payload entropy — through a Random Forest ensemble classifier. '
    'Because Random Forest operates via simple binary decision tree traversal after '
    'training, its inference latency is measured in microseconds, making it architecturally '
    'compatible with real-time gaming constraints (Buczak and Guven, 2016). The system '
    'also simulates Anycast edge routing by distributing simulated packets across geographic '
    'node labels, and streams live classification metrics to an administrative browser '
    'dashboard via Server-Sent Events (SSE).'
)

heading2('Aims')
body(
    'To develop a simulated, AI-driven network security pipeline that classifies and filters '
    'malicious UDP traffic at the network edge in real time, with a primary objective of '
    'eliminating false positives to ensure legitimate players are never disconnected during '
    'an attack or a high-traffic event.'
)

heading2('Objectives')
plain_bullet('Construct a hybrid training dataset by combining real-world botnet telemetry (Parquet format) with procedurally generated synthetic multiplayer player traffic.')
plain_bullet('Train and validate a Random Forest classifier using Scikit-learn, optimised specifically to minimise the False Positive Rate (FPR) rather than raw accuracy.')
plain_bullet('Implement an asynchronous FastAPI backend to continuously generate, classify, and stream simulated packets to connected clients via SSE.')
plain_bullet('Simulate a global Anycast edge routing environment by assigning each packet a geographic edge node tag (BOM-Edge, FRA-Edge, TYO-Edge, LAX-Edge).')
plain_bullet('Build a real-time browser dashboard in Vanilla JS/HTML that displays live pass/drop metrics, node-level filtering, and a live confusion matrix.')
plain_bullet('Integrate an automated WhatsApp alert system (via PyWhatKit) that fires when the malicious drop counter crosses a defined threshold.')
plain_bullet('Evaluate the system using standard classification metrics: accuracy, FPR, AUC-ROC, and feature importance analysis.')

# ══════════════════════════════════════════════════════════════
# 2.2  AIMS, OBJECTIVES AND SCOPE
# ══════════════════════════════════════════════════════════════
heading1('2.2  Aims, Objectives and Scope')

body(
    'The system will automate the following pipeline: dataset ingestion and preprocessing, '
    'model training on demand via a REST API endpoint, continuous asynchronous packet '
    'simulation, real-time ML classification, SSE-based metric streaming, browser-side '
    'dashboard rendering, and threshold-triggered mobile alerting. It will provide a live '
    'administrative interface allowing an operator to select a target edge node, observe '
    'per-packet pass/drop decisions, monitor cumulative confusion matrix values, and receive '
    'an instant WhatsApp notification when attack volumes breach a critical threshold.'
)

heading2('What the System Will Include')
bullet('Hybrid Dataset Engine: ', 'Real botnet Parquet files loaded via Pandas, merged with synthetic player traffic generated using NumPy statistical distributions.')
bullet('ML Classification Pipeline: ', 'A Scikit-learn Random Forest classifier (100 estimators) with StandardScaler normalisation, trained offline and applied to live packet streams.')
bullet('FastAPI Backend: ', 'An ASGI server hosting a POST /api/train endpoint for model training and a GET /api/simulate SSE endpoint for continuous packet streaming.')
bullet('Anycast Simulation: ', 'Geographic edge node tags (BOM, FRA, TYO, LAX) appended to each packet, with dashboard-side filtering support.')
bullet('Live Dashboard: ', 'A Vanilla JS + HTML browser interface rendering real-time packet logs, pass/drop counters, node filters, and a confusion matrix.')
bullet('Alert Integration: ', 'A PyWhatKit subprocess that sends a WhatsApp message to a configured number when malicious drops exceed 15 per session.')
bullet('Evaluation Graphs: ', 'Matplotlib-generated Confusion Matrix, ROC/AUC Curve, and Feature Importance Chart saved as static PNG files.')

heading2('What the System Will Not Include')
bullet('Kernel-level eBPF/XDP hooks: ', 'Actual packet interception at the NIC requires a Linux kernel environment; this is simulated at the application layer instead.')
bullet('Physical SDN infrastructure: ', 'No GNS3 or Mininet topology is used; all network traffic is procedurally generated in Python.')
bullet('Live internet traffic: ', 'The system processes synthetic and Parquet-sourced data only; no real network interfaces are tapped.')
bullet('Deep Packet Inspection: ', 'The classifier uses only metadata features, deliberately avoiding payload decryption for both latency and GDPR compliance reasons (Sommer and Paxson, 2010).')
bullet('LightGBM or deep learning models: ', 'Only Random Forest is implemented, selected for its sub-millisecond inference speed and explainable feature importance output.')

heading2('Technology Stack and Platform')
body(
    'The system will be developed in Python 3.10 using the following libraries and '
    'frameworks: FastAPI 0.110 (ASGI backend), Scikit-learn 1.4 (Random Forest and '
    'StandardScaler), Pandas 2.x and NumPy 1.26 (data processing), Vanilla JavaScript '
    'ES6+ with HTML5 (frontend dashboard), PyWhatKit 5.4 (WhatsApp alerting), and '
    'Matplotlib 3.8 (evaluation graph generation). The application runs on any standard '
    'operating system supporting Python 3.x, requiring no Linux kernel features or '
    'specialised hardware. Parquet dataset files are stored and read from the local '
    'filesystem using PyArrow. The frontend is served as a static asset by the FastAPI '
    'static file handler, accessible via any modern browser at localhost:8000.'
)

# ══════════════════════════════════════════════════════════════
# 2.3  WORK BREAKDOWN STRUCTURE AND GANTT CHART
# ══════════════════════════════════════════════════════════════
heading1('2.3  Work Breakdown Structure and Gantt Chart')


# ── WBS Table (3-column, phase-level, matching image format) ──
wbs_data = [
    (
        'Phase 1: Research & Setup',
        'Literature review on DDoS mitigation techniques; technology stack selection and justification; project scope definition.',
        'Week 1 – Week 2',
    ),
    (
        'Phase 2: Dataset Construction',
        'Ingesting and parsing real-world botnet Parquet files; generating synthetic multiplayer player traffic using NumPy; merging and balancing the hybrid dataset.',
        'Week 3 – Week 4',
    ),
    (
        'Phase 3: Model Development',
        'Applying StandardScaler normalisation; training the Random Forest classifier (100 estimators); evaluating accuracy, FPR, AUC-ROC, and feature importance; generating evaluation graphs.',
        'Week 5 – Week 6',
    ),
    (
        'Phase 4: Backend & Simulation Engine',
        'Building the FastAPI ASGI server; implementing the POST /api/train REST endpoint; developing the async GET /api/simulate SSE generator for continuous packet streaming.',
        'Week 7 – Week 8',
    ),
    (
        'Phase 5: Frontend Dashboard',
        'Designing the HTML layout and JavaScript event handlers; wiring the SSE stream to live DOM updates; adding geographic edge node filtering and real-time confusion matrix display.',
        'Week 9 – Week 10',
    ),
    (
        'Phase 6: Alert Integration & Testing',
        'Integrating the PyWhatKit WhatsApp threshold alert; conducting end-to-end system testing; recording test case results and evaluation metrics.',
        'Week 11',
    ),
    (
        'Phase 7: Report & Presentation',
        'Writing the final project report; producing evaluation write-up and appendices; preparing and rehearsing the presentation slides.',
        'Week 12 – Week 13',
    ),
]

wbs_table = doc.add_table(rows=1 + len(wbs_data), cols=3)
wbs_table.style = 'Table Grid'

# Set column widths
col_widths = [Inches(1.8), Inches(3.4), Inches(1.2)]
for row in wbs_table.rows:
    for i, cell in enumerate(row.cells):
        cell.width = col_widths[i]

# Header row
hdr_cells = wbs_table.rows[0].cells
for i, hdr_text in enumerate(['Phase', 'Tasks', 'Duration']):
    hdr_cells[i].text = hdr_text
    for para in hdr_cells[i].paragraphs:
        for run in para.runs:
            run.bold = True
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)

# Data rows — alternate light shading for readability
for ri, (phase, tasks, duration) in enumerate(wbs_data):
    row_cells = wbs_table.rows[ri + 1].cells

    # Phase cell — bold
    row_cells[0].text = phase
    for para in row_cells[0].paragraphs:
        for run in para.runs:
            run.bold = True
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)

    # Tasks cell
    row_cells[1].text = tasks
    for para in row_cells[1].paragraphs:
        for run in para.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)

    # Duration cell
    row_cells[2].text = duration
    for para in row_cells[2].paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)

doc.add_paragraph()
cap = doc.add_paragraph('Table 2.1: Work Breakdown Structure')
cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in cap.runs:
    run.italic = True; run.font.size = Pt(10); run.font.name = 'Times New Roman'


doc.add_paragraph()

# ── Gantt Chart (text table) ──────────────────────────────────
body(
    'The Gantt chart below maps each WBS phase across the 13-week project timeline. '
    'Shaded cells indicate active weeks for each phase. ✦ marks key milestones.'
)

gantt_cols = ['Phase / Task', 'W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7',
              'W8', 'W9', 'W10', 'W11', 'W12', 'W13']
gantt_rows = [
    # label,        active weeks (1-indexed), milestone week
    ('1. Research & Lit. Review',         [1,2],        2),
    ('2. Dataset Construction',           [3,4],        4),
    ('3. ML Model Development',           [5,6],        6),
    ('4. Backend & Simulation',           [7,8],        8),
    ('5. Frontend Dashboard',             [9,10],       10),
    ('6. Alert Integration & Testing',    [11],         11),
    ('7. Report & Presentation',          [12,13],      13),
]

n_weeks = 13
gantt_table = doc.add_table(rows=1 + len(gantt_rows), cols=1 + n_weeks)
gantt_table.style = 'Table Grid'

hdr_cells = gantt_table.rows[0].cells
hdr_cells[0].text = 'Phase / Task'
set_cell_bg(hdr_cells[0], '1F3864')
for para in hdr_cells[0].paragraphs:
    for run in para.runs:
        run.bold = True; run.font.name = 'Times New Roman'
        run.font.size = Pt(9); run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)

for w in range(n_weeks):
    hdr_cells[w+1].text = f'W{w+1}'
    set_cell_bg(hdr_cells[w+1], '1F3864')
    for para in hdr_cells[w+1].paragraphs:
        for run in para.runs:
            run.bold = True; run.font.name = 'Times New Roman'
            run.font.size = Pt(9); run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)

for ri, (label, active_weeks, milestone) in enumerate(gantt_rows):
    row_cells = gantt_table.rows[ri+1].cells
    row_cells[0].text = label
    for para in row_cells[0].paragraphs:
        for run in para.runs:
            run.font.name = 'Times New Roman'; run.font.size = Pt(9)

    for w in range(n_weeks):
        week_num = w + 1
        cell = row_cells[w+1]
        if week_num in active_weeks:
            if week_num == milestone:
                cell.text = '✦'
                set_cell_bg(cell, '1A5276')
            else:
                cell.text = '█'
                set_cell_bg(cell, '2980B9')
        else:
            cell.text = ''
        for para in cell.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in para.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)

doc.add_paragraph()
cap2 = doc.add_paragraph('Figure 2.1: Project Gantt Chart  (█ = active week  |  ✦ = milestone)')
cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in cap2.runs:
    run.italic = True; run.font.size = Pt(10); run.font.name = 'Times New Roman'

doc.add_paragraph()
body(
    'Key milestones are: dataset ready (end of Week 4), trained model with evaluation '
    'graphs (end of Week 6), fully functional backend SSE server (end of Week 8), '
    'live dashboard complete (end of Week 10), system testing complete (end of Week 11), '
    'and final report and presentation submitted (end of Week 13).'
)

# ══════════════════════════════════════════════════════════════
# REFERENCES
# ══════════════════════════════════════════════════════════════
doc.add_page_break()
heading1('References')

refs = [
    ('Buczak, A.L. and Guven, E. (2016) \'A survey of data mining and machine learning '
     'methods for cyber security intrusion detection\', IEEE Communications Surveys & '
     'Tutorials, 18(2), pp. 1153–1176. Available at: '
     'https://ieeexplore.ieee.org/document/7307098 (Accessed: 25 April 2026).'),
    ('Mirkovic, J. and Reiher, P. (2004) \'A taxonomy of DDoS attack and DDoS defense '
     'mechanisms\', ACM SIGCOMM Computer Communication Review, 34(2), pp. 39–53. '
     'Available at: https://dl.acm.org/doi/10.1145/997150.997156 '
     '(Accessed: 25 April 2026).'),
    ('Sommer, R. and Paxson, V. (2010) \'Outside the closed world: On using machine '
     'learning for network intrusion detection\', 2010 IEEE Symposium on Security and '
     'Privacy, pp. 305–316. Available at: https://ieeexplore.ieee.org/document/5504793 '
     '(Accessed: 25 April 2026).'),
    ('Zargar, S.T., Joshi, J. and Tipper, D. (2013) \'A survey of defense mechanisms '
     'against distributed denial of service (DDoS) flooding attacks\', IEEE Communications '
     'Surveys & Tutorials, 15(4), pp. 2046–2069. Available at: '
     'https://ieeexplore.ieee.org/document/6524652 (Accessed: 25 April 2026).'),
]

for ref in refs:
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Inches(-0.5)
    p.paragraph_format.left_indent       = Inches(0.5)
    p.paragraph_format.space_after       = Pt(6)
    p.paragraph_format.alignment         = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(ref)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)

# ── Save ──────────────────────────────────────────────────────
out_path = r'd:\BITS Research paper\Proposal_Final_v2.docx'
doc.save(out_path)
print('Saved: ' + out_path)
