---
title: Push vs pull — who starts a payment, and why that one fact decides the risk
date: 2026-10-10
module: 01 Intro
series: how-money-moves
order: 2
tags: fundamentals, push payments, pull payments, fraud, UPI, direct debit
summary: Credit push and debit pull look similar on a statement but behave completely differently in risk, speed, reversibility and fraud. A worked comparison using UPI, cards and direct debit.
---

Part 1 introduced the [instruments](../2026-10-10-01-payment-instruments/). This part takes the single most useful distinction among them — **who initiates** — and shows how far it reaches.

## Definitions, without the jargon

- **Push (credit transfer):** the payer tells *their own* bank, "send money to X". The money is pushed out from the payer's side.
- **Pull (debit):** the payee tells *their* bank, "collect money from Y". The request travels back to Y's bank, which decides whether to release the funds.

The same ₹500 can move either way. What changes is which bank is being asked to trust whom.

## UPI shows both in one app

UPI is a good teaching case because it supports both models and most people have used both without noticing.

**UPI "Pay"** — you enter the shop's VPA, the amount, your PIN. Your bank debits you and the money is pushed to the shop's bank. The shop's bank credits the shop in seconds. Nobody asked the shop's permission; a credit is always welcome.

**UPI "Collect" (request money)** — the shop sends you a request. It arrives on your phone; you approve it with your PIN. Technically your bank still debits you only after *you* authorise, so UPI collect is a *pull request that turns into a push on approval*. That design is deliberate: pure pulls, where money leaves without the payer's real-time approval, are where fraud lives. (It is also why NPCI has progressively restricted collect requests from unknown parties.)

## Where the risk sits

| Question | Push (credit transfer) | Pull (direct debit, card) |
|---|---|---|
| Who could lose money by mistake? | The payer (sent to the wrong person, or tricked into sending) | The payer (collected wrongly) — but the *payee's* bank carries the first-line liability |
| Who needs protecting? | The payee needs certainty the money is real; the payer needs protection from being deceived | The payer needs the right to dispute and be refunded |
| Can it be instant? | Yes — the payer's bank verifies funds and identity before sending | Rarely — the payer's bank has not pre-approved this specific amount |
| How is it undone? | Only by asking the payee's bank nicely (recall) — the payee must agree | By rule: refund rights (SEPA DD: 8 weeks no-questions-asked), chargebacks (cards) |
| Typical fraud | Authorised push payment (APP) fraud: scams that persuade the victim to send | Unauthorised debits, card-not-present fraud |

Two consequences follow that explain a lot of what you see at work.

**1. Instant payments are push payments.** UPI, IMPS, SCT Inst, FedNow, UK Faster Payments, Brazil's Pix — all credit-push. The payer's bank has the money and the mandate (the PIN) in hand, so it can commit irrevocably in under ten seconds. There is no equivalent instant pull scheme because the payer's bank would be committing someone else's money on a stranger's request.

**2. Instant plus irrevocable equals fraud pressure.** Once a push can't be undone, scammers switch from stealing credentials to persuading victims. This is why the UK introduced mandatory APP-fraud reimbursement, why Europe made Verification of Payee compulsory alongside instant payments, and why Indian banks have added cooling-off periods for new beneficiaries. The control has to move *before* the payer presses send, because nothing can be done after.

## Cards are a pull that pretends to be instant

A card payment feels instant at the till, but structurally it is a pull: the merchant's bank (acquirer) sends an *authorisation request* through the scheme to your bank (issuer), which says yes or no in a second. No money moves at that point. Clearing and settlement happen later, in batches, and the issuer can reverse the transaction through a chargeback for weeks afterwards. That is why a card refund takes days while a UPI payment is final in seconds: one is a reversible pull, the other an irrevocable push.

## A rule of thumb for requirements

When you read a requirement, find the initiator and you have most of the design:

- *Payer initiates* → verify funds and identity up front, make it fast, worry about scams and wrong beneficiaries, expect recall-request flows rather than refunds.
- *Payee initiates* → verify the mandate, expect delays and batches, build refund and dispute flows, worry about unauthorised collections.

## Next

Now that you know who starts a payment, the next question is who else is involved in moving it. That is the [four-corner model](../2026-10-10-03-four-corner-model-parties/), the diagram behind every rail you'll meet.

*Part 2 of [How money moves](../2026-10-10-00-how-money-moves-map/). Course pairing: [Module 1](../../course/m1/).*
