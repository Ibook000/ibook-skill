#!/usr/bin/env python3
"""
STM32CubeMX .ioc File Editor

Parses, modifies, and validates .ioc configuration files used by STM32CubeMX.
Preserves file ordering, comments, and maintains consistency of pin/IP lists.

Usage:
    python ioc_editor.py <file.ioc> <command> [args...]

Commands:
    show [--section <prefix>]     Show all or filtered key-value pairs
    get <key>                     Get a single value
    set <key> <value>             Set a key-value pair
    add-pin <pin> --signal <sig> [--mode <mode>] [--locked]
    remove-pin <pin>              Remove a pin and all its keys
    add-ip <ip>                   Add a peripheral IP to Mcu.IP list
    remove-ip <ip>                Remove a peripheral IP from Mcu.IP list
    config <periph> <param> <val> Set a peripheral parameter
    nvic <irq> [--enable] [--priority <p>] [--subpriority <sp>]
    clock <param> <value>         Set an RCC clock parameter
    diff                          Show pending changes (requires --dry-run on set ops)
    validate                      Check consistency of the .ioc file
    backup                        Create a .bak copy
"""

import argparse
import copy
import os
import re
import shutil
import sys
from collections import OrderedDict


class IocFile:
    """Parser and editor for STM32CubeMX .ioc files."""

    def __init__(self, filepath):
        self.filepath = os.path.abspath(filepath)
        self.lines = []          # Raw lines (preserves comments, blank lines, order)
        self.kv = OrderedDict()  # key -> (value, line_index)
        self._parse()

    def _parse(self):
        """Parse the .ioc file into lines and key-value index."""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

        self.kv.clear()
        for idx, line in enumerate(self.lines):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            if '=' not in stripped:
                continue
            key, _, value = stripped.partition('=')
            key = key.strip()
            value = value.strip()
            self.kv[key] = (value, idx)

    def save(self, filepath=None):
        """Write the current state back to file."""
        target = filepath or self.filepath
        with open(target, 'w', encoding='utf-8') as f:
            f.writelines(self.lines)

    def backup(self):
        """Create a .bak backup of the file."""
        bak_path = self.filepath + '.bak'
        shutil.copy2(self.filepath, bak_path)
        return bak_path

    def get(self, key):
        """Get value by key. Returns None if not found."""
        if key in self.kv:
            return self.kv[key][0]
        return None

    def set(self, key, value):
        """Set a key-value pair. Updates existing or appends new."""
        if key in self.kv:
            old_val, idx = self.kv[key]
            self.lines[idx] = f'{key}={value}\n'
            self.kv[key] = (value, idx)
        else:
            # Append before the last line if it's empty, else at end
            new_line = f'{key}={value}\n'
            self.lines.append(new_line)
            self.kv[key] = (value, len(self.lines) - 1)

    def delete(self, key):
        """Delete a key. Returns True if found and removed."""
        if key not in self.kv:
            return False
        _, idx = self.kv[key]
        self.lines[idx] = ''
        del self.kv[key]
        return True

    def keys_with_prefix(self, prefix):
        """Get all keys starting with prefix."""
        return [(k, v) for k, (v, _) in self.kv.items() if k.startswith(prefix)]

    def _renumber_pins(self):
        """Rebuild Mcu.Pin0..Mcu.PinN and Mcu.PinsNb from existing pin entries."""
        pins = []
        for key, (val, _) in self.kv.items():
            if re.match(r'^Mcu\.Pin\d+$', key):
                pins.append(val)
        # Remove old pin entries
        to_delete = [k for k in self.kv if re.match(r'^Mcu\.Pin\d+$', k)]
        for k in to_delete:
            self.delete(k)
        # Re-add in sorted order
        for i, pin in enumerate(sorted(pins)):
            self.set(f'Mcu.Pin{i}', pin)
        self.set('Mcu.PinsNb', str(len(pins)))

    def _renumber_ips(self):
        """Rebuild Mcu.IP0..Mcu.IPN and Mcu.IPNb from existing IP entries."""
        ips = []
        for key, (val, _) in self.kv.items():
            if re.match(r'^Mcu\.IP\d+$', key):
                ips.append(val)
        # Remove old IP entries
        to_delete = [k for k in self.kv if re.match(r'^Mcu\.IP\d+$', k)]
        for k in to_delete:
            self.delete(k)
        # Re-add in sorted order
        for i, ip in enumerate(sorted(ips)):
            self.set(f'Mcu.IP{i}', ip)
        self.set('Mcu.IPNb', str(len(ips)))

    # ── Pin Operations ──────────────────────────────────────────────

    def add_pin(self, pin, signal, mode=None, locked=False):
        """Add or update a pin with signal and optional mode."""
        self.set(f'{pin}.Signal', signal)
        if mode:
            self.set(f'{pin}.Mode', mode)
        if locked:
            self.set(f'{pin}.Locked', 'true')
        # Ensure pin is in the Mcu.Pin list
        existing_pins = [v for k, (v, _) in self.kv.items()
                         if re.match(r'^Mcu\.Pin\d+$', k)]
        if pin not in existing_pins:
            self._renumber_pins()

    def remove_pin(self, pin):
        """Remove a pin and all associated keys."""
        # Find the pin name in Mcu.Pin* entries (may have suffix like -TAMPER-RTC)
        pin_base = pin.split('-')[0] if '-' in pin else pin
        to_remove = []
        for key in list(self.kv.keys()):
            key_pin = key.split('.')[0] if '.' in key else ''
            # Match exact pin or pin with suffix
            if key_pin == pin or key_pin.startswith(pin_base + '-'):
                to_remove.append(key)
        for key in to_remove:
            self.delete(key)
        self._renumber_pins()

    def list_pins(self):
        """List all configured pins with their signals."""
        result = []
        for key, (val, _) in self.kv.items():
            if key.endswith('.Signal') and not key.startswith(('RCC.', 'NVIC.', 'SH.', 'VP_')):
                pin = key.split('.Signal')[0]
                mode = self.get(f'{pin}.Mode')
                result.append({'pin': pin, 'signal': val, 'mode': mode})
        return result

    # ── IP Operations ───────────────────────────────────────────────

    def add_ip(self, ip):
        """Add a peripheral IP to the Mcu.IP list."""
        existing = [v for k, (v, _) in self.kv.items()
                    if re.match(r'^Mcu\.IP\d+$', k)]
        if ip not in existing:
            self._renumber_ips()

    def remove_ip(self, ip):
        """Remove a peripheral IP and all its configuration keys."""
        # Remove from IP list
        to_delete = [k for k, (v, _) in self.kv.items()
                     if re.match(r'^Mcu\.IP\d+$', k) and v == ip]
        for k in to_delete:
            self.delete(k)
        self._renumber_ips()
        # Remove all peripheral config keys
        to_remove = [k for k in self.kv if k.startswith(f'{ip}.')]
        for k in to_remove:
            self.delete(k)

    def list_ips(self):
        """List all configured peripheral IPs."""
        return [v for k, (v, _) in sorted(self.kv.items())
                if re.match(r'^Mcu\.IP\d+$', k)]

    # ── Peripheral Config ───────────────────────────────────────────

    def config_peripheral(self, peripheral, param, value):
        """Set a peripheral parameter (e.g., TIM2.Prescaler=63)."""
        key = f'{peripheral}.{param}'
        # Update IPParameters list if it exists
        ip_params_key = f'{peripheral}.IPParameters'
        ip_params = self.get(ip_params_key)
        if ip_params is not None:
            params_list = [p.strip() for p in ip_params.split(',') if p.strip()]
            if param not in params_list:
                params_list.append(param)
                self.set(ip_params_key, ','.join(params_list))
        self.set(key, value)

    # ── NVIC Operations ─────────────────────────────────────────────

    def nvic_config(self, irq, enable=None, priority=None, subpriority=None):
        """Configure an NVIC interrupt entry."""
        key = f'NVIC.{irq}'
        existing = self.get(key)
        if existing:
            parts = existing.split('\\:')
            # Format: enable\:preempt_priority\:sub_priority\:... (7-9 fields)
            if enable is not None:
                parts[0] = 'true' if enable else 'false'
            if priority is not None and len(parts) > 1:
                parts[1] = str(priority)
            if subpriority is not None and len(parts) > 2:
                parts[2] = str(subpriority)
            self.set(key, '\\:'.join(parts))
        else:
            # New entry with default format
            en = 'true' if enable else 'false'
            pri = str(priority) if priority is not None else '0'
            sub = str(subpriority) if subpriority is not None else '0'
            # Standard format: enable\:pri\:sub\:false\:false\:true\:false\:false\:false
            val = f'{en}\\:{pri}\\:{sub}\\:false\\:false\\:true\\:false\\:false\\:false'
            self.set(key, val)

    # ── Clock Operations ────────────────────────────────────────────

    def set_clock(self, param, value):
        """Set an RCC clock parameter."""
        key = f'RCC.{param}'
        # Update RCC.IPParameters if it exists
        ip_params = self.get('RCC.IPParameters')
        if ip_params is not None:
            params_list = [p.strip() for p in ip_params.split(',') if p.strip()]
            if param not in params_list:
                params_list.append(param)
                self.set('RCC.IPParameters', ','.join(params_list))
        self.set(key, value)

    # ── Validation ──────────────────────────────────────────────────

    def validate(self):
        """Validate consistency of the .ioc file. Returns list of issues."""
        issues = []

        # Check Mcu.PinsNb matches actual pin count
        pin_count_expected = self.get('Mcu.PinsNb')
        pin_entries = [k for k in self.kv if re.match(r'^Mcu\.Pin\d+$', k)]
        if pin_count_expected is not None:
            if str(len(pin_entries)) != pin_count_expected:
                issues.append(
                    f'Mcu.PinsNb={pin_count_expected} but found {len(pin_entries)} Mcu.Pin* entries')

        # Check Mcu.IPNb matches actual IP count
        ip_count_expected = self.get('Mcu.IPNb')
        ip_entries = [k for k in self.kv if re.match(r'^Mcu\.IP\d+$', k)]
        if ip_count_expected is not None:
            if str(len(ip_entries)) != ip_count_expected:
                issues.append(
                    f'Mcu.IPNb={ip_count_expected} but found {len(ip_entries)} Mcu.IP* entries')

        # Check pin numbering is contiguous
        pin_indices = sorted([int(re.match(r'^Mcu\.Pin(\d+)$', k).group(1))
                              for k in self.kv if re.match(r'^Mcu\.Pin\d+$', k)])
        expected_indices = list(range(len(pin_indices)))
        if pin_indices != expected_indices:
            issues.append(
                f'Mcu.Pin* indices not contiguous: {pin_indices} (expected {expected_indices})')

        # Check IP numbering is contiguous
        ip_indices = sorted([int(re.match(r'^Mcu\.IP(\d+)$', k).group(1))
                             for k in self.kv if re.match(r'^Mcu\.IP\d+$', k)])
        expected_ip_indices = list(range(len(ip_indices)))
        if ip_indices != expected_ip_indices:
            issues.append(
                f'Mcu.IP* indices not contiguous: {ip_indices} (expected {expected_ip_indices})')

        # Check each pin has a Signal
        for k, (v, _) in self.kv.items():
            if re.match(r'^Mcu\.Pin\d+$', k):
                signal_key = f'{v}.Signal'
                if signal_key not in self.kv:
                    issues.append(f'Pin {v} (in {k}) has no {signal_key} defined')

        # Check Mcu.CPN and Mcu.UserName exist
        if not self.get('Mcu.CPN'):
            issues.append('Mcu.CPN is missing')
        if not self.get('Mcu.UserName'):
            issues.append('Mcu.UserName is missing')

        return issues

    # ── Display ─────────────────────────────────────────────────────

    def show(self, section=None):
        """Show key-value pairs, optionally filtered by prefix."""
        result = []
        for key, (val, _) in self.kv.items():
            if section and not key.startswith(section):
                continue
            result.append((key, val))
        return result

    def diff_from_original(self, original_lines):
        """Compare current state against original lines. Returns changed lines."""
        original_kv = {}
        for line in original_lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#') or '=' not in stripped:
                continue
            key, _, value = stripped.partition('=')
            original_kv[key.strip()] = value.strip()

        changes = {'added': [], 'modified': [], 'removed': []}
        for key, (val, _) in self.kv.items():
            if key not in original_kv:
                changes['added'].append((key, val))
            elif original_kv[key] != val:
                changes['modified'].append((key, original_kv[key], val))

        for key in original_kv:
            if key not in self.kv:
                changes['removed'].append((key, original_kv[key]))

        return changes


def main():
    parser = argparse.ArgumentParser(
        description='STM32CubeMX .ioc File Editor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('file', help='Path to .ioc file')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show changes without saving')

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # show
    p_show = subparsers.add_parser('show', help='Show key-value pairs')
    p_show.add_argument('--section', help='Filter by key prefix')

    # get
    p_get = subparsers.add_parser('get', help='Get a single value')
    p_get.add_argument('key', help='Key to look up')

    # set
    p_set = subparsers.add_parser('set', help='Set a key-value pair')
    p_set.add_argument('key', help='Key to set')
    p_set.add_argument('value', help='Value to assign')

    # add-pin
    p_apin = subparsers.add_parser('add-pin', help='Add or update a pin')
    p_apin.add_argument('pin', help='Pin name (e.g., PA9, PB6)')
    p_apin.add_argument('--signal', required=True, help='Signal assignment')
    p_apin.add_argument('--mode', help='Mode (e.g., Asynchronous, I2C)')
    p_apin.add_argument('--locked', action='store_true', help='Lock the pin')

    # remove-pin
    p_rpin = subparsers.add_parser('remove-pin', help='Remove a pin')
    p_rpin.add_argument('pin', help='Pin name to remove')

    # add-ip
    p_aip = subparsers.add_parser('add-ip', help='Add a peripheral IP')
    p_aip.add_argument('ip', help='IP name (e.g., I2C1, TIM2)')

    # remove-ip
    p_rip = subparsers.add_parser('remove-ip', help='Remove a peripheral IP')
    p_rip.add_argument('ip', help='IP name to remove')

    # config
    p_cfg = subparsers.add_parser('config', help='Set peripheral parameter')
    p_cfg.add_argument('peripheral', help='Peripheral name (e.g., TIM2)')
    p_cfg.add_argument('param', help='Parameter name')
    p_cfg.add_argument('value', help='Parameter value')

    # nvic
    p_nvic = subparsers.add_parser('nvic', help='Configure NVIC interrupt')
    p_nvic.add_argument('irq', help='IRQ name (e.g., USART1_IRQn)')
    p_nvic.add_argument('--enable', action='store_true', help='Enable interrupt')
    p_nvic.add_argument('--disable', action='store_true', help='Disable interrupt')
    p_nvic.add_argument('--priority', type=int, help='Preempt priority')
    p_nvic.add_argument('--subpriority', type=int, help='Sub-priority')

    # clock
    p_clk = subparsers.add_parser('clock', help='Set RCC clock parameter')
    p_clk.add_argument('param', help='RCC parameter name')
    p_clk.add_argument('value', help='Clock value')

    # validate
    subparsers.add_parser('validate', help='Validate .ioc consistency')

    # backup
    subparsers.add_parser('backup', help='Create .bak backup')

    # list-pins
    subparsers.add_parser('list-pins', help='List all configured pins')

    # list-ips
    subparsers.add_parser('list-ips', help='List all configured IPs')

    # diff
    subparsers.add_parser('diff', help='Show pending changes')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    filepath = os.path.abspath(args.file)
    if not os.path.isfile(filepath):
        print(f'Error: File not found: {filepath}', file=sys.stderr)
        sys.exit(1)

    ioc = IocFile(filepath)
    original_lines = copy.deepcopy(ioc.lines)

    try:
        if args.command == 'show':
            entries = ioc.show(section=args.section)
            for key, val in entries:
                print(f'{key}={val}')
            print(f'\n# Total: {len(entries)} entries')

        elif args.command == 'get':
            val = ioc.get(args.key)
            if val is None:
                print(f'Key not found: {args.key}', file=sys.stderr)
                sys.exit(1)
            print(val)

        elif args.command == 'set':
            ioc.set(args.key, args.value)
            print(f'Set: {args.key}={args.value}')

        elif args.command == 'add-pin':
            ioc.add_pin(args.pin, args.signal, mode=args.mode, locked=args.locked)
            print(f'Added pin: {args.pin} -> {args.signal}')

        elif args.command == 'remove-pin':
            ioc.remove_pin(args.pin)
            print(f'Removed pin: {args.pin}')

        elif args.command == 'add-ip':
            ioc.add_ip(args.ip)
            print(f'Added IP: {args.ip}')

        elif args.command == 'remove-ip':
            ioc.remove_ip(args.ip)
            print(f'Removed IP: {args.ip}')

        elif args.command == 'config':
            ioc.config_peripheral(args.peripheral, args.param, args.value)
            print(f'Set: {args.peripheral}.{args.param}={args.value}')

        elif args.command == 'nvic':
            enable = None
            if args.enable:
                enable = True
            elif args.disable:
                enable = False
            ioc.nvic_config(args.irq, enable=enable,
                            priority=args.priority,
                            subpriority=args.subpriority)
            print(f'Updated NVIC: {args.irq}')

        elif args.command == 'clock':
            ioc.set_clock(args.param, args.value)
            print(f'Set clock: RCC.{args.param}={args.value}')

        elif args.command == 'validate':
            issues = ioc.validate()
            if issues:
                print(f'Found {len(issues)} issue(s):')
                for i, issue in enumerate(issues, 1):
                    print(f'  {i}. {issue}')
                sys.exit(1)
            else:
                print('Validation passed: no issues found.')

        elif args.command == 'backup':
            bak = ioc.backup()
            print(f'Backup created: {bak}')

        elif args.command == 'list-pins':
            pins = ioc.list_pins()
            for p in pins:
                mode_str = f' (mode={p["mode"]})' if p['mode'] else ''
                print(f'{p["pin"]}: {p["signal"]}{mode_str}')
            print(f'\n# Total: {len(pins)} pins')

        elif args.command == 'list-ips':
            ips = ioc.list_ips()
            for ip in ips:
                print(ip)
            print(f'\n# Total: {len(ips)} IPs')

        elif args.command == 'diff':
            changes = ioc.diff_from_original(original_lines)
            has_changes = False
            if changes['added']:
                has_changes = True
                print('--- Added ---')
                for key, val in changes['added']:
                    print(f'+ {key}={val}')
            if changes['modified']:
                has_changes = True
                print('--- Modified ---')
                for key, old, new in changes['modified']:
                    print(f'~ {key}: {old} -> {new}')
            if changes['removed']:
                has_changes = True
                print('--- Removed ---')
                for key, val in changes['removed']:
                    print(f'- {key}={val}')
            if not has_changes:
                print('No changes.')

        # Save unless dry-run or read-only command
        read_only = {'show', 'get', 'validate', 'list-pins', 'list-ips', 'diff'}
        if args.command not in read_only and not args.dry_run:
            ioc.save()
            print(f'Saved to: {filepath}')

    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
