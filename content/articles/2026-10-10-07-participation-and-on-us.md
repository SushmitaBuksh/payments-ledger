---
title: Direct and indirect participants — how a fintech gets into a payment system
date: 2026-10-10
module: 02 Indian rails
series: how-money-moves
order: 7
tags: participation, sponsor bank, indirect participant, on-us, fintech, access
summary: Not everyone who sends payments has an account at the central bank. How sponsor banks, indirect access and on-us routing work, with examples from UPI, SEPA and the UK.
---

[Part 6](../2026-10-10-06-accounting-entries-end-to-end/) showed settlement happening across accounts at the central bank. That raises an obvious question: what about institutions that don't have one? Most fintechs, many small banks and all foreign branches without a local licence fall into that group. This part explains the two ways in, and why "on-us" is the quiet third option.

## Direct participation

A **direct participant** is a member of the scheme in its own right. It:

- holds a settlement account with the settlement agent (the central bank, or a designated settlement bank),
- connects technically to the clearing system,
- signs the scheme rulebook and is liable for its own obligations,
- is subject to the operator's eligibility rules — licence type, capital, operational resilience, liquidity arrangements.

Direct participation is expensive and slow to obtain. It is also the only way to control your own settlement risk and cut-off times, which is why large banks always want it.

## Indirect participation

An **indirect participant** reaches the system *through* a direct participant, usually called the **sponsor bank** (also "settlement bank", "agency bank" or "correspondent", depending on the market).

```
Customer ─▶ Indirect participant ─▶ Sponsor bank (direct) ─▶ Clearing system ─▶ ... 
```

The sponsor bank:

- settles on the indirect participant's behalf from its own central-bank account,
- carries the scheme liability for the indirect participant's payments,
- in return charges fees and imposes limits, collateral and monitoring — because if the indirect participant fails, the sponsor is the one the scheme comes to.

From the scheme's point of view, the payment is the sponsor's. From the customer's point of view, it is the indirect participant's. Reconciling those two views is a job in itself.

### Examples

**UPI.** A UPI app (the "third-party app provider") is not a bank and has no RBI settlement account. It connects to UPI through a **PSP bank**; the actual debit and credit happen on accounts at the customer's bank, and settlement runs between banks at the RBI. When the app shows "powered by HDFC Bank" or "Axis Bank" in its footer, that is the sponsor relationship made visible. This is also why NPCI's market-share cap on UPI apps and its rules on multi-bank sponsorship exist: too much volume through one sponsor concentrates risk.

**SEPA.** Thousands of small European banks and payment institutions reach SCT and SCT Inst as indirect participants through a larger bank's connection to a CSM. The EPC rulebook binds the scheme participant; the indirect participant's obligations are in its contract with the sponsor. Since the Instant Payments Regulation, payment and e-money institutions can also apply for direct access to settlement systems in the euro area — a deliberate policy to reduce dependence on sponsor banks.

**United Kingdom.** The Bank of England opened direct RTGS settlement accounts to non-bank payment service providers in 2018 (TransferWise, now Wise, was first). Before that, every fintech needed a sponsor bank for Faster Payments; many still use one because the operational burden of direct membership is heavy.

## Why indirect access shapes product behaviour

A few things that puzzle new BAs become obvious once you know a participant is indirect:

- **Cut-offs earlier than the scheme's.** The sponsor needs time to batch, check and submit, so the indirect participant's customer deadline is earlier.
- **Limits that don't match the scheme's.** The sponsor's per-day exposure limit, not the scheme's transaction limit, is often the binding constraint.
- **Returns that take an extra hop.** A return comes to the sponsor first, then is passed on; the indirect participant sees it later and sometimes with less information.
- **"Account name" mismatches.** Payments to or from an indirect participant may show the sponsor's name in bank-level data. Verification-of-payee services have to handle this.

## On-us: the payment that never leaves the building

The third way to move money is not to use a payment system at all. If both payer and payee hold accounts at the same institution, the payment is **on-us** (also "book transfer", "intra-bank" or "internal transfer"). [Part 6, case 1](../2026-10-10-06-accounting-entries-end-to-end/) showed the entries: one liability down, another up, nothing else.

On-us payments matter more than their simplicity suggests:

1. **They are free and instant,** so banks route to them whenever the destination account is their own — including, in many systems, when a customer *thinks* they are sending via NEFT or SEPA. The channel accepts the scheme instruction; the engine spots the on-us destination and books it internally.
2. **They skip scheme controls** — sanctions screening and fraud checks still apply, but the scheme's reject/return codes, timings and reason codes don't. Reporting and reconciliation have to treat them as their own category.
3. **They are a competitive moat.** The bigger a bank's customer base, the more of its payments are on-us. Big-tech wallets and super-apps aim for exactly this: once everyone is inside, most payments are book transfers and the external rails are only for the edges. Three-corner schemes from [part 3](../2026-10-10-03-four-corner-model-parties/) are on-us by design.

## A practical check for requirements

When a payment feature is described, ask three questions in this order:

1. Is the destination on-us? If yes, none of the scheme rules apply — but your internal rules do.
2. If not, are we a direct or indirect participant on the rail that reaches it? That decides limits, cut-offs and who sees returns.
3. If the rail is cross-border, which correspondent are we going through? That is [part 8](../2026-10-10-08-cross-border-five-ways/) and [part 9](../2026-10-10-09-correspondent-banking-serial-cover/).

*Part 7 of [How money moves](../2026-10-10-00-how-money-moves-map/). Course pairing: [Module 2](../../course/m2/).*
