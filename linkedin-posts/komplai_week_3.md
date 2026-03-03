# Week 3 Content: The Architecture (Target: CEOs, CFOs, Controllers)
**Theme:** Building the Modern Finance Stack.
**Dates:** Feb 17 - Feb 21

---

## Post 7: The "Trust But Verify" Framework
**Date:** Monday, Feb 17
**Topic:** How to Audit AI Outputs
**Hook angle:** Controversial take that AI vendors don't want you to hear

---

If you blindly trust AI with your books, you deserve what happens next.

I keep seeing the same mistake.

A finance team buys an AI tool.
They feed it their ledger.
It spits out a number.
They put that number in the board deck.

Nobody checks the work.

That's not "adopting AI."
That's outsourcing your judgment to a black box.

Here's what most AI vendors won't tell you:

AI in finance should never operate without a human checkpoint.

Not because the AI is bad.
Because the stakes are too high.

One misclassified revenue line and you're restating earnings.
One wrong FX rate and your consolidation is fiction.

The best teams I work with don't trust OR distrust AI.
They verify it.

Here's the framework I give every Controller I advise:

THE MAKER-CHECKER PROTOCOL

Step 1 → AI drafts (the Maker)
It does the heavy lifting. Categorizes transactions, calculates accruals, consolidates entities. But it shows its work — data source, logic, assumptions.

Step 2 → Human samples (the Checker)
You don't review every line. You review a statistical sample.
Pull 10% of transactions. Check the 5 largest line items. Verify every intercompany elimination.

Step 3 → Approve or reject (the Gate)
Sample passes at 98%+ accuracy? Approve.
Fails? Reject, flag the pattern, retrain.

Grade yourself right now:

A = You have a documented Maker-Checker protocol. You're ahead of 95% of teams.
B = You spot-check, but inconsistently. You're exposed.
C = You review everything line-by-line. You're wasting the AI entirely.
F = You don't check at all. Stop what you're doing and fix this today.

This is the architecture we built into Komplai from Day 1.
Every output ships with an execution plan — what data was used, what logic was applied, what was excluded.

The system wants to be audited.
That's the only way finance teams will trust it.

What's your grade? Drop it below. 👇

---

**Visual concept:** A clean 3-step flow: MAKER → CHECKER → GATE. Green checkmarks on the pass path, red X on the reject path. Minimal, diagrammatic.

---

## Post 8: The "One-Person Finance Team" Org Chart
**Date:** Wednesday, Feb 19
**Topic:** Redesigning Finance Roles for 2026
**Hook angle:** Specific dollar figure that makes the problem tangible

---

You're paying someone $85K a year to copy numbers from one system into another.

Let me explain.

I was talking to a CFO last month. She runs a $40M company.

Her finance team? Three people.

One does AP/AR.
One does month-end close.
One does "everything else."

The "everything else" person?
70% of their time is data entry.

That's $60K/year in pure data janitorial work.

But here's the part that should actually scare you:

When the CEO asks "Should we expand into EMEA?" — nobody on the team has the bandwidth to answer.

They're too busy entering invoices.

This is the org chart I see at almost every growing company:

CFO
→ Controller (close + reporting)
→ AP/AR Specialist (data entry)
→ Staff Accountant (data entry)
→ External Consultant (the only one who knows how things work)

Here's what the 2026 version should look like:

CFO
→ Controller (strategy + oversight)
→ Finance Analyst (insights + decisions)
→ AI System (data entry + consolidation + memory)

Three things changed:

1. The data entry roles aren't eliminated — they're upgraded to analysts.
2. The external consultant is gone. Institutional memory lives in the system.
3. Every human on the team is doing judgment work.

Run this audit on your own team this week:

What % of your team's hours go to data entry, formatting, and manual rec?
What % go to analysis, strategy, and decision support?

If the first number is bigger than the second, your org chart is a decade behind.

The companies I advise aren't replacing their finance teams.
They're upgrading them.

That's the Komplai thesis — make every finance person an analyst, not a data clerk.

What's the data entry vs. analysis split on your team? Be honest. 👇

---

**Visual concept:** Side-by-side org charts. Left side (2015) is cluttered, lots of red "data entry" labels. Right side (2026) is clean, green, with "strategy" and "judgment" labels. Simple and shareable.

---

## Post 9: The "Data Entry" Waste Calculator
**Date:** Friday, Feb 21
**Topic:** Quantifying the Cost of Manual Work
**Hook angle:** A specific, uncomfortable dollar figure

---

I ran the numbers on what manual data entry actually costs a finance team.

It's worse than you think.

Here's the formula:

Annual waste = (salary) x (% time on manual tasks) x (headcount)

I ran it on a typical 4-person finance team:

Staff Accountant — $75K salary, 80% manual → $60,000 wasted
AP Specialist — $65K salary, 75% manual → $48,750 wasted
Controller — $120K salary, 40% manual → $48,000 wasted
Finance Manager — $95K salary, 50% manual → $47,500 wasted

Total: $204,000 per year.

On work that produces zero strategic value.

And nobody tracks it. Because it's hidden inside salaries.

But the money isn't even the worst part.

It's the opportunity cost.

Those 2,000+ hours a year of manual work?

That's 2,000 hours your team could spend on:
→ Cash flow forecasting that actually prevents a crisis
→ Vendor analysis that saves $50K in renegotiated contracts
→ Board-ready insights that help close your next fundraise

Here's a 2-minute audit you can do right now:

Open a spreadsheet.
List every person on your finance team.
For each person, estimate hours per week on data entry vs. hours on analysis.
Multiply the data entry hours by their hourly rate.
Annualize it.

That's your waste number.

The goal isn't zero manual work. Some tasks need human judgment.

The goal is to flip the ratio: 80% strategic, 20% manual.

That's the benchmark the best finance teams are targeting.
And it's exactly what we're building Komplai to deliver.

Run the calculator on your team. What's your number?

I'm guessing it's north of $150K. 👇

---

**Visual concept:** A receipt/calculator visual. Line items showing each role's "waste" amount. Bold total at the bottom: "$204,250." Red "BURIED COST" stamp across it.

---

## LinkedIn Algorithm Notes (Internal)

**Formatting rules applied:**
- No markdown bold, headers, or tables (LinkedIn doesn't render them)
- One thought per line for mobile readability and dwell time
- Hook lands in first 2-3 lines (above the "...see more" fold)
- Arrows (→) used instead of bullet points for visual variety
- Posts kept under ~1,800 characters where possible
- No external links in post body (kills reach — put in first comment)
- CTA asks a specific question to drive comments
- Each post is self-contained (no "as I posted last week" dependency beyond Post 9's natural callback)

**Posting tips:**
- Post between 7-9 AM local time for your target audience (US East Coast for CFOs)
- Reply to every comment within the first hour
- Drop the Komplai link in the first comment, not the post body
- If using images, upload natively (don't use link previews)
