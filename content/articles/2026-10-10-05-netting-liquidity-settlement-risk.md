---
title: Netting, liquidity and settlement risk — with the numbers
date: 2026-10-10
module: 01 Intro
series: how-money-moves
order: 5
tags: netting, RTGS, deferred net settlement, liquidity, Herstatt, settlement risk
summary: A three-bank worked example showing how multilateral netting cuts the cash needed by 80%, what that saving costs in risk, and why RTGS and deferred net systems both still exist.
---

[Part 4](../2026-10-10-04-clearing-vs-settlement/) said gross settlement is safe but liquidity-hungry and net settlement is efficient but risky. This part makes that concrete, because the numbers are what make the design choices obvious.

## Three banks, six payments

Over one morning, three banks make these payments to each other (₹ crore):

| From → To | Amount |
|---|---|
| A → B | 100 |
| B → A | 80 |
| B → C | 60 |
| C → B | 90 |
| A → C | 40 |
| C → A | 30 |

Total value moved: **400 crore**.

### Gross settlement (RTGS style)

Each payment settles individually, in full, as it happens. Across the morning the banks need enough cash at the central bank to cover each outgoing payment at the moment it is sent. Worst case, before any inflows arrive:

- A must fund 100 + 40 = **140**
- B must fund 80 + 60 = **140**
- C must fund 90 + 30 = **120**

Total liquidity that has to be sitting idle at the central bank: **400 crore** — the full value. In practice inflows offset outflows during the day, and RTGS systems add queueing and liquidity-saving mechanisms, but the principle holds: gross settlement needs a lot of cash on hand.

### Bilateral netting

Each pair settles only the difference:

- A↔B: A owes B 100, B owes A 80 → **A pays B 20**
- B↔C: B owes C 60, C owes B 90 → **C pays B 30**
- A↔C: A owes C 40, C owes A 30 → **A pays C 10**

Cash actually moved: 20 + 30 + 10 = **60 crore**. An 85% reduction already.

### Multilateral netting

Now compute each bank's single net position against everyone:

- A: receives 80 + 30 = 110, pays 100 + 40 = 140 → **net −30**
- B: receives 100 + 90 = 190, pays 80 + 60 = 140 → **net +50**
- C: receives 60 + 40 = 100, pays 90 + 30 = 120 → **net −20**

The CSM instructs the settlement agent: debit A 30, debit C 20, credit B 50. Cash moved: **50 crore**. Positions always sum to zero, which is how you check the arithmetic.

| Method | Cash that moves | Share of gross value |
|---|---|---|
| Gross | 400 | 100% |
| Bilateral net | 60 | 15% |
| Multilateral net | 50 | 12.5% |

This is why ACH systems, card schemes and most retail rails are **deferred net settlement (DNS)**: they net all day and settle once or a few times, and the banks need a fraction of the cash.

## What netting costs: exposure until settlement

Between the moment B's customers are credited and the moment the net 50 crore actually arrives, B is *exposed*. If A fails before settlement, B has already released money it has not received. Scale that across a whole banking system and you have **systemic settlement risk**.

The textbook case is **Bankhaus Herstatt**, a German bank closed by regulators on 26 June 1974 in the German afternoon. Counterparties had already paid Deutsche Marks to Herstatt that morning; the US dollar legs due back to them in New York were never paid. Time-zone gaps turned a small bank's failure into a global scare, and "Herstatt risk" became the name for the risk that you pay your side of a deal and the other side never arrives.

Two responses followed over the next decades:

1. **RTGS for large values.** Central banks built real-time gross systems so that high-value payments settle finally, one by one, with no interbank exposure. India's RTGS (2004, 24×7 since 2020), the Eurosystem's T2, Fedwire, CHAPS. The minimum RTGS amount in India (₹2 lakh) exists precisely to push large, risky payments onto the gross rail and leave small ones to netting.
2. **Risk controls on DNS systems.** Net systems added collateral pools, debit caps, loss-sharing agreements and guarantee funds so that one participant's failure doesn't unwind everyone's payments. For FX specifically, CLS Bank (2002) settles both currency legs simultaneously — payment-versus-payment — so neither side pays without receiving.

## How instant payments square the circle

Instant rails like UPI, IMPS and SCT Inst credit the payee in seconds but settle between banks on a net basis later. How is that not Herstatt risk every two seconds? Through **prefunding and caps**: participants keep a funded position (or collateral) with the operator, and each bank's net debit is capped at what it has prefunded. The payee's bank can credit instantly because the scheme guarantees the money is already there. This is why "becoming a UPI participant" involves liquidity arrangements, not just an API.

## The design space, in one table

| System type | Settlement | Liquidity need | Interbank exposure | Typical use |
|---|---|---|---|---|
| RTGS (RTGS India, T2, Fedwire) | Gross, real time, final | High | None | Large-value, time-critical |
| DNS / ACH (NEFT, SEPA SCT via STEP2, BACS) | Net, in cycles | Low | Until the cycle settles | Bulk, low-value, non-urgent |
| Instant retail (UPI, IMPS, SCT Inst) | Net, with prefunding/caps | Medium (prefunded) | Capped by prefunding | Real-time retail |
| Card schemes | Net, daily | Low | Scheme guarantees + collateral | Retail purchases |

## Why a BA should care

- "Why can't we raise the limit?" is usually a liquidity-and-caps question, not a technology question.
- Cut-off times exist because net cycles have to close before settlement; a requirement to "accept payments until 23:59" has settlement consequences.
- When a payment is "credited but not settled", the two banks' books disagree until the cycle completes — that is where reconciliation breaks and investigations begin. Which is the perfect lead-in to [part 6: the accounting entries, end to end](../2026-10-10-06-accounting-entries-end-to-end/).

*Part 5 of [How money moves](../2026-10-10-00-how-money-moves-map/). Course pairing: [Module 1](../../course/m1/) and [Module 2](../../course/m2/).*
