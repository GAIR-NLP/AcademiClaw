[Distributed Data Consistency Design - Operational Steps]

For the current order flow in `context/current_order_flow.py` (check inventory -> deduct inventory -> create order -> payment -> update status), there are consistency issues such as inventory overselling, order and payment status inconsistency, and duplicate payment processing. Please follow the steps below to complete the design and deliverables.

---

**1. Understand the Current Flow and Problems**
- Read `context/current_order_flow.py`: The current implementation uses synchronous serial calls to each service, with no distributed transaction or idempotency guarantees.
- Key analysis points: inventory overselling (concurrent deductions), order status inconsistent with payment/inventory, duplicate charges due to payment retries, etc.

**2. Write the Data Consistency Design Document**
- **Problem Analysis**: inventory overselling, order status inconsistency, distributed transactions, idempotency requirements.
- **Solution Selection**: distributed locks, TCC/Saga, message queues, idempotent design, compensation and reconciliation.
- **Architecture and Flow**: service boundaries, call sequence, event-driven or two-phase commit, etc.
- Save as `consistency_design.md` or `analysis_report.md` in the current directory.

**3. Key Technical Points and Implementation Ideas**
- **Distributed Locks**: concurrency control for inventory deduction.
- **TCC or Saga**: Try-Confirm-Cancel or compensation flow.
- **Message Queues**: asynchronous events, eventual consistency, retries and dead-letter queues.
- **Idempotency**: idempotent implementation of payment, order creation, and other interfaces.
- **Compensation Mechanisms**: reconciliation tasks, timeout cancellation, status repair.

**4. Implementation Examples or Pseudocode for Key Components**
- Inventory deduction (reserve/confirm/release).
- Order service (create/confirm/cancel).
- Payment service (idempotent payment, result notification).
- Event handling (payment success, order cancellation, timeout, etc.).
- Monitoring and reconciliation (inconsistency detection, compensation triggers).
- May be included in the design document or as separate `.py` files.

**5. Performance and Reliability Assessment**
- Performance impact: lock granularity, message latency, retry strategies.
- Brief description of high availability, fault tolerance, and scalability.

**6. Deliverables and Saving**
- Save all deliverables in the current working directory: design document, architecture description, key code or pseudocode, performance assessment.
