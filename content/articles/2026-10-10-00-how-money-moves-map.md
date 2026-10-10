---
title: How money moves — the complete map of the payments domain in 12 parts
date: 2026-10-10
module: General
series: how-money-moves
order: 0
tags: series, fundamentals, overview, learning path
summary: Start here. A 12-part series that builds the payments domain from first principles — instruments, push and pull, the four-corner model, clearing and settlement, accounting, participation, cross-border, correspondent banking, Swift, SEPA and ISO 20022 — each part with worked examples and linked to the next.
---

Most payments knowledge arrives in fragments: an MT103 field here, a UPI limit there, a half-remembered diagram of nostro accounts. The fragments never quite join up, so every new rail or message feels like starting over.

This series is an attempt to fix that. Twelve parts, read in order, each building on the last, each with a worked example you can redo yourself. By the end, a `pacs.008` crossing three correspondents should feel like the obvious consequence of a few simple ideas rather than a wall of XML.

## The map

```
 ┌────────────────────── WHAT A PAYMENT IS ──────────────────────┐
 │  1 Instruments  →  2 Push vs pull  →  3 Four-corner model     │
 └────────────────────────────┬───────────────────────────────────┘
                              ▼
 ┌────────────────────── HOW IT IS PROCESSED ─────────────────────┐
 │  4 Clearing vs settlement → 5 Netting & risk → 6 Accounting   │
 │                       7 Participation & on-us                  │
 └────────────────────────────┬───────────────────────────────────┘
                              ▼
 ┌────────────────────── ACROSS BORDERS ──────────────────────────┐
 │  8 Five cross-border models → 9 Correspondent banking          │
 │                      10 Swift                                  │
 └────────────────────────────┬───────────────────────────────────┘
                              ▼
 ┌────────────────────── SCHEMES AND STANDARDS ───────────────────┐
 │  11 SEPA (SCT, Inst, direct debit)  →  12 ISO 20022            │
 └────────────────────────────────────────────────────────────────┘
```

## The parts

**Block 1 — what a payment is**

1. [Payment instruments — the six ways money actually moves](../2026-10-10-01-payment-instruments/). One rent payment paid six ways; why credit transfers and direct debits are the two that matter.
2. [Push vs pull — who starts a payment, and why that one fact decides the risk](../2026-10-10-02-push-vs-pull-payments/). UPI pay vs collect, why instant payments are always push, and why that creates fraud pressure.
3. [The four-corner model — every payment system drawn on one napkin](../2026-10-10-03-four-corner-model-parties/). Payer, PSPs, payee, plus scheme, CSM and settlement agent. A UPI payment and a SEPA transfer mapped onto it.

**Block 2 — how it is processed**

4. [Clearing vs settlement — the two words you have to get right first](../2026-10-10-04-clearing-vs-settlement/). Why a cheque takes two days and UPI takes two seconds.
5. [Netting, liquidity and settlement risk — with the numbers](../2026-10-10-05-netting-liquidity-settlement-risk/). A three-bank example where netting cuts cash needs by 87%, and what Herstatt taught everyone about the cost.
6. [The accounting entries behind a payment, end to end](../2026-10-10-06-accounting-entries-end-to-end/). The same payment booked on-us, via the central bank, and via a correspondent — every debit and credit, including the nostro mirror.
7. [Direct and indirect participants — how a fintech gets into a payment system](../2026-10-10-07-participation-and-on-us/). Sponsor banks, why indirect access shapes limits and cut-offs, and why on-us payments are a competitive moat.

**Block 3 — across borders**

8. [Cross-border payments — the five ways money crosses a border](../2026-10-10-08-cross-border-five-ways/). Correspondent banking, linked instant systems, closed-loop providers, cards and tokenised money, compared on one remittance.
9. [Correspondent banking in detail — serial vs cover payments, charges and the messages](../2026-10-10-09-correspondent-banking-serial-cover/). A USD 50,000 payment through a three-bank chain both ways, with OUR/SHA/BEN worked through.
10. [Swift — what it is, what it isn't, and the five things it actually gives you](../2026-10-10-10-swift-what-it-is/). Cooperative, network, standards, services; BIC, RMA, FIN/FINplus, gpi, UETR.

**Block 4 — schemes and standards**

11. [SEPA — credit transfers, instant payments and direct debits in one rulebook family](../2026-10-10-11-sepa-sct-inst-direct-debit/). SCT vs SCT Inst vs SDD, the mandate lifecycle, every R-transaction with an example, and the 2025–2026 changes.
12. [ISO 20022 — what actually changes when a payment becomes a pacs.008](../2026-10-10-12-iso-20022-what-changes/). The same payment as MT103 and pacs.008 side by side, the three message families on the four-corner model, and the dates that still matter.

## How to use the series

- **Read in order the first time.** Each part assumes the previous ones; the cross-links let you jump back when a term is unfamiliar.
- **Do the "check yourself" questions.** They are the same kind of question you'll be asked in an interview or an incident call.
- **Pair each part with the course module it names.** The [course](../../course/) has the primary sources — RBI FAQs, Swift pages, EPC rulebooks, the ISO 20022 catalogue — so you can verify everything here against the originals.
- **Redo the examples with your own numbers.** Change the banks, the amounts, the charge option. If the entries still balance and the messages still make sense, you understand it.

## What the series does not cover (yet)

Cards in depth (authorisation, interchange, 3-D Secure), the Indian rails one by one (RTGS, NEFT, IMPS, UPI as systems rather than examples), exceptions and investigations under ISO 20022 in detail, payment hubs and host-to-host connectivity, and the business-analysis craft around all of it. Those are the [course modules](../../course/) and the articles to come.

*This is the index for the series. Start with [part 1](../2026-10-10-01-payment-instruments/).*
