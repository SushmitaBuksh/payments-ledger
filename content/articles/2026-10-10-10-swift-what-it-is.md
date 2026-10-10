---
title: Swift — what it is, what it isn't, and the five things it actually gives you
date: 2026-10-10
module: 03 Swift & gpi
series: how-money-moves
order: 10
tags: swift, FIN, FINplus, RMA, BIC, gpi, UETR
summary: Swift moves messages, not money. The cooperative, the network, the standards and the services untangled, with the five pieces every payments BA should be able to explain — BIC, RMA, FIN/FINplus, gpi and the UETR.
---

Ask ten people what Swift is and you'll get "the international payment system". It isn't one. Swift has never held or moved a single dollar. Understanding what it *does* do is the difference between reading a payments incident correctly and chasing the wrong team. This part follows naturally from the correspondent chains in [part 9](../2026-10-10-09-correspondent-banking-serial-cover/).

## One organisation, four hats

**1. A cooperative.** The Society for Worldwide Interbank Financial Telecommunication was founded in 1973 by 239 banks, is headquartered in Belgium, and is owned by its member institutions. It is overseen by the G10 central banks with the National Bank of Belgium as lead. That ownership structure is why Swift is cautious, consensus-driven and slow to change — and why, when governments want to cut a country's banks off, Swift is the lever they pull.

**2. A network.** SwiftNet is a private, highly secure messaging network connecting over 11,000 institutions in 200-plus countries. It guarantees that a message sent by Bank A is delivered, unaltered, exactly once, to Bank B, with a verifiable audit trail. That is all. The money moves afterwards, by the nostro/vostro entries in [part 6](../2026-10-10-06-accounting-entries-end-to-end/), because the message told the banks to make them.

**3. A standards body.** Swift wrote the MT message standards used since the 1970s, and today it maintains the ISO 20022 usage guidelines for cross-border payments (CBPR+) together with the industry. It is also the registration authority for the BIC standard (ISO 9362) and runs the ISO 20022 registration authority on behalf of ISO.

**4. A services company.** On top of the network it sells gpi, sanctions-screening utilities, KYC registries, reference data (SwiftRef), the Case Management service for investigations, and more.

When someone says "Swift is down" they mean the network. When they say "Swift changed the format" they mean the standards. When they say "Swift kicked X out" they mean the cooperative. Keep the hats separate.

## The five things to be able to explain

### BIC — the address

A **Business Identifier Code** (ISO 9362) names an institution on the network. Eight or eleven characters:

```
C I T I  I N  B X  X X X
└bank┘  └ctry┘└loc┘└branch┘
```

- 4 letters: institution (CITI)
- 2 letters: country (IN)
- 2 characters: location (BX = Mumbai)
- 3 optional characters: branch (XXX = head office)

`DEUTDEFF500` is Deutsche Bank, Germany, Frankfurt, branch 500. People say "SWIFT code" and mean BIC. A BIC identifies a *bank*; an IBAN (where used) identifies an *account*. India does not use IBAN, which is why Indian payments carry account number plus IFSC domestically and account number plus BIC internationally.

### RMA — the permission

Any two institutions can both be on SwiftNet without being allowed to message each other. The **Relationship Management Application** is the mutual authorisation: Bank A grants Bank B permission to send it certain message types, and vice versa. No RMA, no message — the network rejects it. This is a fraud and compliance control (you cannot be sent payment instructions by a bank you have never vetted) and it is why onboarding a new correspondent takes weeks. In [part 9's](../2026-10-10-09-correspondent-banking-serial-cover/) cover method, Banco Sul could send the announcement directly to Bank of Baroda only because an RMA existed between them.

### FIN and FINplus — the services

**FIN** is the classic store-and-forward messaging service that carried MT messages for decades. **FINplus** is the equivalent service for ISO 20022 (MX) messages. The messages themselves are covered in [part 12](../2026-10-10-12-iso-20022-what-changes/); the thing to know here is that during the 2022–2025 coexistence period banks ran both, and that since November 2025 cross-border payment instructions travel on FINplus. If a message is referred to as "an MX on FINplus" versus "an MT on FIN", that is what it means.

### gpi — the service level

By the mid-2010s, correspondent banking had a reputation problem: slow, opaque, unpredictable fees. **Swift gpi (global payments innovation)**, launched in 2017, is a set of rules banks sign up to — same-day use of funds, fee and FX transparency, end-to-end tracking, unaltered remittance information — plus the infrastructure to enforce them. The key piece is the **Tracker**, a central database where every bank in a chain reports the status of a payment as it handles it, so the sending bank (and its customer) can see where the money is. Most large banks are gpi members; Swift reports that roughly half of gpi payments are credited within 30 minutes and almost all within 24 hours.

### UETR — the tracking number

None of that tracking works unless every message about a payment carries the same reference. The **Unique End-to-end Transaction Reference** is a 36-character identifier (a UUID, e.g. `eb6305c9-1f7f-49de-aed0-16487c27b42d`) generated by the first bank and copied, unchanged, into every subsequent message — the announcement, the cover, status reports, returns and investigations. Since November 2018 it is mandatory on all payment instructions, gpi member or not; a message without one is rejected by the network. When you are asked "where is this payment?", the UETR is the first thing you ask for and the only thing you need.

## What Swift doesn't do

- **It doesn't settle.** No accounts, no money. Settlement happens at central banks and correspondents.
- **It isn't the only network.** Domestic schemes (UPI, SEPA CSMs, Fedwire) have their own networks and many use ISO 20022 without touching Swift. Some countries run alternative cross-border messaging systems (Russia's SPFS, China's CIPS has its own messaging for RMB).
- **It doesn't decide fees or FX.** Those are between the banks. gpi makes them *visible*; it doesn't set them.

## Where this leaves you

You can now read a cross-border payment properly: a `pacs.008` on FINplus, from a BIC to a BIC under an RMA, carrying a UETR you can look up in the gpi Tracker, instructing nostro/vostro entries that settle the money. The next part turns to a region where the rail *is* standardised end to end — [SEPA](../2026-10-10-11-sepa-sct-inst-direct-debit/) — before [part 12](../2026-10-10-12-iso-20022-what-changes/) explains the message standard underneath all of it.

*Part 10 of [How money moves](../2026-10-10-00-how-money-moves-map/). Course pairing: [Module 3](../../course/m3/) and [Module 5](../../course/m5/).*
