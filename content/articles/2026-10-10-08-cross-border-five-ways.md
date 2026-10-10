---
title: Cross-border payments — the five ways money crosses a border
date: 2026-10-10
module: 04 Correspondent banking
series: how-money-moves
order: 8
tags: cross-border, correspondent banking, UPI-PayNow, remittance, closed loop, stablecoins
summary: Why there is no "international UPI", and the five models that fill the gap — correspondent banking, interlinked domestic systems, closed-loop networks, card schemes and tokenised money — compared on one ₹1 lakh remittance.
---

Inside a country, a payment system has one currency, one central bank and one rulebook. Cross a border and all three change. There is no global central bank to settle across, so the industry has built five different workarounds. This part compares them; [part 9](../2026-10-10-09-correspondent-banking-serial-cover/) goes deep on the oldest and biggest.

## The problem in one sentence

Money never actually *leaves* a country. Rupees exist only as balances in Indian bank accounts (and ultimately at the RBI); euros only in euro-area accounts. "Sending rupees to Germany" really means: reduce a rupee balance in India, increase a euro balance in Germany, and have two institutions agree on how the difference is squared. Every model below is a different answer to *who* those two institutions are and *how* they square up.

## One payment, five routes

Meena in Pune sends roughly ₹1,00,000 (about €1,050 at today's rate) to her son Arjun studying in Berlin.

### 1. Correspondent banking

Meena's bank debits her INR. It has a EUR account (a nostro, see [part 6](../2026-10-10-06-accounting-entries-end-to-end/)) with a German or large international bank. It instructs that correspondent, by Swift message, to pay Arjun's bank. If Arjun's bank is small, the correspondent may need its *own* correspondent — chains of two to four banks are normal.

- **Reach:** anywhere a chain exists, which is nearly everywhere.
- **Speed:** hours to a few days, depending on chain length, cut-offs and time zones. Swift gpi now credits most payments within minutes to hours, but the slow tail is long.
- **Cost:** each bank in the chain may deduct a fee; FX margin at the first bank; typically 3–6% for a retail remittance of this size, less for corporates.
- **Transparency:** historically poor — hence gpi's tracker and the UETR.
- **Who settles with whom:** each adjacent pair, across nostro/vostro accounts, by the entries in [part 6, case 3](../2026-10-10-06-accounting-entries-end-to-end/).

### 2. Interlinked domestic instant systems

Two countries connect their fast payment systems so a payment hops directly from one to the other. **UPI–PayNow** (India–Singapore, live since February 2023) is the standard example; the Bank for International Settlements' Project Nexus aims to generalise it across several Asian systems. Arjun would need to be in a linked country, so this route doesn't exist for Germany yet — but it shows where things are heading.

- **Reach:** only linked corridors (small today, growing).
- **Speed:** seconds.
- **Cost:** low, often regulated.
- **How it settles:** a sponsor bank on each side holds the other currency; the operators net between them. It is correspondent banking with the correspondent step automated and the FX pre-agreed.

### 3. Closed-loop networks

Wise, PayPal, Remitly, Western Union and similar providers do not move money across the border at all. They hold a pool of INR in India and a pool of EUR in Germany. Meena pays INR into the Indian pool (by UPI or bank transfer — a *domestic* payment); the provider pays Arjun from the German pool (another domestic payment, by SEPA). The provider rebalances its pools periodically through the correspondent system in bulk.

- **Reach:** wherever the provider has pools and licences.
- **Speed:** minutes to hours, because both legs are fast domestic payments.
- **Cost:** low and visible — typically 0.5–2% including FX.
- **Catch:** both ends must be where the provider operates, and the provider carries the FX and liquidity risk of its pools. This is also a three-corner model from [part 3](../2026-10-10-03-four-corner-model-parties/).

### 4. Card schemes

Meena could give Arjun a supplementary credit card, or Arjun could pay his rent with an Indian card. Visa and Mastercard are global four-corner schemes with built-in FX: the issuer in India settles with the scheme in INR (or USD), the scheme settles with the German acquirer in EUR.

- **Reach:** anywhere cards are accepted.
- **Speed:** authorisation instant, settlement a few days.
- **Cost:** FX markup of 2–3.5% plus any cross-border fees, borne by the cardholder and merchant.
- **Catch:** it is a payment *for goods*, not a transfer to a person; and it is a pull ([part 2](../2026-10-10-02-push-vs-pull-payments/)) with chargeback rights.

### 5. Tokenised money: stablecoins and CBDC pilots

Meena buys a USD stablecoin, sends the token to Arjun's wallet, and Arjun sells it for euros. The transfer itself is near-instant and borderless because the token lives on a shared ledger rather than in two national banking systems. The borders reappear at the on- and off-ramps, where tokens are exchanged for bank money under local regulation. Central banks are running wholesale CBDC experiments (BIS Project mBridge, among others) that apply the same idea to interbank settlement.

- **Reach:** wherever on/off-ramps exist and are legal; India's rules on crypto assets are restrictive.
- **Speed:** minutes.
- **Cost:** low on-chain, but ramp spreads and compliance costs vary widely.
- **Catch:** regulatory uncertainty, consumer protection, and the fact that the hard part (converting to and from local bank money) is still done by regulated intermediaries.

## Side by side

| Route | Reach | Speed | Typical cost | Transparency | Where the FX happens |
|---|---|---|---|---|---|
| Correspondent banking | Global | Hours–days | High | Improving (gpi) | Sending bank or correspondent |
| Linked instant systems | Few corridors | Seconds | Low | High | Pre-agreed by operators |
| Closed-loop providers | Provider footprint | Minutes–hours | Low | High | Provider |
| Card schemes | Global merchants | Instant auth, slow settlement | Medium | Medium | Scheme/issuer |
| Tokenised money | Ramp-dependent | Minutes | Low–variable | High on-chain | At the ramps |

## Why correspondent banking still dominates

Given the table, why does most cross-border *value* still move through correspondents? Three reasons: it is the only route with universal reach; it is the only one built for large corporate and interbank amounts; and every other route ultimately uses it to rebalance. The G20's cross-border payments programme is largely an effort to make this route faster, cheaper and more transparent rather than replace it — and ISO 20022's richer data ([part 12](../2026-10-10-12-iso-20022-what-changes/)) is a big part of that.

## Next

Time to open the box. [Part 9: correspondent banking in detail — serial vs cover payments, charges, and the messages that carry them](../2026-10-10-09-correspondent-banking-serial-cover/).

*Part 8 of [How money moves](../2026-10-10-00-how-money-moves-map/). Course pairing: [Module 4](../../course/m4/).*
