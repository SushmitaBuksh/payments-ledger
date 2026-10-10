---
title: SEPA — credit transfers, instant payments and direct debits in one rulebook family
date: 2026-10-10
module: 09 Rejects & returns
series: how-money-moves
order: 11
tags: SEPA, SCT, SCT Inst, SDD, direct debit, mandate, R-transactions, verification of payee
summary: How 36 countries made euro payments behave like domestic ones. SCT, SCT Inst and SDD compared, the mandate lifecycle, R-transactions explained with examples, and the 2025–2026 changes every implementation has to handle.
---

Everything so far has described payments in general. SEPA is worth a dedicated part because it is the clearest example of a region deciding that cross-border should feel domestic — and because its rulebooks are free, public and precise, which makes it the best place to learn how a scheme really works. It also gives us the vocabulary for rejects, returns and refunds that the [course's Module 9](../../course/m9/) builds on.

## What SEPA is

The **Single Euro Payments Area** covers the EU plus a handful of other countries (36 in all, including the UK, Switzerland, Norway and, more recently, Albania and Montenegro). Within it, a euro payment from Lisbon to Helsinki must cost the same and work the same as one across town.

It is not one system. It is a set of **schemes** — rulebooks owned by the European Payments Council (EPC) — that any clearing and settlement mechanism can implement. Recall the [four-corner model](../2026-10-10-03-four-corner-model-parties/): the EPC is the scheme, the CSMs (EBA Clearing's STEP2 and RT1, national ACHs, the Eurosystem's TIPS) are the clearing layer, and the Eurosystem's TARGET services are the settlement agent. A bank joins the *scheme* and connects to one or more *CSMs*.

Two legal foundations sit underneath: the SEPA Regulation (260/2012), which made IBAN the account identifier and set end dates for legacy formats, and the Instant Payments Regulation (2024/886), which made instant payments mandatory.

## The three core schemes

| | SCT (credit transfer) | SCT Inst (instant credit transfer) | SDD Core / B2B (direct debit) |
|---|---|---|---|
| Initiated by | Payer (push) | Payer (push) | Payee (pull), under a mandate |
| Speed | Next business day at latest; usually same day | Under 10 seconds, 24×7×365 | Collected on a due date agreed in advance |
| Maximum amount | None in the rulebook | None since October 2025 (participants may still apply limits by bilateral/customer agreement) | None |
| Interbank messages | `pacs.008`, `pacs.004` return, `pacs.002` | `pacs.008`, `pacs.002` (accept/reject within the time-out), `pacs.004` | `pacs.003` collection, `pacs.004` return/refund, `pacs.007` reversal |
| Refund right for payer | No (recall only, payee must agree) | No (recall only) | Core: 8 weeks no-questions; 13 months if unauthorised. B2B: none |
| Who uses it | Everyone | Everyone, by law since 2025 | Core: consumers (utilities, subscriptions). B2B: companies, with a signed mandate lodged at their bank |

Two 2025 milestones changed the landscape and still shape current projects. Under the Instant Payments Regulation, euro-area PSPs had to be able to *receive* SCT Inst by 9 January 2025 and to *send* it by 9 October 2025, at no higher price than a regular SCT. From 9 October 2025 they also have to offer **Verification of Payee** on all credit transfers: before the payer confirms, their bank checks the beneficiary name against the IBAN with the payee's bank and shows "match", "close match" or "no match". It is the EU's answer to the APP-fraud problem that [part 2](../2026-10-10-02-push-vs-pull-payments/) described.

## The direct debit mandate lifecycle

Direct debit is the one instrument where paperwork is part of the rail. A worked example: a Berlin gym collects €49 a month from a member.

1. **Mandate creation.** The member signs a mandate (paper or electronic) authorising the gym to collect, and the gym stores it. Each mandate has a *Unique Mandate Reference*; the gym has a *Creditor Identifier* issued in its country. Under Core, the bank never sees the mandate; under B2B, the payer must also register it with their bank, which checks every collection against it.
2. **Pre-notification.** At least 14 calendar days before the first collection (unless agreed otherwise), the gym tells the member the amount and date.
3. **Collection.** The gym's bank sends `pacs.003` through the CSM to the member's bank with the mandate data inside. The member's bank debits on the due date.
4. **Amendment.** Member changes bank: the mandate continues, with the amendment flagged in the next collection.
5. **Cancellation.** No collection for 36 months lapses the mandate automatically; otherwise the member or gym cancels.

That lifecycle is why direct debit systems need a mandate store, and why migrating one (bank merger, platform change) is a project in itself.

## R-transactions — the vocabulary of things going wrong

SEPA names every exception precisely. Learning these is the fastest way to speak fluently about failures on *any* rail.

| R-transaction | Who sends it | When | Example |
|---|---|---|---|
| **Reject** | Any PSP or CSM, *before* settlement | Message fails validation or checks | IBAN invalid; account closed (`AC04`); format error |
| **Return** | Payee's bank, *after* settlement | Cannot or will not credit | Account number exists but closed yesterday; credit refused by beneficiary |
| **Recall** | Payer's bank, after settlement | Payer asks for money back (duplicate, fraud, wrong beneficiary) | Customer typed the wrong IBAN. The payee's bank asks its customer; `camt.056` request, `camt.029` answer |
| **Refund** (SDD Core only) | Payer's bank | Payer disputes a collection | "I cancelled the gym in March" — 8 weeks no-questions; 13 months for unauthorised |
| **Refusal** | Payer, before debit | Payer tells their bank not to pay this collection | Blocks a known collection in advance |
| **Reversal** | Payee's bank | Payee collected by mistake | Gym collected twice; sends `pacs.007` to give it back |
| **Revocation** / **Request for cancellation** | Payee's bank | Payee withdraws a collection before settlement | Billing run sent in error |

Every R-transaction carries an ISO reason code — `AC01` incorrect account number, `AC04` closed account, `AC06` blocked account, `AM04` insufficient funds, `MD01` no mandate, `MS02` refused by debtor, `SL01` due to specific service offered by the debtor agent, and so on. The EPC publishes guidance on which codes to use when. Memorise a dozen and you will read return files as easily as prose.

Note the one rule that trips people up: in a *reject*, no money moved, so there is nothing to give back. In a *return* or *refund*, money did move and comes back as a new payment in the opposite direction. The accounting from [part 6](../2026-10-10-06-accounting-entries-end-to-end/) applies twice.

## What is changing now

- **Structured addresses.** From November 2026 (15 November for the EPC schemes, aligned with Swift's release), unstructured address text is no longer permitted; addresses must be structured (street, town, postcode, country in separate fields) or hybrid. Every system that stores addresses as free text has a migration to do, and it is the dominant payments project of 2026 in Europe and in cross-border messaging alike.
- **One-leg-out instant credit transfer (OCT Inst).** An EPC scheme for the euro leg of a payment that starts or ends outside SEPA, so a remittance from India can hit a European account instantly once it reaches a SEPA participant. It is the bridge between [part 8's](../2026-10-10-08-cross-border-five-ways/) models.
- **Request-to-Pay and payment-account access schemes** sit alongside the payment schemes, standardising the *ask* for a payment and open-banking access.

## Why a non-European BA should learn SEPA

Because it is the most completely documented scheme in the world, and because its message set is ISO 20022 end to end. Once you can read an SCT `pacs.008`, a return `pacs.004` and a recall `camt.056`, you can read the same messages on Swift CBPR+, on T2, on Fedwire and on Indian systems as they migrate. That is the subject of the final part: [ISO 20022 — what actually changes](../2026-10-10-12-iso-20022-what-changes/).

*Part 11 of [How money moves](../2026-10-10-00-how-money-moves-map/). Course pairing: [Module 9](../../course/m9/) and the regional-rails material in the roadmap.*
