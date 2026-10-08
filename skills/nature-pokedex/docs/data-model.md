# Portable data model

The field inventory and invariants are in `spec/domain-contract.json`. These are
semantic requirements, not a selected wire format, ORM mapping or database DDL.
Internal identifier types and matching algorithms remain implementation decisions.

`Taxon` holds a confirmed canonical identity at an explicit defensible rank,
aliases, supported lineage, a browsing Life Group and stable knowledge. Display
name alone does not establish identity. Preserve useful earlier names as aliases.
The minimum rank vocabulary includes species, genus, subgenus, subfamily and
family; additional ranks require an explicit contract extension rather than guesses.

`Encounter` holds one event, its independent Event Key, optional canonical relation,
provisional candidate, confidence/basis, time, broad location, optional count,
evidence, field marks, behaviour and owner commentary. A confirmed broader taxon
can coexist with a narrower provisional ID. Corrections preserve event identity
and useful history, and may reduce confidence or change the canonical link.

Named breed/variety confidence is independent of taxon confidence and absent when
there is no named candidate. Phenotype is descriptive evidence, not pedigree or
canonical identity. Memorable is owner-marked significance; unmarked is not a
negative judgment. Never invent its explanation or normalize away owner wording.

`MediaAsset` identifies bytes by SHA-256; encounter/media associations permit reuse.
Filenames and raw source references live in provenance associations, allowing
multiple names for one digest. A digest match does not prove event identity.
Evidence may exist without a digest or stored binary. A showcase selection is a
separate owner choice. Missing media, date, count or location does not invalidate
an otherwise supported encounter.

`TaxonRating` owns four nullable integer inputs, model version, assessment date,
per-axis rationale, evidence/reference support, uncertainty, representative-estimate
flag and optional owner tier override. Computed score/tier are derived. A broad
rank can be rated using supported representative traits. Capture reads the current
linked rating and never creates an encounter-time score copy.

## Evidence-derived collection state

Canonical `Photo` means owner-supplied or owner-produced encounter photography.
It is not a generic image-kind label. Third-party or unattributed identification
images remain identification inputs outside the persisted Photo claim. Personal
visual encounter and storage remain independent of owner-photo attribution.

- Seen requires supported personal visual encounter evidence. Photo/Video alone
  is insufficient; heard-only and tracks/sign are insufficient.
- Photographed requires an owner-supplied personal encounter photograph, even
  when digest, binary or upload is absent.
- Confirmed requires an encounter supporting the linked taxon at its actual rank;
  confirmed audio-only encounters can remain unseen and unphotographed.
- First Seen means the earliest supported owner encounter date, including
  nonvisual events. Undated history makes this the earliest *known dated* event,
  not a proven lifetime first. Recompute both affected taxa after relinks.

## Time and unresolved policies

Preserve unknown, date-only and offset-aware instant values as distinct variants.
Do not convert dates to midnight, use import timestamps as observation dates or
guess historical zones. Preserve supplied offsets/zones with true instants.
Naive datetime handling, mixed precision ordering and any business timezone are
explicit open policies. Historical timestamps must not be reinterpreted by a new
representation. No import or production migration is implied.

## If storage is ever built

Keep separate Taxon, TaxonRating, Encounter, MediaAsset, EncounterMedia, evidence,
identification-basis and provenance records. Enforce unique Event Keys and digest
identities, foreign keys and relevant checks in the database, and use explicit
migrations. Notion field names, stored-score workarounds and rollups are adapter
concerns, not part of the model.
