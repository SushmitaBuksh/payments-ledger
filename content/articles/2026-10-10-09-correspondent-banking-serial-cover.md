---
title: Correspondent banking in detail — serial vs cover payments, charges and the messages
date: 2026-10-10
module: 06 Serial & cover
series: how-money-moves
order: 9
tags: correspondent banking, serial payment, cover payment, MT103, MT202 COV, pacs.008, pacs.009, OUR SHA BEN
summary: One USD 50,000 payment traced through a three-bank chain two ways — serial and cover — with the exact messages each bank sends, the nostro entries, and a worked example of OUR, SHA and BEN charges.
---

[Part 8](../2026-10-10-08-cross-border-five-ways/) explained why correspondent banking is the backbone of cross-border payments. This part opens it up. By the end you should be able to draw a payment chain, name every message on it, and tell a stakeholder exactly why the beneficiary received USD 49,975 instead of 50,000.

## The cast

An Indian exporter's customer in Brazil is paying for goods. Simplify to the relevant banks:

- **Banco Sul** (Brazil) — the payer's bank. No USD account in New York of its own.
- **Citibank NY** — Banco Sul's USD correspondent. Banco Sul holds a nostro here.
- **JPMorgan NY** — the correspondent of the beneficiary's bank.
- **Bank of Baroda** (India) — the beneficiary's bank, holding a USD nostro at JPMorgan.
- **The exporter** — the beneficiary, with a USD account at Bank of Baroda.

Amount: USD 50,000. Two New York banks have to pass the money between them through Fedwire or CHIPS, because that is where US dollars settle.

## The two message families

Swift carries two kinds of payment message:

- **Customer transfer** — carries the full story: who is paying, who is being paid, why. MT103 in the old format; `pacs.008` in ISO 20022.
- **Financial-institution transfer** — bank-to-bank, moving money to cover something. MT202 (and MT202 COV for the cover variant); `pacs.009` (and `pacs.009 COV`).

Since 22 November 2025, cross-border payment instructions on Swift are ISO 20022 (`pacs.*`); MT103/202 are no longer accepted for them. I give both names because core-banking systems, archives and colleagues still speak MT.

## Method 1: serial payment

The customer transfer itself hops from bank to bank. Each bank receives it, books it, and sends a *new* customer transfer to the next bank.

```
Banco Sul ──pacs.008──▶ Citi NY ──pacs.008──▶ JPMorgan NY ──pacs.008──▶ Bank of Baroda ──▶ Exporter
```

What each bank does:

1. **Banco Sul** debits the payer, credits its nostro mirror for Citi, sends `pacs.008` to Citi. In the message: debtor = payer, creditor = exporter, creditor agent = Bank of Baroda, and an instruction to route via JPMorgan.
2. **Citi NY** debits Banco Sul's vostro, pays JPMorgan USD 50,000 over Fedwire/CHIPS, and forwards a `pacs.008` to JPMorgan with the same debtor and creditor details.
3. **JPMorgan NY** receives the funds, credits Bank of Baroda's vostro, forwards `pacs.008` to Bank of Baroda.
4. **Bank of Baroda** debits its JPMorgan nostro mirror, credits the exporter.

Properties of serial: every bank sees the full payment details (good for sanctions screening), every bank processes a customer payment (slower, more fees), and the payment moves strictly in sequence.

## Method 2: cover payment

The customer transfer goes *directly* to the beneficiary's bank, telling it what is coming. Separately, the money travels through the correspondents as a bank-to-bank transfer that "covers" it.

```
Announcement:  Banco Sul ──────────── pacs.008 ───────────────────▶ Bank of Baroda
Cover (money): Banco Sul ──pacs.009 COV──▶ Citi NY ──Fedwire/CHIPS──▶ JPMorgan NY ──credit advice──▶ Bank of Baroda
```

1. **Banco Sul** sends `pacs.008` straight to Bank of Baroda (they have a Swift relationship — an RMA — even though no account), and sends `pacs.009 COV` to Citi saying "pay USD 50,000 to JPMorgan for account of Bank of Baroda, to cover payment reference X".
2. **Citi NY** debits Banco Sul's vostro, pays JPMorgan.
3. **JPMorgan NY** credits Bank of Baroda's vostro and advises it (`camt.054` credit notification, formerly MT910).
4. **Bank of Baroda** matches the credit advice against the `pacs.008` it received earlier — same reference, same amount — and only then credits the exporter.

Properties of cover: faster (the announcement arrives immediately and the cover moves in a single interbank hop), cheaper (correspondents handle a bank transfer, not a customer payment), but the beneficiary's bank must *wait for and match the cover* before releasing funds. Unmatched covers and covers-without-announcement are a classic investigations queue.

### The screening problem that created MT202 COV

Before 2009, the cover leg was a plain MT202 carrying only bank names. A correspondent in New York screening for sanctions saw "Banco Sul pays Bank of Baroda" and nothing about the underlying customers. Regulators objected; Swift introduced **MT202 COV**, which carries the originator and beneficiary details inside the cover message so every bank in the chain can screen them. ISO 20022 keeps this as `pacs.009 COV`, with the underlying customer data in a dedicated block. If anyone asks why there are two versions of a bank-to-bank message, that is the reason.

## Charges: OUR, SHA, BEN with numbers

Every bank in the chain may charge. The payer chooses, in the instruction, who bears which charges. Assume Citi charges USD 15 and JPMorgan USD 10 for handling, and Bank of Baroda charges nothing for incoming.

| Charge option | Meaning | Payer is debited | Beneficiary receives | Where the 25 went |
|---|---|---|---|---|
| **OUR** (`DEBT` in ISO) | Payer pays all charges | 50,000 + charges claimed by correspondents (often pre-agreed, e.g. 50,025 or a flat "OUR fee") | **50,000** | Billed back to Banco Sul, who charged the payer |
| **SHA** (`SHAR`) | Payer pays their own bank's fees; beneficiary pays the rest | 50,000 (+ Banco Sul's own fee) | **49,975** | Deducted from the amount by Citi and JPMorgan |
| **BEN** (`CRED`) | Beneficiary pays everything, including the sender's fee | 50,000 | **49,975 minus Banco Sul's fee**, e.g. 49,950 | All deducted from the amount |

Three practical notes:

- **SHA is the default** in SEPA and the most common choice internationally. Under SEPA, the payer's and payee's banks charge their own customers separately and the full amount must arrive — intermediaries do not deduct.
- **OUR does not guarantee full value in practice.** A correspondent further down the chain may still deduct if it never agreed to bill the sender. The result is the single most common cross-border complaint: "I chose OUR and they still got less." Swift gpi's fee transparency was designed to expose exactly where deductions happen.
- **The charge code travels in the message** (`ChrgBr` element in `pacs.008`; field 71A in MT103), so every bank in the chain can see the instruction. Whether they honour it is a matter of agreement.

## Reading the chain from a message

A `pacs.008` names the parties with specific roles. Mapping them to our example:

| ISO 20022 element | MT103 field | In the example |
|---|---|---|
| `Dbtr` (debtor) | 50 | Brazilian payer |
| `DbtrAgt` (debtor agent) | 52 | Banco Sul |
| `InstgAgt` / `InstdAgt` | header | The sending and receiving bank *of this particular message* — changes at every hop |
| `IntrmyAgt1` (intermediary agent) | 56 | Citi NY, when Banco Sul tells Bank of Baroda the route |
| `CdtrAgt` (creditor agent) | 57 | Bank of Baroda |
| `Cdtr` (creditor) | 59 | The exporter |
| `ChrgBr` | 71A | SHA / OUR / BEN |
| `UETR` | 121 (block 3) | The one reference that stays the same across every hop |

When something goes wrong, the UETR is what you search for first; it is the thread that ties the announcement, the cover, the credit advice and the tracker status together. [Part 10](../2026-10-10-10-swift-what-it-is/) explains where it came from.

## Check yourself

- In the cover method, what does Bank of Baroda do if the `pacs.008` arrives but no cover credit appears within a day?
- Why would a sanctions team prefer serial payments, and why does the business prefer cover?
- Payer selects OUR; beneficiary receives 49,990. Which bank most likely deducted, and how would you prove it?

*Part 9 of [How money moves](../2026-10-10-00-how-money-moves-map/). Course pairing: [Module 4](../../course/m4/), [Module 5](../../course/m5/) and [Module 6](../../course/m6/).*
