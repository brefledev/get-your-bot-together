#!/usr/bin/env python3
"""Cursor LOCAL beforeMCPExecution guard. No network, credential access or writes.

Reads Cursor's JSON event on stdin and the adjacent review-policy.json.
Unknown well-formed tools ASK. Approved read tools ALLOW. Configured send tools
DENY unsupported/unapproved recipients and ASK even when all recipients match.
This does not govern shell/browser calls, Cursor Cloud, or another assistant.
"""
import json
import re
import sys
from pathlib import Path

MAX_BYTES = 1_048_576
POLICY = Path(__file__).resolve().with_name("review-policy.json")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def decode(text):
    return json.loads(text, object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def address(value):
    # Deliberately narrow: no display names, comma lists, nested objects or headers.
    # An adapter for a different tool schema must be reviewed separately.
    if not isinstance(value, str) or len(value) > 254:
        raise ValueError("unsupported address")
    if not re.fullmatch(r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,63}", value):
        raise ValueError("unsupported address")
    local, domain = value.rsplit("@", 1)
    if local.startswith('.') or local.endswith('.') or '..' in local:
        raise ValueError("unsupported address")
    if any(not label or label.startswith('-') or label.endswith('-') for label in domain.split('.')):
        raise ValueError("unsupported address")
    return local + '@' + domain.lower()


def identity(entry):
    if not isinstance(entry, dict):
        raise ValueError("invalid tool record")
    values = entry.get("server"), entry.get("tool")
    if any(not isinstance(x, str) or not x or x != x.strip() or any(ord(c) < 32 for c in x) for x in values):
        raise ValueError("missing tool identity")
    return values


def validate_policy(policy):
    expected = {"version", "read_tools", "send_tools", "blocked_tools", "allowed_recipients"}
    if not isinstance(policy, dict) or set(policy) != expected or type(policy['version']) is not int or policy['version'] != 1:
        raise ValueError("invalid policy")
    for group in expected - {"version"}:
        if not isinstance(policy[group], list):
            raise ValueError("invalid policy list")
    recipients = {address(x) for x in policy['allowed_recipients']}
    reads, blocks, sends, seen = set(), set(), {}, set()
    for group, target in [('read_tools', reads), ('blocked_tools', blocks), ('send_tools', sends)]:
        for entry in policy[group]:
            key = identity(entry)
            if key in seen:
                raise ValueError("duplicate or conflicting tool policy")
            seen.add(key)
            fields = {'server', 'tool', 'recipient_fields', 'input_fields'} if group == 'send_tools' else {'server', 'tool'}
            if set(entry) != fields:
                raise ValueError("unsupported tool policy field")
            if group == 'send_tools':
                paths = entry['recipient_fields']
                if not isinstance(paths, list) or not paths or any(not isinstance(x, str) or not x or x != x.strip() for x in paths) or len(set(paths)) != len(paths):
                    raise ValueError("invalid recipient fields")
                input_fields = entry['input_fields']
                if not isinstance(input_fields, list) or not input_fields or any(not isinstance(x, str) or not x or x != x.strip() for x in input_fields) or len(set(input_fields)) != len(input_fields) or not set(paths).issubset(input_fields):
                    raise ValueError('invalid input fields')
                sends[key] = (paths, set(input_fields))
            else:
                target.add(key)
    return reads, blocks, sends, recipients


def response(permission, message):
    return {"permission": permission, "user_message": message, "agent_message": message}


def evaluate(event, policy):
    reads, blocks, sends, allowed = validate_policy(policy)
    if not isinstance(event, dict):
        raise ValueError("invalid event")
    key = identity({'server': event.get('mcp_server_name'), 'tool': event.get('tool_name')})
    raw = event.get('tool_input')
    if not isinstance(raw, str):
        raise ValueError("Cursor tool_input must be a JSON string")
    payload = decode(raw)
    if not isinstance(payload, dict):
        raise ValueError("tool input must decode to an object")
    if key in blocks:
        return response('deny', 'This tool is blocked for the review workflow. Return the draft to its owner.')
    if key in reads:
        return response('allow', 'This exact tool is approved as read-only in the review policy.')
    if key not in sends:
        return response('ask', 'This tool is not pre-approved for this review. Inspect its actual inputs before allowing it; recipient checks have not been applied.')
    recipient_fields, input_fields = sends[key]
    if not set(payload).issubset(input_fields):
        return response('deny', 'This call has fields outside the reviewed tool schema. Recheck the policy mapping before taking the action.')
    found = []
    for field in recipient_fields:
        if field not in payload or payload[field] is None or payload[field] == '':
            continue
        values = payload[field] if isinstance(payload[field], list) else [payload[field]]
        found.extend(address(x) for x in values)
    if not found:
        return response('deny', 'No recipients could be verified in this call. A draft ID alone is insufficient; return the current draft for owner review.')
    if any(x not in allowed for x in found):
        return response('deny', 'A recipient is outside the approved list. Return the draft and proposed recipient change to the owner.')
    return response('ask', 'The configured recipient fields match the list. Review the final message and attachments before allowing this send; recipient matching is not content approval.')


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        policy_raw = POLICY.read_bytes()
        if len(raw) > MAX_BYTES or len(policy_raw) > MAX_BYTES:
            raise ValueError('input too large')
        result = evaluate(decode(raw.decode('utf-8')), decode(policy_raw.decode('utf-8')))
    except Exception:
        # Do not echo possibly private inputs or traceback into hook output.
        result = response('deny', 'The review guard could not validate this call or its policy. Fix the configuration; do not bypass it to complete the action.')
    sys.stdout.write(json.dumps(result) + '\n')


if __name__ == '__main__':
    main()
