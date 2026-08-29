from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WATCHLISTS_MODULE = ROOT / "scripts" / "ssot_watchlists.py"
MERGE_GATE = ROOT / "scripts" / "check_merge_gate.py"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_watchlists_no_third_copy() -> None:
    lists = load_module(WATCHLISTS_MODULE, "ssot_watchlists")
    gate = load_module(MERGE_GATE, "check_merge_gate")
    loaded = gate.load_watchlists()
    if loaded != lists.WATCHLISTS:
        fail("check_merge_gate.load_watchlists() diverged from ssot_watchlists.WATCHLISTS")
    ok("check_merge_gate imports ssot_watchlists.WATCHLISTS")


def test_ssot_mapping() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    watchlists = gate.load_watchlists()

    cases = {
        "docs/INTERFACES.md": {"api"},
        "docs/contracts/contract-billing.md": {"api"},
        ".github/workflows/ci.yml": {"prd", "adr"},
        "docs/PRD.md": {"prd"},
        "adrs/adr-02-stack.md": {"adr"},
        "service/app/handlers.py": set(),
        "surface/src/lib/x.ts": set(),
    }
    for rel, expected in cases.items():
        actual = set(gate.ssots_for(rel, watchlists))
        if actual != expected:
            fail(f"ssots_for({rel!r}) = {actual}, expected {expected}")
    ok(f"SSOT mapping matches {len(cases)} fixture files")


def test_required_ssots_groups_by_file() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    watchlists = gate.load_watchlists()
    required = gate.required_ssots(
        ["docs/INTERFACES.md", "docs/contracts/contract-billing.md", "surface/src/lib/x.ts"],
        watchlists,
    )
    if "api" not in required:
        fail(f"expected api in required SSOTs, got {required}")
    if set(required["api"]) != {"docs/INTERFACES.md", "docs/contracts/contract-billing.md"}:
        fail(f"unexpected file grouping for api: {required['api']}")
    ok("required_ssots groups triggering files per SSOT")


def test_verdict_parsing_pass() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    body = "Some PR description.\n\nPlan-Verdict: api: pass\n"
    recorded = gate.recorded_verdicts(body)
    if "api" not in recorded:
        fail(f"expected api recorded, got {recorded}")
    ok("a Plan-Verdict pass line is recorded")


def test_verdict_parsing_accepts_status_vocabulary() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    for status in ("pass", "clear", "compliant", "valid", "ok", "drift"):
        body = f"Plan-Verdict: adr: {status}\n"
        if "adr" not in gate.recorded_verdicts(body):
            fail(f"a passing verdict spelled {status!r} must be recorded")
    ok("all six passing statuses are recorded")


def test_plan_verdict_records_the_ssot() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    for ssot in ("prd", "adr", "api"):
        recorded = gate.recorded_verdicts(f"Plan-Verdict: {ssot}: ok\n")
        if ssot not in recorded:
            fail(f"Plan-Verdict: {ssot} must record {ssot}, got {recorded}")
    ok("each Plan-Verdict SSOT records itself")


def test_plan_verdict_rejects_blocking_status() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    for status in ("violation", "defect", "danger", "needs-new-adr"):
        if gate.recorded_verdicts(f"Plan-Verdict: adr: {status}\n"):
            fail(f"a blocking plan verdict spelled {status!r} must NOT be recorded")
    ok("blocking statuses are not recorded")


def test_plan_verdict_rejects_unknown_ssot() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    for body in (
        "Plan-Verdict: docs: ok\n",
        "Plan-Verdict: api valid\n",
    ):
        if gate.recorded_verdicts(body):
            fail(f"must record nothing: {body!r}")
    ok("an unknown SSOT and a malformed plan-verdict line record nothing")


def test_verdict_parsing_empty_or_none_body() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    if gate.recorded_verdicts(None):
        fail("None body must record nothing")
    if gate.recorded_verdicts(""):
        fail("empty body must record nothing")
    ok("None/empty PR body records no verdicts")


def test_verdict_parsing_rejects_violation_and_malformed() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    if gate.recorded_verdicts("Plan-Verdict: api: violation\n"):
        fail("a 'violation' verdict line must not count as a recorded pass")
    if gate.recorded_verdicts("the api check passed\n"):
        fail("free prose must not be parsed as a recorded verdict")
    ok("'violation' and malformed lines are never recorded as a pass")


def test_end_to_end_no_watched_files_passes_trivially() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    watchlists = gate.load_watchlists()
    required = gate.required_ssots(["surface/src/lib/x.ts"], watchlists)
    if required:
        fail(f"expected zero required SSOTs, got {required}")
    ok("no watched files -> zero required SSOTs (trivial pass)")


def test_end_to_end_missing_verdict_is_detected() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    watchlists = gate.load_watchlists()
    required = gate.required_ssots(["docs/INTERFACES.md"], watchlists)
    recorded = gate.recorded_verdicts("no verdict lines here")
    missing = sorted(set(required) - recorded)
    if missing != ["api"]:
        fail(f"expected api missing, got {missing}")
    ok("a changed watched file with no recorded verdict is flagged missing")


def test_end_to_end_recorded_verdict_satisfies_requirement() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    watchlists = gate.load_watchlists()
    required = gate.required_ssots(["docs/INTERFACES.md"], watchlists)
    recorded = gate.recorded_verdicts("Plan-Verdict: api: pass\n")
    missing = sorted(set(required) - recorded)
    if missing:
        fail(f"expected no missing SSOTs, got {missing}")
    ok("a recorded pass for the required SSOT satisfies the gate")


def test_verdict_parsing_rejects_unavailable() -> None:
    gate = load_module(MERGE_GATE, "check_merge_gate")
    for ssot in ("prd", "adr", "api"):
        body = f"Plan-Verdict: {ssot}: unavailable\n"
        if gate.recorded_verdicts(body):
            fail(f"an 'unavailable' status for {ssot} must not count as a recorded pass")
    ok("'unavailable' is not a verdict and is never recorded as a pass")


def main() -> int:
    tests = [
        test_watchlists_no_third_copy,
        test_ssot_mapping,
        test_required_ssots_groups_by_file,
        test_verdict_parsing_pass,
        test_verdict_parsing_accepts_status_vocabulary,
        test_plan_verdict_records_the_ssot,
        test_plan_verdict_rejects_blocking_status,
        test_plan_verdict_rejects_unknown_ssot,
        test_verdict_parsing_empty_or_none_body,
        test_verdict_parsing_rejects_violation_and_malformed,
        test_verdict_parsing_rejects_unavailable,
        test_end_to_end_no_watched_files_passes_trivially,
        test_end_to_end_missing_verdict_is_detected,
        test_end_to_end_recorded_verdict_satisfies_requirement,
    ]
    failed = 0
    for fn in tests:
        try:
            fn()
        except AssertionError:
            failed += 1
        except Exception as exc:
            print(f"FAIL: {fn.__name__}: {exc}", file=sys.stderr)
            failed += 1

    if failed:
        print(f"\n{failed} test(s) failed", file=sys.stderr)
        return 1
    print(f"\nall {len(tests)} test(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
