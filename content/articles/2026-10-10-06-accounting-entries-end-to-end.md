---
title: The accounting entries behind a payment, end to end
date: 2026-10-10
module: 04 Correspondent banking
series: how-money-moves
order: 6
tags: accounting, nostro, vostro, mirror account, central bank account, double entry
summary: The same ₹1 lakh payment booked three ways — on-us, interbank via the central bank, and cross-border via a correspondent — with every debit and credit shown. If you can read these, you can read any payment investigation.
---

Payments people talk about messages. Finance people talk about entries. The payment is only *done* when both agree, and most investigations are a disagreement between them. This part shows the entries for three versions of the same payment. It builds on [netting and settlement](../2026-10-10-05-netting-liquidity-settlement-risk/) and sets up [correspondent banking](../2026-10-10-09-correspondent-banking-serial-cover/).

## The one rule

A bank's balance sheet has customer deposits on the liability side (the bank owes customers that money) and the bank's own balances at other banks — the central bank, correspondents — on the asset side. Every payment is two entries at every bank it touches: one on a customer or counterparty account, one on the account where the bank's money actually sits.

Debit reduces a liability or increases an asset; credit does the opposite. Hold on to that and the rest is mechanical.

## Case 1: on-us — both customers at the same bank

Priya and Rahul both bank with Bank X. Priya pays Rahul ₹1,00,000.

**Bank X's books**

| Account | Debit | Credit |
|---|---|---|
| Priya's deposit account (liability) | 1,00,000 | |
| Rahul's deposit account (liability) | | 1,00,000 |

That is all. No money leaves Bank X; one liability shrinks, another grows by the same amount. No clearing, no settlement, no scheme fee. This is why banks route internally whenever they can — and why your own bank's "instant transfer to another customer of ours" has always been instant, long before UPI.

## Case 2: interbank, domestic — settled at the central bank

Priya banks with Bank X; Rahul with Bank Y. Priya pays ₹1,00,000 by RTGS (gross, so the entries are one-for-one; with NEFT or UPI the same entries happen, but the central-bank leg is the *net* of many payments at the end of a cycle).

**Bank X (sending)**

| Account | Debit | Credit |
|---|---|---|
| Priya's deposit account (liability) | 1,00,000 | |
| Bank X's settlement account at RBI (asset) | | 1,00,000 |

Bank X owes Priya less, and has less money at the central bank.

**Reserve Bank of India (settlement agent)**

| Account | Debit | Credit |
|---|---|---|
| Bank X's settlement account (liability of RBI) | 1,00,000 | |
| Bank Y's settlement account (liability of RBI) | | 1,00,000 |

For the central bank, the banks' balances are liabilities. It moves ₹1 lakh from X's account to Y's. This single entry *is* settlement.

**Bank Y (receiving)**

| Account | Debit | Credit |
|---|---|---|
| Bank Y's settlement account at RBI (asset) | 1,00,000 | |
| Rahul's deposit account (liability) | | 1,00,000 |

Bank Y has more at the central bank and owes Rahul more.

Notice the pattern: each bank's entry is the mirror of the central bank's entry for it. When they match, everyone reconciles. When Bank Y credits Rahul (because the message arrived) but the RBI leg hasn't happened yet (because settlement is deferred), Bank Y's books show a *receivable* from the system until the cycle closes. That gap is exactly the exposure [part 5](../2026-10-10-05-netting-liquidity-settlement-risk/) described.

## Case 3: cross-border — settled through a correspondent

Priya in Mumbai pays USD 1,200 to Rahul in New York. Bank X (India) has no account at the Federal Reserve, so it keeps a USD account with Citibank New York — its **nostro**. Rahul banks with Chase, which also has a Fed account. Citi settles with Chase through Fedwire or CHIPS.

First, two words from [part 4 of the course](../../course/m4/):

- **Nostro** ("ours"): Bank X's USD account held *at* Citi, as seen from Bank X. On Bank X's books it is an asset.
- **Vostro** ("yours"): the same account as seen from Citi. On Citi's books it is a liability — Citi owes Bank X that money.

One account, two names, depending on whose books you are reading.

**Bank X (Mumbai) — debits Priya, reduces its nostro**

| Account | Debit | Credit |
|---|---|---|
| Priya's deposit account, INR equivalent at the agreed rate (liability) | ₹1,00,800 | |
| **Nostro mirror** — "Our USD account at Citi NY" (asset) | | USD 1,200 |

Bank X cannot see Citi's ledger in real time, so it keeps its own copy of what the nostro balance *should* be. That copy is the **nostro mirror account**. The FX difference between the INR debit and the USD credit goes to a position account (omitted here for clarity).

**Citibank New York — moves money out of Bank X's vostro to the Fed**

| Account | Debit | Credit |
|---|---|---|
| Vostro — "Bank X's USD account with us" (liability) | USD 1,200 | |
| Citi's reserve account at the Federal Reserve (asset) | | USD 1,200 |

**Federal Reserve**

| Account | Debit | Credit |
|---|---|---|
| Citi's reserve account | USD 1,200 | |
| Chase's reserve account | | USD 1,200 |

**Chase — credits Rahul**

| Account | Debit | Credit |
|---|---|---|
| Chase's reserve account at the Fed (asset) | USD 1,200 | |
| Rahul's deposit account (liability) | | USD 1,200 |

Four ledgers, eight entries, one payment. The Swift messages ([part 9](../2026-10-10-09-correspondent-banking-serial-cover/) covers which ones) are what tell each bank to make its pair of entries.

## Where reconciliation breaks

The nostro mirror at Bank X and the vostro at Citi should always agree. Three things make them diverge, and together they fill most of a payments-operations day:

1. **Timing.** Bank X books the mirror entry when it *sends* the instruction; Citi books the vostro when it *executes*, possibly next business day. Value dates exist to line these up.
2. **Charges.** Citi deducts a USD 15 fee from the vostro that Bank X didn't book. The mirror shows 1,200 out; the statement shows 1,215. Charge codes (OUR/SHA/BEN) decide who should have absorbed it.
3. **Returns and repairs.** Chase cannot apply the credit (wrong account number) and sends the money back. Citi credits the vostro; Bank X's mirror still shows it gone until someone processes the return.

The tool for catching all three is the end-of-day statement from the correspondent — MT940/MT950 today, `camt.053` under ISO 20022 — matched line by line against the mirror. Automated nostro reconciliation is one of the quietly huge functions in any bank, and a BA who can read these entries is the person who gets asked to fix it.

## Check yourself

- In case 3, which single account would you look at first if Rahul says he received only USD 1,185?
- If Bank X and Citi were the same bank (Bank X's own New York branch), which entries disappear?

## Next

Case 2 assumed both banks have an account at the central bank. Many don't — fintechs, small banks, foreign branches. How they get in anyway is [part 7: direct and indirect participation, and why on-us payments matter](../2026-10-10-07-participation-and-on-us/).

*Part 6 of [How money moves](../2026-10-10-00-how-money-moves-map/). Course pairing: [Module 4](../../course/m4/).*
