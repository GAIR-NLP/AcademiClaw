Query:
---

[Query Description]
Design a data consistency solution for a distributed e-commerce system. The current system uses a microservices architecture and suffers from problems such as inventory overselling, order status inconsistency, and duplicate payment processing.

**Goals:**
1. Analyze consistency issues in distributed transactions (inventory, orders, payments, etc.)
2. Design appropriate solutions to ensure high availability and performance
3. Provide concrete technical implementation ideas or pseudocode/code for key components

**Process:**
1. Read `context/current_order_flow.py` to understand the current order flow and its problems
2. Write a data consistency design document: problem analysis, solution selection, architecture and flow
3. Explain key technical points: distributed locks, TCC/Saga, message queues, idempotency, compensation and reconciliation, etc.
4. Provide implementation examples or pseudocode for key components (inventory deduction, order service, payment service, event handling, monitoring and compensation, etc.)
5. Briefly assess performance impact, high availability, fault tolerance, and scalability
6. Save all deliverables to the current directory

**Deliverable Requirements:**
- Data consistency design document (e.g., `consistency_design.md` or `analysis_report.md`)
- Architecture design and flowchart description (may be merged into the design document or as a separate file)
- Implementation examples or pseudocode for key components (may be merged into the document or as separate .py files)
- Performance impact assessment (may be merged into the design document)

[Context]
File list:
- `context/current_order_flow.py` - Current order flow (with consistency issues)
- `context/operation_list.md` - Operational steps reference
