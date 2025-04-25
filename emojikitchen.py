import json
import sys
import re
from typing import List, Dict, Optional

class EmojiKitchen:
    def __init__(self, json_path: str = "emojikitchen.json"):
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.emoji_data = self.data.get("data", {})

    def get_combinations_for_emoji(self, emoji_codepoint: str) -> List[Dict]:
        results = []
        emoji_entry = self.emoji_data.get(emoji_codepoint)
        if not emoji_entry:
            print(f"[!] Emoji {emoji_codepoint} not found.")
            return results

        combinations = emoji_entry.get("combinations", {})
        for partner_codepoint, combo_list in combinations.items():
            for combo in combo_list:
                results.append({
                    "leftEmoji": combo["leftEmoji"],
                    "leftCodepoint": combo["leftEmojiCodepoint"],
                    "rightEmoji": combo["rightEmoji"],
                    "rightCodepoint": combo["rightEmojiCodepoint"],
                    "alt": combo["alt"],
                    "image": combo["gStaticUrl"]
                })
        return results

    def get_combo_result(self, emoji1_codepoint: str, emoji2_codepoint: str) -> Optional[Dict]:
        emoji_entry = self.emoji_data.get(emoji2_codepoint)
        if not emoji_entry:
            print(f"[!] Emoji {emoji2_codepoint} not found.")
            return None

        combinations = emoji_entry.get("combinations", {})
        combo_list = combinations.get(emoji1_codepoint)
        if not combo_list:
            print(f"[!] No combination found for {emoji1_codepoint} + {emoji2_codepoint}")
            return None

        combo = combo_list[0]
        return {
            "leftEmoji": combo["leftEmoji"],
            "leftCodepoint": combo["leftEmojiCodepoint"],
            "rightEmoji": combo["rightEmoji"],
            "rightCodepoint": combo["rightEmojiCodepoint"],
            "alt": combo["alt"],
            "image": combo["gStaticUrl"]
        }


def emoji_to_codepoint(s: str) -> str:
    # Converts an emoji (e.g. 😀) to codepoint string (e.g. 1f600 or 1f1e6-1f1fa for flags)
    return '-'.join([f"{ord(c):x}" for c in s])


def escape_to_codepoint(escape: str) -> str:
    """ Convert unicode escape like u1fae9 to proper codepoint 1fae9 """
    match = re.match(r'^u([0-9a-fA-F]+)$', escape)
    if match:
        return match.group(1)
    return escape


def normalize_input(arg: str) -> str:
    # If input is emoji (raw), convert to codepoint; otherwise, handle as hex
    if 'u' in arg:  # check if it's a unicode escape like u1fae9
        return escape_to_codepoint(arg)
    elif all(part in arg for part in ['0', '1', '2', '3', '4', '5', '6', '7',
                                      '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', '-', 'A', 'B', 'C', 'D', 'E', 'F']):
        # It's a valid codepoint hex format already
        return arg.lower()
    else:
        # Treat it as raw emoji
        return emoji_to_codepoint(arg)


def main():
    args = sys.argv[1:]
    if not args or len(args) > 2:
        print("Usage: python emoji_kitchen.py <emoji/codepoint> [emoji/codepoint]")
        return

    ek = EmojiKitchen()

    # Normalize inputs (either emoji or codepoint)
    inputs = [normalize_input(arg) for arg in args]

    if len(inputs) == 1:
        print(f"=== All combinations for {args[0]} ({inputs[0]}) ===")
        combos = ek.get_combinations_for_emoji(inputs[0])
        for c in combos:
            print(f"{c['leftEmoji']} ({c['leftCodepoint']}) + {c['rightEmoji']} ({c['rightCodepoint']})")
            print(f"  Alt: {c['alt']}")
            print(f"  URL: {c['image']}\n")
    else:
        left, right = inputs
        print(f"=== Combo: {args[0]} + {args[1]} ===")
        combo = ek.get_combo_result(left, right)
        if combo:
            print(f"{combo['leftEmoji']} ({combo['leftCodepoint']}) + {combo['rightEmoji']} ({combo['rightCodepoint']})")
            print(f"  Alt: {combo['alt']}")
            print(f"  URL: {combo['image']}\n")


if __name__ == '__main__':
    main()