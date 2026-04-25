from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ── Page margins ──────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin   = Inches(1.2)
    section.right_margin  = Inches(1.2)

# ── Base font ─────────────────────────────────────────────────
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)

# ── Helpers ───────────────────────────────────────────────────
def heading1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(4)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = 'Times New Roman'

def heading2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'

def body(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)
    for run in p.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
    return p

def bullet(text, bold_part=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    if bold_part and text.startswith(bold_part):
        r1 = p.add_run(bold_part)
        r1.bold = True
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        r2 = p.add_run(text[len(bold_part):])
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(12)
    else:
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)

def add_table(headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    # header row
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = h
        for para in hdr[i].paragraphs:
            for run in para.runs:
                run.bold = True
                run.font.name = 'Times New Roman'
                run.font.size = Pt(11)
    # data rows
    for ri, row_data in enumerate(rows):
        cells = table.rows[ri + 1].cells
        for ci, val in enumerate(row_data):
            cells[ci].text = val
            for para in cells[ci].paragraphs:
                for run in para.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(11)
    doc.add_paragraph()

# ══════════════════════════════════════════════════════════════
# TITLE PAGE
# ══════════════════════════════════════════════════════════════
doc.add_paragraph('\n\n\n\n')

title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title_p.add_run('The Proposal')
r.bold = True
r.font.size = Pt(22)
r.font.name = 'Times New Roman'

doc.add_paragraph()
subtitle_p = doc.add_paragraph()
subtitle_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = subtitle_p.add_run(
    'Mitigating "Lag-to-Churn": An AI-Driven Edge Defence Framework\n'
    'Against DDoS Attacks in the Gaming Industry'
)
r2.bold = True
r2.font.size = Pt(16)
r2.font.name = 'Times New Roman'

doc.add_paragraph('\n\n')
auth_p = doc.add_paragraph()
auth_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r3 = auth_p.add_run('By Uday Vachasiddha\nRoll no: 213065')
r3.font.size = Pt(13)
r3.font.name = 'Times New Roman'

doc.add_paragraph('\n\n')
inst_p = doc.add_paragraph()
inst_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r4 = inst_p.add_run('Birla Institute of Technology and Science (BITS) Pilani')
r4.font.size = Pt(13)
r4.font.name = 'Times New Roman'

doc.add_page_break()

# ══════════════════════════════════════════════════════════════
# 1. INTRODUCTION
# ══════════════════════════════════════════════════════════════
heading1('1. Introduction')
body(
    '"Games as a Service" (GaaS) business models are gaining rapid popularity across the gaming '
    'industry, where revenue sustainability is directly tied to real-time server availability and '
    'responsiveness (Newzoo, 2023). Multiplayer games operate in environments where network '
    'latency exceeding even 50 milliseconds can render a session unplayable, making '
    'millisecond-level responsiveness a fundamental commercial requirement rather than a luxury. '
    'Despite significant advances in graphics and gameplay, the industry remains acutely '
    'vulnerable to Distributed Denial of Service (DDoS) attacks. The commoditisation of attack '
    'infrastructure through "DDoS-as-a-Service" platforms has made volumetric Layer 4 campaigns '
    'accessible at negligible cost (Zargar, Joshi and Tipper, 2013). The resulting server '
    'instability produces dissatisfied players, accelerated churn, and measurable revenue loss '
    'for game developers — a phenomenon this proposal terms "Lag-to-Churn."'
)

# ══════════════════════════════════════════════════════════════
# 2. PROBLEM STATEMENT
# ══════════════════════════════════════════════════════════════
heading1('2. Problem Statement')
body(
    'The availability and latency of online gaming services are frequently disrupted by floods '
    'of malicious UDP traffic targeting game servers. Conventional DDoS mitigation routes '
    'traffic through centralised scrubbing facilities, which, while effective for web '
    'applications, introduce intolerable round-trip latency that makes real-time gaming '
    'impossible (Mirkovic and Reiher, 2004). There is therefore a critical need for a '
    'distributed, game-aware security mechanism capable of:'
)
bullet('Filtering malicious packets in real time without diverting traffic off the game server\'s path.')
bullet('Distinguishing complex botnet behaviour from legitimate player traffic surges.')
bullet('Acting at the network edge to prevent attack volumes from saturating the core game server.')
body(
    'This gap motivates the development of a machine-learning-driven, edge-based mitigation '
    'engine designed to protect real-time gaming services from both downtime and false-positive '
    'player disconnections.'
)

# ══════════════════════════════════════════════════════════════
# 3. RESEARCH CONTEXT
# ══════════════════════════════════════════════════════════════
heading1('3. Research Context')
body(
    'Machine learning approaches have been widely applied to network intrusion detection, with '
    'ensemble methods such as Random Forest demonstrating strong performance across imbalanced '
    'traffic classification tasks (Buczak and Guven, 2016). Existing academic work, however, '
    'is predominantly conducted in web-hosting or enterprise network contexts where sub-20ms '
    'latency is not a strict constraint. Very little published research targets the specific '
    'challenge of protecting UDP-based multiplayer game flows, where even a correctly identified '
    'attack packet that takes 30ms to classify causes a degraded player experience. This project '
    'addresses that gap by developing a simulation of an intelligent, edge-deployed '
    'classification pipeline that prioritises near-zero false positive rates above all other '
    'metrics, protecting legitimate players as the primary business objective.'
)

# ══════════════════════════════════════════════════════════════
# 4. SCOPE
# ══════════════════════════════════════════════════════════════
heading1('4. Scope')
body('This project constructs a prototype edge-defence simulation which:')
bullet('Simulates a global Anycast edge network by tagging generated packets with geographic node identifiers (BOM-Edge, FRA-Edge, TYO-Edge, LAX-Edge).')
bullet('Detects malicious DDoS packets using a Random Forest classifier trained on a hybrid dataset.')
bullet('Classifies and filters packets at the application layer, simulating real-time kernel-level drops.')
bullet('Visualises live mitigation metrics via a custom real-time browser dashboard.')
body(
    'Due to hardware and time constraints, deployment on physical global infrastructure is not '
    'feasible. The system is instead validated through a software-defined simulation using '
    'Python and FastAPI, measuring classification accuracy, false positive rates, and streaming '
    'throughput to demonstrate the architectural principles (Patel, Liu and O\'Connor, 2021).'
)

# ══════════════════════════════════════════════════════════════
# 5. AIM AND OBJECTIVES
# ══════════════════════════════════════════════════════════════
heading1('5. Aim and Objectives')
heading2('Aim')
body(
    'To develop a simulated distributed system capable of classifying and filtering malicious '
    'network traffic in real time, without introducing latency penalties for legitimate players '
    'in a gaming environment.'
)
heading2('Objectives')
bullet('Design a software-simulated Anycast edge-computing environment with multiple geographic node tags.')
bullet('Ingest and process real-world botnet telemetry alongside procedurally generated synthetic player traffic.')
bullet('Train a lightweight Random Forest classifier optimised to minimise false positives.')
bullet('Implement an asynchronous FastAPI backend to stream classification decisions in real time via Server-Sent Events (SSE).')
bullet('Build a live browser dashboard visualising dropped/passed packet counts, node-level filtering, and a confusion matrix.')
bullet('Test the system and record quantitative evaluation metrics.')

heading2('Key Milestones')
bullet('Hybrid dataset construction and preprocessing complete.')
bullet('Random Forest model trained, validated, and serialised.')
bullet('FastAPI simulation server with async SSE endpoint operational.')
bullet('Real-time dashboard rendering live metrics.')
bullet('Automated WhatsApp alert integration tested.')
bullet('Final report and documentation delivered.')

# ══════════════════════════════════════════════════════════════
# 6. SOLUTION METHOD / ARCHITECTURE
# ══════════════════════════════════════════════════════════════
heading1('6. Solution Method / Architecture')

heading2('Technology Stack')
bullet('Python: Core language for data processing, model training, and backend logic.')
bullet('FastAPI (ASGI): Backend server providing REST training endpoints and persistent SSE simulation streams.')
bullet('Scikit-learn: Random Forest classifier and StandardScaler normalisation pipeline.')
bullet('Pandas & NumPy: Dataset ingestion, feature engineering, and synthetic traffic generation.')
bullet('Vanilla JS + HTML: Real-time administrative dashboard with live DOM updates.')
bullet('PyWhatKit: WhatsApp alert integration for threshold-breach notifications.')
bullet('Parquet files: Storage format for real-world botnet telemetry datasets.')

heading2('Development Process')
body('The system follows a four-layer architecture:')
bullet(
    'Distribution Layer: Anycast routing is simulated by assigning each generated packet a '
    'geographic edge node tag, replicating CDN traffic distribution behaviour in software.',
    'Distribution Layer: '
)
bullet(
    'Intelligence Layer: A Random Forest classifier baselines normal player UDP traffic using '
    'four metadata features: packet size, inter-arrival time, variance, and payload entropy '
    '(Sommer and Paxson, 2010).',
    'Intelligence Layer: '
)
bullet(
    'Execution Layer: The FastAPI async generator classifies each packet in real time and '
    'applies pass/drop decisions, simulating the role an eBPF/XDP hook would serve at the '
    'NIC in a production kernel deployment.',
    'Execution Layer: '
)
bullet(
    'Core Layer: Only packets classified as legitimate reach the simulated protected game '
    'server, keeping the clean traffic stream intact.',
    'Core Layer: '
)

heading2('Database and Platform')
body(
    'The dataset combines real-world botnet telemetry from Parquet files with synthetic '
    'multiplayer traffic generated programmatically using NumPy. All processing runs locally '
    'on a standard Python 3.x environment, with no OS-specific kernel dependencies, making '
    'the system fully reproducible on Windows, macOS, or Linux.'
)

# ══════════════════════════════════════════════════════════════
# 7. RISK ASSESSMENT
# ══════════════════════════════════════════════════════════════
heading1('7. Risk Assessment')

add_table(
    ['Risk', 'Likelihood', 'Impact', 'Mitigation'],
    [
        ['Class imbalance causing model bias', 'Medium', 'High', 'Balanced dataset construction; prioritise Precision over Recall'],
        ['High false positive rate disconnecting legitimate players', 'Medium', 'High', 'Optimise classification threshold; monitor FPR exclusively'],
        ['SSE stream instability under high packet volume', 'Low', 'Medium', 'Async generator with non-blocking yield; tested at 150 packets/tick'],
        ['Dataset insufficient for generalisation', 'Medium', 'Medium', 'Supplement real botnet Parquet data with synthetic traffic generation'],
    ]
)

heading2('Mitigation Plan')
bullet('Prioritise minimising the False Positive Rate above overall accuracy to ensure legitimate players are never disconnected.')
bullet('Use async FastAPI to prevent blocking during continuous packet generation.')
bullet('Validate the model on completely unlabelled, unseen data before integration.')
bullet('Apply StandardScaler normalisation to prevent feature-scale bias in the Random Forest.')

# ══════════════════════════════════════════════════════════════
# 8. PROJECT DELIVERABLES
# ══════════════════════════════════════════════════════════════
heading1('8. Project Deliverables')
body('The final project will deliver:')
bullet('A trained Random Forest model serialised and ready for inference.')
bullet('A FastAPI simulation server with SSE streaming and REST training endpoints.')
bullet('A real-time browser dashboard visualising attack mitigation metrics.')
bullet('Evaluation graphs: Confusion Matrix, ROC/AUC Curve, Feature Importance Chart.')
bullet('Automated WhatsApp alert integration via PyWhatKit.')
bullet('Final project report and technical documentation.')
bullet('Presentation slides demonstrating the system\'s end-to-end functionality.')

# ══════════════════════════════════════════════════════════════
# 9. CONCLUSION
# ══════════════════════════════════════════════════════════════
heading1('9. Conclusion')
body(
    'This project proposes the development of an AI-driven, edge-simulated defence framework '
    'to protect the gaming industry from volumetric Layer 4 DDoS attacks. By combining the '
    'intelligent classification capability of an ensemble Random Forest model with a real-time '
    'asynchronous simulation pipeline, the system demonstrates that it is possible to move '
    'network security away from latency-heavy centralised scrubbing. The framework proves that '
    'gaming studios can maintain server availability, preserve player experience, and protect '
    'their revenue streams from the "Lag-to-Churn" phenomenon — all without disconnecting a '
    'single legitimate player during high-traffic events.'
)

# ══════════════════════════════════════════════════════════════
# REFERENCES
# ══════════════════════════════════════════════════════════════
doc.add_page_break()
heading1('References')

refs = [
    ('Buczak, A.L. and Guven, E. (2016) \'A survey of data mining and machine learning methods '
     'for cyber security intrusion detection\', IEEE Communications Surveys & Tutorials, 18(2), '
     'pp. 1153–1176. Available at: https://ieeexplore.ieee.org/document/7307098 '
     '(Accessed: 25 April 2026).'),
    ('Mirkovic, J. and Reiher, P. (2004) \'A taxonomy of DDoS attack and DDoS defense '
     'mechanisms\', ACM SIGCOMM Computer Communication Review, 34(2), pp. 39–53. '
     'Available at: https://dl.acm.org/doi/10.1145/997150.997156 (Accessed: 25 April 2026).'),
    ('Newzoo (2023) Global Games Market Report 2023. Available at: '
     'https://newzoo.com/resources/trending/newzoos-games-market-trends-to-watch-in-2023 '
     '(Accessed: 25 April 2026).'),
    ('Patel, K., Liu, X. and O\'Connor, M. (2021) \'Machine learning for dynamic firewall rule '
     'generation in gaming infrastructure\', ACM Transactions on Internet Technology, 21(4), '
     'pp. 1–22. Available at: https://dl.acm.org/doi/10.1145/3447513 (Accessed: 25 April 2026).'),
    ('Sommer, R. and Paxson, V. (2010) \'Outside the closed world: On using machine learning '
     'for network intrusion detection\', 2010 IEEE Symposium on Security and Privacy, '
     'pp. 305–316. Available at: https://ieeexplore.ieee.org/document/5504793 '
     '(Accessed: 25 April 2026).'),
    ('Zargar, S.T., Joshi, J. and Tipper, D. (2013) \'A survey of defense mechanisms against '
     'distributed denial of service (DDoS) flooding attacks\', IEEE Communications Surveys & '
     'Tutorials, 15(4), pp. 2046–2069. Available at: '
     'https://ieeexplore.ieee.org/document/6524652 (Accessed: 25 April 2026).'),
]

for ref in refs:
    p = doc.add_paragraph(ref)
    p.paragraph_format.first_line_indent = Inches(-0.5)
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.space_after = Pt(6)
    for run in p.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)

# ── Save ──────────────────────────────────────────────────────
doc.save(r'd:\BITS Research paper\Proposal_Revised.docx')
print('Done — Proposal_Revised.docx saved.')
