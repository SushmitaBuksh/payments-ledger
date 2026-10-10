---
title: Clearing vs settlement — the two words you have to get right first
date: 2026-10-10
module: 01 Intro
series: how-money-moves
order: 4
slug: 2026-10-10-04-clearing-vs-settlement
tags: fundamentals, clearing, settlement, UPI, cheques
summary: Why a cheque takes two days and a UPI payment takes two seconds, explained with the two concepts that underpin every payment system.
---

Almost every confusing conversation I've had about payments came down to two words being used loosely: **clearing** and **settlement**. Get these straight and the rest of the domain starts to make sense. In the [four-corner model](../2026-10-10-03-four-corner-model-parties/) from part 3, clearing happens in the middle (the CSM) and settlement happens at the settlement agent.

## The simple version

- **Clearing** is the exchange of *information*: who is paying whom, how much, from which account to which. It includes checking that the instruction is valid and working out what each bank owes the others.
- **Settlement** is the movement of *money* between banks to discharge those obligations — usually across accounts the banks hold at the central bank.

A payment instruction can be cleared long before it is settled. And from a customer's point of view, "the money arrived" often means the beneficiary bank chose to credit the account *before* settlement, because it trusts the system to settle later.

## Gross vs net

Settlement can happen in two ways.

| | Gross | Net |
|---|---|---|
| How | Each payment settles individually, in full | Payments are totalled up and only the net difference between banks settles |
| When | Immediately, one by one (real time) | At fixed times, in batches |
| Risk | Low — nothing is owed between settlements | Higher — banks owe each other until the batch settles |
| Liquidity needed | High | Low |
| Example | RTGS | NEFT, cheque clearing |

The trade-off is the heart of payment-system design: gross settlement is safe but needs a lot of liquidity sitting idle; net settlement is efficient but creates exposure between banks until the batch settles. [Part 5](../2026-10-10-05-netting-liquidity-settlement-risk/) puts numbers on exactly how much liquidity netting saves and what the exposure costs.

## Four payments, side by side

**Cheque.** The paper (or its image) goes to a clearing house. Clearing: the banks exchange cheque details and the clearing house computes net positions. Settlement: the net amounts settle across central-bank accounts at the end of the cycle. Add the time for the cheque to physically reach the bank and the fraud checks on it, and you get one to two days.

**NEFT.** Electronic, but still *batched*. Instructions are collected, netted, and settled in half-hourly batches. Near-instant from the customer's view most of the time, but structurally a net system.

**RTGS.** Each payment settles individually and finally across central-bank accounts, in real time. Used for large values because the finality matters more than the liquidity cost.

**UPI.** Instant for the customer, but here's the subtle part: the *message* clears in real time and the beneficiary bank credits the account immediately, while the inter-bank *settlement* happens later in batches through the scheme operator. The two seconds you experience are clearing plus a bank's willingness to credit ahead of settlement. The risk in between is managed by limits and guarantees.

## Why this matters for a BA

When a stakeholder says "the payment is done," ask: do you mean the instruction was accepted, cleared, the beneficiary was credited, or the banks have settled? Those are four different points in time, four different system states, and four different things that can go wrong. Most "where is my money" investigations are a mismatch between which of these the customer assumed and which actually happened.

## Next

Netting sounds like an accounting trick. It is actually the reason most of the world's payments are affordable — and the reason a bank failure in 1974 still shapes how settlement works. [Part 5: netting, liquidity and settlement risk, with numbers](../2026-10-10-05-netting-liquidity-settlement-risk/).

*Part 4 of [How money moves](../2026-10-10-00-how-money-moves-map/). Course pairing: [Module 1](../../course/m1/).*
