# Prompt Patterns

## Design Rules

A strong prompt for this workflow usually contains:

1. Data boundary
2. Research focus
3. Output type
4. Quality standard
5. Fallback instruction

## 1. Research Prompt

```text
Read the local sample patent PDFs, extracted text files, and any notes in intake/research-notes.
Focus on section order, structural wording, numbering rules, scope granularity, background-problem framing, and figure-description patterns.
Produce a reusable writing guide for this domain in Markdown and make it specific enough to support later AI direction selection.
```

## 2. AI Direction Selection Prompt

```text
Use the local writing guide, sample patent PDFs, extracted text, and any notes in intake/research-notes.
Choose one utility-model patent direction that fits the corpus and the research results.
Provide: final title, target problem, core structural scheme, why it fits the references, likely figures/components, drafting assumptions, and missing information.
Continue directly to drafting after the direction is chosen.
```

## 3. Patent Package Prompt

```text
Use the AI-selected direction, the local writing guide, sample patent PDFs, extracted text, and research notes to produce one complete patent package.
First draft the disclosure. Then generate figure prompts. Then review completeness, figure-text consistency, numbering stability, topic fit, and open questions. Finally revise the disclosure once based on that review.
Output a disclosure draft, figure prompts, review report, and reviewed disclosure.
Do not treat the work as complete until the review pass and revised draft are both finished.
```

## 4. Domain Accelerator Prompt

```text
Build an unfamiliar-domain accelerator page for a non-specialist reviewer based on the selected direction and the reviewed disclosure.
Explain the core structure, working chain, easy-to-confuse parts, and what to manually verify next.
Keep the page useful for later human review rather than formal filing.
```
