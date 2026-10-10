---
title: Payment instruments — the six ways money actually moves
date: 2026-10-10
module: 01 Intro
series: how-money-moves
order: 1
tags: fundamentals, instruments, credit transfer, direct debit, cards
summary: Cash, cheque, credit transfer, direct debit, card and wallet — what each instrument really is, who starts it, and why the difference decides everything downstream.
---

Every payment you will ever analyse starts with an **instrument**: the agreed form in which a payer tells someone to move money. Get the instrument right and you can predict most of what follows — who bears the risk, how fast it settles, how it can be reversed. This article is the ground floor of the [How money moves](../2026-10-10-00-how-money-moves-map/) series.

## One rent payment, six ways

Imagine you owe your landlord ₹30,000 on the 1st of the month. Here is the same debt paid with each instrument.

| Instrument | What you do | Who starts the movement | Money leaves your account |
|---|---|---|---|
| **Cash** | Hand over notes | You (physically) | Instantly, with no record |
| **Cheque** | Write a paper order to your bank | You write it, landlord presents it | When the cheque clears, 1–2 days after presentation |
| **Credit transfer** (NEFT, RTGS, IMPS, UPI pay) | Instruct your bank to send ₹30,000 to the landlord's account | You ("push") | Immediately or at the next batch |
| **Direct debit** (NACH / e-mandate, SEPA DD) | Sign a mandate once; landlord's bank pulls each month | Landlord ("pull") | On the collection date |
| **Card** | Tap or type card details on a rent-payment app | Landlord's acquirer requests authorisation; your bank approves | Authorised instantly, settled 1–3 days later |
| **Wallet / stored value** | Pay from a prepaid balance (PPI) | You, but the money already left your bank when you topped up | Already gone |

Six instruments, one debt. Notice what varies: *who* initiates, *when* funds leave, and *how* the thing could be undone.

## The two families that matter most

Most of the domain reduces to two instruments: **credit transfers** and **direct debits**. Cards are a special case we return to later; cash and cheques are declining; wallets are usually a credit transfer in disguise.

**Credit transfer.** The payer instructs their own bank. The bank already holds the payer's money and knows the payer, so the instruction is trustworthy the moment it is authenticated. That is why credit transfers can be instant (UPI, IMPS, SCT Inst, FedNow) and why they are hard to reverse: the payer meant it.

**Direct debit.** The payee instructs *their* bank to collect from the payer, on the strength of a mandate signed earlier. The payer's bank is being asked to release money on someone else's say-so. That is why direct debits need mandate management, why they carry refund rights, and why they are never instant.

If you remember one sentence from this article: **the party who initiates the payment is the party the system has to protect against.** Push payments protect the payee from non-payment; pull payments protect the payer from wrongful collection.

## Why a BA should care

When a stakeholder asks for "a payment feature", the first question is which instrument. The answer decides:

- **The message set.** Credit transfers travel as `pain.001` → `pacs.008` (or MT101 → MT103); direct debits as `pain.008` → `pacs.003`. Different schemas, different validations.
- **The exception model.** A failed credit transfer is a reject or a [return](../2026-10-10-11-sepa-sct-inst-direct-debit/); a failed direct debit adds refunds and mandate-related R-transactions.
- **The fraud surface.** Push payments suffer from authorised push payment (APP) fraud, where the payer is tricked into sending; pull payments suffer from unauthorised collections.
- **The customer promise.** "Instant" is a credit-transfer promise. Nobody promises an instant direct debit.

## What the instrument does not tell you

An instrument says *what kind of order* was given. It does not say *which pipe* the order travels through. A credit transfer in India might ride NEFT, RTGS, IMPS or UPI; in Europe, SCT or SCT Inst; across borders, a Swift correspondent chain. The pipe is the **rail** (or scheme, or system), and the next three articles are about those pipes: first [who starts the payment and why that matters](../2026-10-10-02-push-vs-pull-payments/), then [the four-corner model](../2026-10-10-03-four-corner-model-parties/) that every rail is built on.

## Check yourself

- A salary payment, an EMI, a Netflix subscription, a UPI "collect request". Which instrument is each? (Hint: the Netflix one depends on whether you gave a card or a mandate.)
- Why can a bank safely make a credit transfer instant but not a direct debit?

*This is part 1 of the series. The course module that pairs with it is [Module 1: Introduction to payments](../../course/m1/).*
