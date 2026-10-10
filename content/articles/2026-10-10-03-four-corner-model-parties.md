---
title: The four-corner model — every payment system drawn on one napkin
date: 2026-10-10
module: 01 Intro
series: how-money-moves
order: 3
tags: fundamentals, four-corner model, scheme, CSM, settlement agent
summary: Payer, payer's bank, payee's bank, payee — plus the three things in the middle nobody draws. One UPI payment and one SEPA transfer mapped onto the model, and where three-corner schemes fit.
---

If you can draw one diagram from memory in this domain, make it this one. Every rail — UPI, NEFT, SEPA, Swift correspondent banking, Visa — is a variation on the **four-corner model**. Parts [1](../2026-10-10-01-payment-instruments/) and [2](../2026-10-10-02-push-vs-pull-payments/) told you what a payment is and who starts it; this part tells you who carries it.

## The four corners

```
  Payer  ──────────────────────────────  Payee
    │                                      │
    │ (customer-to-bank)                   │ (bank-to-customer)
    │                                      │
 Payer's PSP ───────(interbank)──────── Payee's PSP
```

- **Payer** (debtor, originator, remitter): the person or company whose account is debited.
- **Payer's PSP** (debtor agent, originating bank): holds the payer's account and sends the payment out. *PSP* — payment service provider — is the neutral word, because it might be a bank, a fintech, or a wallet.
- **Payee's PSP** (creditor agent, beneficiary bank): receives the payment and credits its customer.
- **Payee** (creditor, beneficiary): whose account is credited.

The two vertical edges are **customer-to-bank** legs: the payer's instruction in, the payee's statement out. The horizontal edge is the **interbank** leg, where the industry's standards and systems live.

## The three things in the middle

The napkin version stops there, but real payments need three more roles between the two PSPs. They are often one organisation, which is why beginners miss them.

1. **The scheme (rulebook owner).** Writes the rules every participant signs: message formats, timings, fees, how to handle returns. NPCI for UPI; the European Payments Council for SEPA; Visa and Mastercard for cards; Swift's CBPR+ guidelines for cross-border ISO 20022 messages.
2. **The clearing and settlement mechanism (CSM).** Moves the *messages* between PSPs and works out who owes whom. The UPI switch; a SEPA CSM such as EBA Clearing's STEP2 or a national ACH; the card network's processing system.
3. **The settlement agent.** Holds the accounts across which the *money* finally moves — almost always the central bank. In India, settlement for UPI and IMPS happens in the PSPs' accounts at the RBI; in the euro area, in TARGET (T2).

In the next part we separate clearing from settlement properly. For now: messages go through the CSM; money moves at the settlement agent; the scheme says how.

## Example 1: a UPI payment on the model

You pay ₹250 to a chai stall using a UPI app linked to your HDFC account; the stall's VPA is with Paytm Payments Bank.

| Corner / middle | Who |
|---|---|
| Payer | You |
| Payer's PSP | HDFC Bank (your account), via your UPI app, which is itself a licensed participant |
| Scheme | NPCI (UPI rulebook) |
| CSM | NPCI's UPI switch (routes the debit and credit messages in real time) |
| Settlement agent | RBI (net positions between HDFC and Paytm Payments Bank settled across their RBI accounts in later cycles) |
| Payee's PSP | Paytm Payments Bank |
| Payee | The chai stall |

The stall sees the money in two seconds. HDFC and Paytm Payments Bank settle with each other later. That gap between message and money is the subject of [part 4](../2026-10-10-04-clearing-vs-settlement/).

## Example 2: a SEPA credit transfer on the model

A German importer pays €40,000 to a Dutch supplier.

| Corner / middle | Who |
|---|---|
| Payer | German importer |
| Payer's PSP | Commerzbank (sends a `pacs.008`) |
| Scheme | European Payments Council — SCT rulebook |
| CSM | EBA Clearing STEP2 (or another SEPA-compliant CSM both banks reach) |
| Settlement agent | Eurosystem's T2, where the CSM's net positions settle |
| Payee's PSP | ING |
| Payee | Dutch supplier |

Same shape, different names. That is the point of the model.

## Three-corner schemes and "on-us" payments

Sometimes two corners collapse into one.

- **Three-corner (closed-loop) schemes.** American Express and Diners traditionally act as both issuer and acquirer: the payer's PSP and the payee's PSP are the same company, so there is no interbank leg and no external scheme. Wallet-to-wallet payments inside a single app (Paytm to Paytm) are the same shape.
- **On-us payments.** Both payer and payee bank with the same institution. The bank simply moves money between two of its own ledgers; no CSM, no settlement agent. Banks love on-us payments because they are free and instant, and a surprising share of domestic volume is on-us at the largest banks. [Part 7](../2026-10-10-07-participation-and-on-us/) comes back to this.

## Why the model matters to a BA

- **Requirements map onto edges.** A customer channel change is a vertical-edge change. A scheme migration (MT to ISO 20022, say) is a horizontal-edge change and touches every participant at once.
- **Messages have a corner of origin.** `pain.*` messages travel on the payer's vertical edge; `pacs.*` on the horizontal edge; `camt.*` reporting flows down the payee's vertical edge (and back to the payer). If you know which edge a problem is on, you know which message family to read. [Part 12](../2026-10-10-12-iso-20022-what-changes/) builds on this.
- **Fees and liabilities attach to corners.** Interchange flows from acquirer to issuer; scheme fees go to the rulebook owner; returns move liability from one PSP to another.

## Next

Messages move in the middle; money moves at the settlement agent, later. Why "later", and what can go wrong in between, is [clearing vs settlement](../2026-10-10-04-clearing-vs-settlement/).

*Part 3 of [How money moves](../2026-10-10-00-how-money-moves-map/). Course pairing: [Module 1](../../course/m1/).*
